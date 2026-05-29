from src.utils import Test


@Test.case
def test_decorator_works_no_parenthesis():
    ...


@Test.case()
def test_decorator_works_with_parenthesis():
    ...
