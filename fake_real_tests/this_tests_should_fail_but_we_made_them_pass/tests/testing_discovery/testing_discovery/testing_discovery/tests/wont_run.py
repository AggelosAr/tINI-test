
from tini_test.test import Test


@Test.case
def also_wont_run() -> None:

    print('also wont run')
    1/0
