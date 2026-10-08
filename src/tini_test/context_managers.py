import sys
import threading
from collections import deque
from contextlib import contextmanager
from io import StringIO
from threading import Lock
from typing import Generator, Optional

from tini_test.misc.annotations import TestCallable, TestFunctionName
from tini_test.mock import MockDefinition
from tini_test.shared import MetaSharedVar, SharedVar

from .misc.exceptions import (CouldNotFindMetaSharedVar, ExceptionWasNotRaised,
                              WillRaiseReceivedNotAnException)

_exceptions = (Exception, BaseException)

_local_thread = threading.local()

_lock = Lock()


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
        
        # TODO maybe add a helpfull message on ExceptionWasNotRaised
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
    # TODO add match on enum to discard output and exception traces in minimal modes ( which ones? )
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
def patch_mocks(mocks: list[MockDefinition]) -> Generator[None, None, None]:
    if mocks:
        with _lock:
            try:
                deque(map(lambda mock: mock.patch(), mocks), maxlen=0)
                yield
            finally:
                deque(map(lambda mock: mock.restore(), mocks), maxlen=0)
    else:
        yield



# TODO this propably breaks again on async
# We should create a seperate scope for each test.....
# TODO this should be applied 1 step above?
@contextmanager
def patch_shared(root_name: TestFunctionName, 
                 patching: TestCallable, 
                 shared_vars: list[SharedVar]) -> Generator[None, None, None]:
    if shared_vars:
       
        try:
            old_meta = MetaSharedVar.extract_meta(_from=patching)

            if old_meta is None or not isinstance(old_meta, MetaSharedVar):
                raise CouldNotFindMetaSharedVar(test_name=root_name)

            local_context = MetaSharedVar.get_context_from_shards(shared_vars)

            old_meta.update_local_context(test_name=root_name, context=local_context)

            yield

        finally:
            ...

    else:
        yield

