from src.arg_parser import argument_parser
from src.misc.exceptions import (CantFindRelativePathToRoot, NotSupportedMode,
                                 TestFunctionNotFound,
                                 TooManyArgumentsDirAndFile)
from src.runner import collect_tests, run_tests

if __name__=='__main__':

    mode, search_dir, search_file, search_test_function = argument_parser()

    try:
        tests_container = collect_tests(mode=mode,
                                        search_dir=search_dir,
                                        search_file=search_file,
                                        search_test_function=search_test_function)
    # TODO see command line behaviour
    except TooManyArgumentsDirAndFile:
        ...
    except CantFindRelativePathToRoot:
        ...
    except NotSupportedMode:
        ...
    except TestFunctionNotFound:
        ...
    else:
        run_tests(tests_container)
    finally:
        ...
