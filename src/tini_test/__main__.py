from .arg_parser import ArgsDict, receive_args
from .initializer import initialize_test_suite
from .misc.exceptions import CantFindRelativePathToRoot, TestNotFound


def _tini_test(kwargs: ArgsDict):
    
    try:
        test_suite = initialize_test_suite(**kwargs)
         
    except CantFindRelativePathToRoot:
        raise

    except TestNotFound:
        raise

    else:
        test_suite.runner()
        test_suite.pprint()


if __name__=='__main__':
    _tini_test(receive_args())
    