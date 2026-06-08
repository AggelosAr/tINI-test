from tini_test.test import Test


@Test.case
def wont_run() -> None:

    print('wont run')
    1/0
