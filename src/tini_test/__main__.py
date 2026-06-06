from .arg_parser import receive_args
from .initializer import initialize_test_suite
from .misc.exceptions import CantFindRelativePathToRoot, TestNotFound

if __name__=='__main__':

    try:
        test_suite = initialize_test_suite(**receive_args())
         
    except CantFindRelativePathToRoot:
        raise

    except TestNotFound:
        raise

    else:
        test_suite.runner()

    finally:
        test_suite.pprint_summary()
