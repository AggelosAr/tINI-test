from functools import partial
from typing import Optional

from small_test.misc.exceptions import (ExceptionWasNotRaised,
                                        WillRaiseReceivedNotAnException)

_exceptions = (Exception, BaseException)

# TODO Maybe add MaybeWillRaise

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
