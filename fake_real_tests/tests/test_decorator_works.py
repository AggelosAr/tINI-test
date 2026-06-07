from tini_test.test import Test


def setup():
    print('SETUP CALLED')

def cleanup():
    print('CLEANUP CALLED')



@Test.case
def test_decorator_works_no_parenthesis() -> None:
    ...



@Test.case()
def test_decorator_works_with_parenthesis() -> None:
    ...


# #################################
# #### POSITIONAL
# #################################


@Test.case(setup = setup, cleanup = cleanup)
def test_setup_provided_pos_r() -> None:
    ...



@Test.case(setup = lambda: setup(), cleanup = lambda: cleanup())
def test_setup_provided_pos_r_l() -> None:
    ...


# #################################
# #### KEYWORD
# #################################


@Test.case(setup, cleanup)
def test_setup_provided_key_r() -> None:
    ...



@Test.case(lambda: setup(), lambda: cleanup())
def test_setup_provided_key_r_l() -> None:
    ...


# #############################################
# #### test both positional and keyword works
# #############################################


@Test.case(setup, cleanup=cleanup)
def test_setup_provided_key_p_k() -> None:
    ...
