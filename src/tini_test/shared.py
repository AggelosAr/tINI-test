from typing import Any, Callable, Optional

from tini_test.misc.annotations import MockWrappedObject, TestWrappedObject
from tini_test.misc.exceptions import SharedOnlyAcceptsArguments




class Shared:

    def __new__(cls, *args: tuple[Any], **kwargs: Any):

        if kwargs:
            raise SharedOnlyAcceptsArguments

        return Shared.shared(*args)

    @classmethod
    def shared(cls,
               func: None
                     | Callable
                     | MockWrappedObject 
                     | TestWrappedObject = None,
                
               *args: Optional[tuple[Any]]):
        

        def wrapper(func):

            def _wrapper(*args, **kwargs):

               return

            
          
         

            return _wrapper

        if callable(func):
            return wrapper(func)

        return wrapper
