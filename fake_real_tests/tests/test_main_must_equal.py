from src.must_equals import must_equal
from src.test_utils import Test


@Test.case
def test_tuple_size_dont_match() -> None:
    must_equal((1, 2), (1, 2, 3))


@Test.case
def test_tuple_value_dont_match() -> None:
    must_equal((1, 2, 3), (1, 4, 3))


@Test.case
def test_list_size_dont_match() -> None:
    must_equal([1, 2], [1, 2, 3])


@Test.case
def test_list_value_dont_match() -> None:
    must_equal([1, 2, 3], [1, 4, 3])


@Test.case
def test_multiline_string_diff() -> None:
    must_equal(
            'hello\nworld\nfoo',
            'hello\nthere\nfoo',
        )


@Test.case
def test_dict_value_dont_match() -> None:
    must_equal(
            {'a': 1, 'b': 2},
            {'a': 1, 'b': 3},
        )


@Test.case
def test_dict_value_dont_match_case() -> None:
    a = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    b = 'RRRRRRRRRRRRRRRRRRRRRRRsadasdasdasd'

    must_equal(a,  b)


@Test.case
def test_equal_tuple_passes() -> None:
    must_equal((1, 2, 3), (1, 2, 3))


@Test.case
def test_equal_multiline_string_passes() -> None:
    must_equal(
        'a\nb\nc',
        'a\nb\nc',
    )