
from tini_test.test_suite import Test


@Test.case
def also_wont_run() -> None:

    print('also wont run')
    1/0
