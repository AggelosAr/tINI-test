from tini_test import Test


def setup() -> int:
    return 1


def cleanup() -> int:
    return 1

@Test.case(setup=setup)
def test_setup_returns() -> int:
    return 10


@Test.case(cleanup=cleanup)
def test_cleanup_returns() -> int:
    return 10


@Test.case(setup=setup, cleanup=cleanup)
def test_setup_cleanup_returns() -> int:
    return 10
