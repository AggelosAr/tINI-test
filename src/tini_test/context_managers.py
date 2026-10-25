import inspect
import sys
import threading
from collections import deque
from contextlib import contextmanager
from functools import partial
from io import StringIO
from threading import Lock
from typing import Any, Generator, Optional

from tini_test.coverage._coverage import CoverageTracker
from tini_test.misc.annotations import CoverageStore, TestCallable
from tini_test.mock import MockDefinition, MockNone
from tini_test.shared import MetaSharedVar, SharedVar, direct_access

from .misc.exceptions import (ExceptionWasNotRaised,
                              WillRaiseReceivedNotAnException)

_exceptions = (Exception, BaseException)

_local_thread = threading.local()

_lock = Lock()

_tracer = CoverageTracker.tracer


class WillRaise(object):

    def __init__(self,  *exceptions) -> None:
        try:
            assert any(issubclass(e, _e) for e in exceptions for _e in _exceptions)
        except:
            raise WillRaiseReceivedNotAnException

        # Normalize exceptions
        self.exceptions = set(map(lambda l: l.__name__, exceptions))
        self.exception = None
        self.exc_type = None
        self.exc_traceback = None
    
    def __enter__(self) -> 'WillRaise':
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> Optional[bool]:
        if exc_type and exc_type.__name__ in self.exceptions:

            self.exception = exc_value
            self.exc_type = exc_type
            self.exc_traceback = exc_traceback
            return True
        
        raise ExceptionWasNotRaised


class MaybeWillRaise(object):
    ...


class _ThreadLocalStdout:
    def __init__(self, default_stream):
        self._default_stream = default_stream

    def write(self, text: str) -> int:
        stream = getattr(_local_thread, 'stream', None)
        if stream is not None:
            return stream.write(text)
        return self._default_stream.write(text)

    def flush(self) -> None:
        stream = getattr(_local_thread, 'stream', None)
        if stream is not None:
            return stream.flush()
        return self._default_stream.flush()

    def isatty(self) -> bool:
        stream = getattr(_local_thread, 'stream', None)
        if stream is not None and hasattr(stream, 'isatty'):
            return stream.isatty()
        return getattr(self._default_stream, 'isatty', lambda: False)()

    def __getattr__(self, name: str):
        return getattr(self._default_stream, name)


sys.stdout = _ThreadLocalStdout(sys.stdout)



@contextmanager
def _thread_redirect_stdout(stream: StringIO):
    previous = getattr(_local_thread, 'stream', None)
    _local_thread.stream = stream
    try:
        yield
    finally:
        if previous is None:
            del _local_thread.stream
        else:
            _local_thread.stream = previous



@contextmanager
def with_lock(use: bool) -> Generator[None, None, None]:
    if use:
        _lock.acquire()
    try:
        yield
    finally:
        if use:
            _lock.release()



@contextmanager
def patch_mocks(mocks: list[MockDefinition]) -> Generator[None, None, None]:
    if mocks:
        try:
            deque(map(lambda mock: mock.patch(), mocks), maxlen=0)
            yield
        finally:
            deque(map(lambda mock: mock.restore(), mocks), maxlen=0)
    else:
        yield



@contextmanager
def patch_shared(patching: TestCallable, shared_vars: list[SharedVar]) -> Generator[None, None, None]:
    if shared_vars:

        meta = MetaSharedVar.get_meta_var()
       
        try:
            with direct_access(meta) as _meta:
                local_context = _meta.get_context_from_shards(shared_vars)
                
                test_name = patching.__name__
                _meta.update_local_context(test_name=test_name, context=local_context)

            yield

        finally:

            with direct_access(meta) as _meta:
                _meta.test_reset()

    else:
        yield



@contextmanager
def coverage(trace: bool, storage: CoverageStore) -> Generator[None, None, None]:
    if trace:
        previous = sys.gettrace()
        sys.settrace(partial(_tracer, storage))
        try:
            yield
        finally:
            sys.settrace(previous)
    else:
        yield



class Mock:

    @staticmethod
    @contextmanager
    def mocking(mock    : Optional[Any] = MockNone,
                *,
                returns : Optional[Any] = MockNone, 
                args    : Optional[Any] = MockNone,
                kwargs  : Optional[Any] = MockNone) -> Generator[None, None, None]:
        '''
        No guarantee is made that the mocked object will not intefere with the original
        during `async` mode. @inspect

        * Use the the `@Isolate` decorator to ensure isolation.

        Should only be used inside a `@Test.case` decorated function.
        '''
        mock_body = MockDefinition.validate_mock(mock, returns, args, kwargs)
        _mock = MockDefinition(mock, body=mock_body)
        
        # @inspect
        frame = inspect.currentframe().f_back.f_back
        test_name = frame.f_code.co_name

        _mock.test_name = test_name

        # This mock is closer to the actual call site than the decorator-based mocks if any.
        # This mock is also closer to any local mocks that may exist in the current scope.
        relevant_mocks = MockDefinition._get_previous_mocks(_mock)
        if not relevant_mocks:
            MockDefinition.register(_mock)
        
        try:
            deque(map(lambda __mock: __mock.restore(), relevant_mocks), maxlen=0)
            _mock.patch()
            yield
        finally:
            _mock.restore()
            if not relevant_mocks:
                MockDefinition.unregister(_mock)
            deque(map(lambda __mock: __mock.patch(), relevant_mocks), maxlen=0)
