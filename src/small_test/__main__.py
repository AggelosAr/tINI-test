from ._internals._internal_exceptions._exceptions import (_FailStateWasNotFail,
                                                          _LastOpNotExpected)
from .arg_parser import receive_args
from .misc.exceptions import (CantFindRelativePathToRoot, NotSupportedMode,
                              TestNotFound)
from .runner import get_test_container, run_tests

if __name__=='__main__':

    mode, search_dir, search_file, search_test_function = receive_args()

    try:
        tests_container, time = get_test_container(mode,
                                                   search_dir,
                                                   search_file,
                                                   search_test_function)
    except CantFindRelativePathToRoot:
        raise
    except NotSupportedMode:
        raise
    except TestNotFound:
        raise
    except _FailStateWasNotFail: # TODO(**1**) This means something broke with small-test ? remove from here ?
        raise
    except _LastOpNotExpected: # TODO(**1**)
        raise
    else:
        run_tests(time, tests_container)
    finally:
        ...
