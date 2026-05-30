from src.arg_parser import recieve_args
from src.misc.exceptions import (CantFindRelativePathToRoot, NotSupportedMode,
                                 TestNotFound,
                                 TooManyArgumentsGivenDirAndFile)
from src.runner import get_test_container, run_tests

if __name__=='__main__':

    mode, search_dir, search_file, search_test_function = recieve_args()

    try:
        tests_container = get_test_container(mode,
                                             search_dir,
                                             search_file,
                                             search_test_function)
    except TooManyArgumentsGivenDirAndFile:
        raise
    except CantFindRelativePathToRoot:
        raise
    except NotSupportedMode:
        raise
    except TestNotFound:
        raise
    else:
        run_tests(tests_container)
    finally:
        ...
