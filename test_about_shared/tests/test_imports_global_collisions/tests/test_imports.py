from tini_test import NotInitialized, Shared, Test, WillRaise, must_equal, var


@Shared(var.X)
@Test.case
def test_imports_example():
    ...