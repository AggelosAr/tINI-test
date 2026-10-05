


from typing import Callable

from tini_test.misc.annotations import MockWrappedObject, TestWrappedObject
from tini_test.misc.exceptions import SharedOnlyAcceptsArguments




class Shared:

    def __new__(cls, *args, **kwargs):
        if not kwargs:
            raise SharedOnlyAcceptsArguments
        
        return Shared.shared(*args, **kwargs)

    @classmethod
    def shared(cls,
               func: None
                     | Callable
                     | MockWrappedObject 
                     | TestWrappedObject = None,
               *args: tuple[]):
        

        def wrapper(func):

            def _wrapper(*args, **kwargs):

               return

            
          
         

            return _wrapper


        return wrapper
