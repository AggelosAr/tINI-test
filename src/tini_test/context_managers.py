import sys
import threading
from contextlib import contextmanager
from io import StringIO
from typing import Optional

from .misc.exceptions import (ExceptionWasNotRaised,
                              WillRaiseReceivedNotAnException)

_exceptions = (Exception, BaseException)

_local_thread = threading.local() # Is this safe here? TODO


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

    def __init__(self):
        raise NotImplementedError


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
