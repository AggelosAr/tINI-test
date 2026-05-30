from src.test_suite import Test


@Test.case
def test_decorator_works_no_parenthesis():
    ...


@Test.case()
def test_decorator_works_with_parenthesis():
    ...
