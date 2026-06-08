from fake_real_tests.tests.test_db_setup_cleanup import (_cleanup_test_db,
                                                         _create_test_db)
from tini_test.test_utils import Test


@Test.case(
    setup=lambda: 1/0,
    cleanup=lambda: _cleanup_test_db("db_transaction_P")
)
def test_db_transaction_rollback_setup_fails() -> None:
    """Test database transaction and rollback behavior."""
    ...



@Test.case(
    setup=lambda: _create_test_db("db_transaction_P"),
    cleanup=lambda: _cleanup_test_db("db_transaction_P")
)
def test_db_transaction_rollback_main_fails() -> None:
    1/0



@Test.case(
    setup=lambda: _create_test_db("db_transaction_P"),
    cleanup=lambda: 1/0
)
def test_db_transaction_cleanup_fails() -> None:
    ...



@Test.case(
    setup=lambda: 1,
    cleanup=lambda: 1,
    _no_op=lambda: 1
)
def test_no_op() -> None:
    ...



@Test.case
def passes() -> None:
    ...
