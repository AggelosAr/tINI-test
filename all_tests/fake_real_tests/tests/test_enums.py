from tini_test import Test, WillRaise, must_equal
from tini_test.enums import RunMode, Verbosity
from tini_test.misc.exceptions import (NotSupportedRunMode,
                                       NotSupportedVerbosity)


@Test.case
def test_bad_run_mode():
    
    with WillRaise(NotSupportedRunMode) as context:
        r = RunMode.arg_parser_type('X')

    must_equal(True, 'Supported run modes are'  in str(context.exception))
    


@Test.case
def test_bad_verbosity():

    with WillRaise(NotSupportedVerbosity) as context:
        r = Verbosity.arg_parser_type('Y')

    must_equal(True, 'Supported verbosity modes are ' in str(context.exception))
