from typing import Optional

_exception = Exception.__str__


class WillRaise(object):

    def __init__(self,  *exceptions):
        # use duck typing to determine if the obj is an exception 
        assert all(map(lambda obj: obj.__str__ is _exception, exceptions))# Raise here # TODO add test # Add new exception

        self.exceptions = exceptions
        self.exception = None
        self.exc_type = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> Optional[bool]:

        if exc_type in self.exceptions:
            self.exception = exc_value
            self.exc_type = exc_type
            return True
