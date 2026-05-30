from typing import assert_never

from src.utils import Test


@Test.case
def test_broken_test_case_one():
    print('test_broken_test_case_one')
    1/0
    assert_never()



@Test.case
def test_broken_test_case_two():
    print('test_broken_test_case_two')
    ok
    assert_never()



def setup_breaks():
    print('setup_breaks---->This should print and fail the test')
    1/0

@Test.case(setup=lambda: setup_breaks())
def test_setup_breaks():
    print('test_setup_breaks---->This should never print')
    assert_never()



def cleanup_breaks():
    print('cleanup_breaks---->This should print and fail the test')
    1/0

@Test.case(cleanup=lambda: cleanup_breaks())
def test_cleanup_breaks():
    print('test_cleanup_breaks---->This should print and then the clean up will divide by zero')



def _cleanup_breaks():
    print('_cleanup_breaks---->This should never print')
    assert_never()

@Test.case(setup=lambda: setup_breaks(), 
           cleanup=lambda: _cleanup_breaks())
def test_cleanup_breaks_test_and_break_down_wont_run():
    print('---->This should never print')
    assert_never()



# @Test.case
# def test_sorting_works():
#     print('~~~~~~~~~~~~~~~~~~~~~~~~~')
#     ...
