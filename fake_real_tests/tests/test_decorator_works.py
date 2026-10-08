from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          run_test)
from tini_test.must_equals import must_equal
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


@Test.case(setup, lambda: cleanup())
def test_database_mix() -> None:
    ...



@Test.case
def test_arguments_should_be_callables() -> None:
    names = ['case1', 'case2', 'case3']
    tests = ['''

@Test.case(1)
def case1(): ...

''',
'''

@Test.case(1, 2)
def case2(): ...

''',

'''

@Test.case(lambda: 100, '2')
def case3(): ...

'''
]
    err = 'tini_test.misc.exceptions.TestArgumentsShouldBeCallables: Test received as argument(s) not callable(s)'

    for test_name, test in zip(names, tests):

        _ = get_temp_file(test, test_name)
        completed_process = run_test(test_name, test_name)

        must_equal(1, completed_process.returncode)

        search_line = None
        for line in completed_process.stderr.splitlines():
            if 'tini_test.misc.exceptions.TestArgumentsShouldBeCallables:' in line: 
                search_line = line
        
        must_equal(err, search_line)

        delete_test_dir(test_name)
