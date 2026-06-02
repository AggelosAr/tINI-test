from typing import Optional

from small_test.misc.exceptions import WillRaiseReceivedNotAnException

_exception = Exception.__str__


class WillRaise(object):

    def __init__(self,  *exceptions) -> None:
        # use duck typing to determine if the obj is an exception 
        try:
            assert all(map(lambda obj: obj.__str__ is _exception, exceptions))
        except:
            raise WillRaiseReceivedNotAnException

        self.exceptions = exceptions
        self.exception = None
        self.exc_type = None
        self.exc_traceback = None
    
    def __enter__(self) -> 'WillRaise':
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> Optional[bool]:

        if exc_type in self.exceptions:
            self.exception = exc_value
            self.exc_type = exc_type
            self.exc_traceback = exc_traceback
            return True
        
        return False
