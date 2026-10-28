import inspect
import os
import sys
import threading
from collections import deque
from contextlib import contextmanager
from functools import partial
from io import StringIO
from threading import Lock
from typing import Any, Generator, Optional

from tini_test._internals.consts import _ROOT, _SETNINEL
from tini_test.coverage._coverage import CoverageTracker
from tini_test.misc.annotations import (CoverageStore, DirectoryPath,
                                        TestCallable)
from tini_test.mock import (ARTIFACT_TRACKER, TRACKING_GLOBALS,
                            BuiltInArtifact, MockDefinition, MockNone)
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
def patch_built_ins(apply_at: DirectoryPath):
    previous = sys.gettrace()
    sys.settrace(partial(BuiltInArtifact.built_in_replacer, apply_at))
    try:
        yield
    finally:
        sys.settrace(previous)



@contextmanager
def patch_mocks(mocks: list[MockDefinition], replace_at: DirectoryPath) -> Generator[None, None, None]:
    if mocks:
        try:
            MockDefinition.patch_all(mocks)

            with patch_built_ins(replace_at):

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
        during `async` mode.

        * Use the the `@Isolate` decorator to ensure isolation. TODO fix isolate... ~1 / 1_000_000+? error rate ?

        * (Should only be used inside a `@Test.case` decorated function.)
        '''
        frame = inspect.currentframe()
        previous = frame


        # In case of built-in mocks, we need to manually track the frames 
        # Untill we reach the entry point ...................
        frames = []
        files = []

        # Go back ~two frames to find the `run_step` ... bad but necessary, breaks on async I suppose
        while frame and frame.f_code.co_name != 'run_step':
            previous = frame
            frame = frame.f_back

            frames.append(frame)
            files.append(os.path.abspath(frame.f_code.co_filename))

        # frames.pop()
        # files.pop()

        # Last frame and first needs to be filtered .... TODO 

         
        frame = previous

    
        real_test = MockDefinition._cx_get_real_test(frame)

        mock = BuiltInArtifact.get_original_if_exists(mock)

        mock_body = MockDefinition.validate_definition(mock, returns, args, kwargs)
        _mock = MockDefinition(mock_body)

        MockDefinition.add_scope(_mock, real_test)

        # This mock is closer to the actual call site than the decorator-based mocks if any.
        # This mock is also closer to any local mocks that may exist in the current scope.
        relevant_mocks = _mock._cx_get_previous_mocks()

        ARTIFACT_TRACKER.append(_SETNINEL)
        
        if not relevant_mocks:
            _mock._cx_register()
        
        try:
            deque(map(lambda mock: mock.restore(), relevant_mocks), maxlen=0)

            _mock.patch()

            if _mock._isbuiltin:

                current_frame_file = os.path.abspath(frame.f_code.co_filename)

                last_artifact = ARTIFACT_TRACKER[-1]

                TRACKING_GLOBALS.add(current_frame_file)

                for file_name, frame in zip(files, frames):
                    TRACKING_GLOBALS.add(file_name)
                    frame.f_globals[last_artifact.__name__] = last_artifact.replacement
                    last_artifact.applied_at.append(frame.f_globals)

           
            with patch_built_ins(*_ROOT):

                yield


        finally:
            TRACKING_GLOBALS.clear()
            _mock.restore()

            
            if not relevant_mocks:
                _mock._cx_unregister()

            MockDefinition.patch_all(relevant_mocks)

            if _mock._isbuiltin:

                while ARTIFACT_TRACKER:
                    artifact = ARTIFACT_TRACKER.pop()

                    if artifact is _SETNINEL:
                        break

                    for global_dict in artifact.applied_at:
                        global_dict[artifact.__name__] = artifact.original

                to_add = []
                while ARTIFACT_TRACKER:
                    artifact = ARTIFACT_TRACKER.pop()
                    to_add.append(artifact)

                    if artifact is _SETNINEL:
                        break

                    for global_dict in artifact.applied_at:
                        global_dict[artifact.__name__] = artifact.replacement

                ARTIFACT_TRACKER.extend(reversed(to_add))

