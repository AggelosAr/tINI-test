from src.must_equals import must_equal
from src.test_utils import Test


@Test.case
def test_must_equal_frozen_set_passes() -> None:

    s = frozenset({1, 2, 3})
    t = frozenset({1, 2, 3})

    must_equal(s, t)



@Test.case
def test_must_equal_type_none() -> None:

    s = type(None)
    t = type(None)
    
    must_equal(s, t)
