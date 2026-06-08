from tini_test.test_utils import Test


@Test.case
def passes_good_bad() -> None:
    ...



@Test.case
def passes_bad_snakes() -> None:
    ...



1/0



@Test.case
def passes_good() -> None:
    ...



@Test.case
def passes_bad() -> None:
    ...

