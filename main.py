from src.arg_parser import argument_parser
from src.misc.exceptions import (CantFindRelativePathToRoot, NotSupportedMode,
                                 TestFunctionNotFound,
                                 TooManyArgumentsDirAndFile)
from src.runner import collect_tests, run_tests

if __name__=='__main__':

    # mode, search_dir, search_file, search_test_function = argument_parser()

    search_dir = 'fake_real_tests/test_module_collector/tests'
    search_dir = ''
    search_file = 'test_cleanup_works_on_fail'
    search_test_function = 'test_cleanup_works_even_if_setup_fails_and_then_breaks'
    search_test_function = ''
    mode = 'NORMAL'


    try:
        tests_container = collect_tests(mode=mode,
                                        search_dir=search_dir,
                                        search_file=search_file,
                                        search_test_function=search_test_function)
    # TODO see command line behaviour
    except TooManyArgumentsDirAndFile:
        raise
    except CantFindRelativePathToRoot:
        raise
    except NotSupportedMode:
        raise
    except TestFunctionNotFound:
        raise
    else:
        run_tests(tests_container)
    finally:
        ...
