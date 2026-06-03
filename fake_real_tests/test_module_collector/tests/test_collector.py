from small_test.must_equals import must_equal
from src.small_test.context_manager import WillRaise
from src.small_test.misc.exceptions import (CantFindRelativePathToRoot,
                                            TestNotFound)
from src.small_test.module_collector import ModuleCollector
from src.small_test.runner import get_test_container
from src.small_test.test_suite import Test

# Recursion indeed stops early when searching for file. maybe add a test.
# !
 
# TODO update to test edge cases like . .. ./././. etc .....



@Test.case
def test_collector_collects_all() -> None:
    test_collector = ModuleCollector()
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()

    # print('------------------------------------------------')
    # print(dict(test_collector.test_modules.items()))
    # print('------------------------------------------------')

    correct_items = {'fake_real_tests.test_must_equals.tests': ['test_must_equal_lists', 
                                                                'test_must_equal_dicts', 
                                                                'test_must_equal_works', 
                                                                'test_must_equal_tuples', 
                                                                'test_must_equal_strings', 
                                                                'test_must_equal_sets', 
                                                                'test_must_equal_ints', 
                                                                'test_must_equal_bools', 
                                                                'test_must_equals_misc', 
                                                                'test_must_equal_floats'], 
                     'fake_real_tests.test_module_collector.tests': ['test_collector'], 
                     'fake_real_tests.test_dir.tests': ['test_smth'], 
                     'this_tests_should_fail_but_we_made_them_pass': ['test_fails', 
                                                                      'test_cleanup_works_on_fail', 
                                                                      'test_broken_test'], 
                     'fake_real_tests.tests': ['test_decorator_works', 
                                               'test_will_raise', 
                                               'test_internals_must_equal', 
                                               'test_db_setup_cleanup', 
                                               'test_setup', 
                                               'test_cleanup'], 
                     'tests': []}
    must_equal(correct_items, dict(test_collector.test_modules.items()))




@Test.case
def test_collector_collects_all_and_exclude_dir_works() -> None:
    test_collector = ModuleCollector(exclude_dir='this_tests_should_fail_but_we_made_them_pass')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()

    correct_items = {'fake_real_tests.test_must_equals.tests': ['test_must_equal_lists', 
                                                                'test_must_equal_dicts', 
                                                                'test_must_equal_works', 
                                                                'test_must_equal_tuples', 
                                                                'test_must_equal_strings', 
                                                                'test_must_equal_sets', 
                                                                'test_must_equal_ints', 
                                                                'test_must_equal_bools', 
                                                                'test_must_equals_misc', 
                                                                'test_must_equal_floats'], 
                     'fake_real_tests.test_module_collector.tests': ['test_collector'], 
                     'fake_real_tests.test_dir.tests': ['test_smth'], 
                     'fake_real_tests.tests': ['test_decorator_works', 
                                               'test_will_raise', 
                                               'test_internals_must_equal', 
                                               'test_db_setup_cleanup', 
                                               'test_setup', 
                                               'test_cleanup'], 
                     'tests': []}
    must_equal(correct_items, dict(test_collector.test_modules.items()))



@Test.case
def test_collector_can_find_correct_dir_from_search_dir() -> None:
    test_collector = ModuleCollector(search_dir='this_tests_should_fail/tests')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()

    correct_items = {'fake_real_tests.this_tests_should_fail.tests': 
                     ['test_fails', 
                      'test_cleanup_works_on_fail', 
                      'test_broken_test']}
    must_equal(correct_items, dict(test_collector.test_modules.items()))



@Test.case
def test_collector_will_not_find_tests_from_wrong_search_dir() -> None:
    with WillRaise(CantFindRelativePathToRoot):
        _ = ModuleCollector(search_dir='doesnt_exist/dir2')



@Test.case
def test_collector_finds_correct_file_without_extension() -> None:
    test_collector = ModuleCollector(search_file='test_fails')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()
    
    correct_items = {'fake_real_tests.this_tests_should_fail.tests': ['test_fails']}
    must_equal(correct_items, dict(test_collector.test_modules.items()))



@Test.case
def test_collector_finds_correct_file_with_extension() -> None:
    test_collector = ModuleCollector(search_file='test_fails.py')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()

    correct_items = {'fake_real_tests.this_tests_should_fail.tests': ['test_fails']}
    must_equal(correct_items, dict(test_collector.test_modules.items()))



@Test.case
def test_collector_will_not_find_anything_if_nonexisting_file_is_requested() -> None:
    test_collector = ModuleCollector(search_file='file_that_is_not_here')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()
    
    correct_items: dict = {}
    must_equal(correct_items, dict(test_collector.test_modules.items()))



@Test.case
def test_test_module_will_not_collect_a_single_function_if_it_doesnt_exist() -> None:
    with WillRaise(TestNotFound):
        _ = get_test_container(test_function='file_that_is_not_here')



@Test.case
def test_test_module_will_collect_a_single_function() -> None:
    tests_container = get_test_container(test_function='test_decorator_works_with_parenthesis')

    correct_item = 'test_decorator_works_with_parenthesis'

    must_equal(True, tests_container[1] < 1)

    module_tests = tests_container[0]['fake_real_tests.tests']['test_decorator_works']
    gathered_tests = module_tests.decorated_tests

    
    must_equal(1, len(gathered_tests))
    must_equal(correct_item, gathered_tests[0].func.__closure__[-1].cell_contents.__name__) # type: ignore[attr-defined]



@Test.case
def test_test_module_will_collect_this_function() -> None:

    t = 'test_test_module_will_collect_this_function'
    tests_container, _ = get_test_container(test_function=t)

    must_equal(1, len(tests_container['fake_real_tests.test_module_collector.tests']))

    module_tests = tests_container['fake_real_tests.test_module_collector.tests']['test_collector']
    gathered_tests = module_tests.decorated_tests

    must_equal(1, len(gathered_tests))
    must_equal(t, gathered_tests[0].func.__closure__[-1].cell_contents.__name__) # type: ignore[attr-defined]
