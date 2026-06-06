from tini_test.enums import RunMode

from .arg_parser import receive_args
from .misc.exceptions import CantFindRelativePathToRoot, TestNotFound
from .runner import arun_tests, get_test_container, run_tests

if __name__=='__main__':

    run_mode, verbosity, search_dir, file_name, test_function = receive_args()

    try:
        tests_container, time = get_test_container(verbosity,
                                                   search_dir,
                                                   file_name,
                                                   test_function)
    except CantFindRelativePathToRoot:
        raise
    except TestNotFound:
        raise
    else:
        match run_mode:
            case RunMode.SYNC:
                run_tests(time, tests_container)
            case RunMode.ASYNC:
                arun_tests(time, tests_container)
    finally:
        ...
