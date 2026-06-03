from small_test.test_suite import Test


@Test.case
def test_decorator_works_no_parenthesis() -> None:
    ...



@Test.case()
def test_decorator_works_with_parenthesis() -> None:
    ...
