import inspect
import sys
import threading
from collections import deque
from contextlib import contextmanager
from functools import partial
from io import StringIO
from threading import Lock
from typing import Any, Callable, Generator, Optional

from tini_test._internals.consts import _INIT, _SETNINEL
from tini_test.coverage._coverage import CoverageTracker
from tini_test.misc.annotations import (CoverageStore, DirectoryPath,
                                        TestCallable)
from tini_test.mock import (ARTIFACT_TRACKER, FILE_TRACKER, BuiltInArtifact,
                            MockDefinition, Mocking, MockNone)
from tini_test.shared import MetaSharedVar, SharedVar, direct_access

from .misc.exceptions import (ExceptionWasNotRaised,
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



class TraceHandler:
        
        def __init__(self):
            self._tracers = {}

        def __call__(self, *args, **kwargs) -> Callable:
            tracer = partial(lambda *args, **kwargs: None, *args, **kwargs)
            for tracer in self._tracers.values():
                tracer = partial(tracer, *args, **kwargs)
            
            return tracer

        @classmethod
        @contextmanager
        def trace_on(self, tracer: Callable) -> Generator[None, None, None]:
            previous_sys_trace = sys.gettrace()
            previous_thread_trace = threading.gettrace()

            sys.settrace(tracer)
            threading.settrace(tracer)
            
            try:
                yield

            finally:

                sys.settrace(previous_sys_trace)
                threading.settrace(previous_thread_trace)

        def raise_on(self) -> None:
            raise NotImplementedError()

        def attach(self, tracer: Callable) -> None:
            # print('ATTACHING TRACER ', tracer)
            self._tracers[hex(id(tracer))] = tracer

        def detach(self, tracer: Callable) -> None:
            del self._tracers[hex(id(tracer))]

        def clear(self) -> None:
            self._tracers.clear()
            


@contextmanager
def handle_tracers(trace: bool) -> Generator[TraceHandler, None, None]:
    if trace:
        previous_sys_trace = sys.gettrace()
        previous_thread_trace = threading.gettrace()

        _trace_handle = TraceHandler()

        sys.settrace(_trace_handle)
        threading.settrace(_trace_handle)

        try:
            yield _trace_handle

        finally:
            sys.settrace(previous_sys_trace)
            threading.settrace(previous_thread_trace)

            _trace_handle.clear()
    else:
        yield



@contextmanager
def coverage(trace_on: bool, storage: CoverageStore, 
             handle: Optional[TraceHandler] = None) -> Generator[None, None, None]:
    if trace_on:

        tracer = partial(CoverageTracker.tracer, storage)

        if handle:
            handle.attach(tracer)

        try:
            if handle:
                yield
            else:
                with TraceHandler.trace_on(tracer):
                    yield 

        finally:
            if handle:
                handle.detach(tracer)
    else:
        yield



@contextmanager
def patch_built_ins(apply_at: DirectoryPath, is_root: Optional[bool] = False, 
                    handle: Optional[TraceHandler] = None) -> Generator[None, None, None]:

    tracer = partial(BuiltInArtifact.built_in_replacer, apply_at, is_root)

    if handle:
        handle.attach(tracer)

    try:
        if handle:
            yield
        else:
            with TraceHandler.trace_on(tracer):
                yield 
        
    finally:
        if handle:
            handle.detach(tracer)



@contextmanager
def patch_mocks(mocks: list[MockDefinition], replace_at: DirectoryPath, 
                handle: Optional[TraceHandler] = None) -> Generator[None, None, None]:
        
    if mocks:
        try:
            MockDefinition.patch_all(mocks)

            with patch_built_ins(replace_at, True, handle):

                yield

        finally:
            MockDefinition.restore_all(mocks)
            
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



class _CX_Mocking:

    @staticmethod
    @contextmanager
    def mocking(mock    : Optional[Any] = MockNone,
                *,
                returns : Optional[Any] = MockNone, 
                args    : Optional[Any] = MockNone,
                kwargs  : Optional[Any] = MockNone) -> Generator[None, None, None]:
        '''
        No guarantee is made that the mocked object will not intefere with the original
        during `async` mode.

        * Use the the `@Isolate` decorator to ensure isolation.

        * (Should only be used inside a `@Test.case` decorated function.)
        '''
        ARTIFACT_TRACKER.append(_SETNINEL) # type: ignore [arg-type]

        mock      = BuiltInArtifact._CX_get_original_if_exists(mock)
        mock_body = MockDefinition.validate_definition(mock, returns, args, kwargs)
        _mock     = MockDefinition(mock_body)

        
        mocking = Mocking(inspect.currentframe())
        mocking._rewind_frames()

        MockDefinition.add_scope(_mock, mocking.real_test)

        # This mock is closer to the actual call site than the decorator-based mocks if any.
        # This mock is also closer to any local mocks that may exist in the current scope.
        relevant_mocks = Mocking._CX_get_previous_mocks(_mock)
        if not relevant_mocks:
            Mocking._CX_register(_mock)

        current_builtins = len(ARTIFACT_TRACKER)

        try:
            # Restore previous mocks before applying the new mock
            deque(map(lambda mock: mock.restore(), relevant_mocks), maxlen=0)

            # Patch current mock
            _mock.patch()

            # If we found built-in patch it.
            if _mock._isbuiltin:
                BuiltInArtifact._CX_patch_initial(mocking.rewinded_frames, _INIT[0]._ROOT)

            # If we will find any built-ins patch them.
            with patch_built_ins(apply_at=_INIT[0]._ROOT):
                yield


        finally:
            # Clear the buffer
            FILE_TRACKER.clear()

            # Restore the mock
            _mock.restore()

            # Unregister the mock if it was registered previously
            if not relevant_mocks:
                Mocking._CX_unregister(_mock)

            # Here we must check if the mock was a built-in and re-patch if necessary
            # If we generated any artifacts during the process, we need to re-patch them
            if _mock._isbuiltin or len(ARTIFACT_TRACKER) > current_builtins:
                BuiltInArtifact._CX_maybe_re_patch_level()

            # Re-apply all relevant mocks to restore the previous state
            MockDefinition.patch_all(relevant_mocks)
