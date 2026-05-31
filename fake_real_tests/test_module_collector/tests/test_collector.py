from src.asserts import WillRaise
from src.misc.exceptions import (CantFindRelativePathToRoot, TestNotFound,
                                 TooManyArgumentsGivenDirAndFile)
from src.module_collector import ModuleCollector
from src.runner import get_test_container
from src.test_suite import Test

# Recursion indeed stops early when searching for file. maybe add a test.
# !
 

@Test.case
def test_collector_collects_all():
    test_collector = ModuleCollector()
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()


    correct_items = {'fake_real_tests.test_module_collector.tests': ['test_collector'], 
                     'fake_real_tests.test_dir.tests': ['test_smth'], 
                     'fake_real_tests.this_tests_should_fail.tests': ['test_fails', 
                                                                      'test_cleanup_works_on_fail', 
                                                                      'test_broken_test'], 
                     'fake_real_tests.tests': ['test_decorator_works', 
                                               'test_will_raise', 
                                               'test_db_setup_cleanup', 
                                               'test_setup', 
                                               'test_cleanup'],
                     'tests': []}
    assert correct_items == dict(test_collector.test_modules.items())



@Test.case
def test_collector_bad_initialiazation():
    with WillRaise(TooManyArgumentsGivenDirAndFile) as context:
        _ = ModuleCollector(search_dir='.', search_file='.')
  


@Test.case
def test_collector_can_find_correct_dir_from_search_dir():
    test_collector = ModuleCollector(search_dir='this_tests_should_fail/tests')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()

    correct_items = {'fake_real_tests.this_tests_should_fail.tests': 
                     ['test_fails', 
                      'test_cleanup_works_on_fail', 
                      'test_broken_test']}
    assert correct_items == dict(test_collector.test_modules.items())



@Test.case
def test_collector_will_not_find_tests_from_wrong_search_dir():
    with WillRaise(CantFindRelativePathToRoot):
        test_collector = ModuleCollector(search_dir='doesnt_exist/dir2')



@Test.case
def test_collector_finds_correct_file_without_extension():
    test_collector = ModuleCollector(search_file='test_fails')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()
    
    correct_items = {'fake_real_tests.this_tests_should_fail.tests': ['test_fails']}
    assert correct_items == dict(test_collector.test_modules.items())



@Test.case
def test_collector_finds_correct_file_with_extension():
    test_collector = ModuleCollector(search_file='test_fails.py')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()

    correct_items = {'fake_real_tests.this_tests_should_fail.tests': ['test_fails']}
    assert correct_items == dict(test_collector.test_modules.items())



@Test.case
def test_collector_will_not_find_anything_if_nonexisting_file_is_requested():
    test_collector = ModuleCollector(search_file='file_that_is_not_here')
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_collected_data()
    
    correct_items = {}
    assert correct_items == dict(test_collector.test_modules.items())



@Test.case
def test_test_module_will_not_collect_a_single_function_if_it_doesnt_exist():
    with WillRaise(TestNotFound):
        _ = get_test_container(test_function='file_that_is_not_here')



# TODO maybe update
@Test.case
def test_test_module_will_collect_a_single_function():
    tests_container = get_test_container(test_function='test_decorator_works_with_parenthesis')

    correct_item = 'test_decorator_works_with_parenthesis'

    assert len(tests_container) == 1
    assert len(tests_container['fake_real_tests.tests']) == 1

    module_tests = tests_container['fake_real_tests.tests']['test_decorator_works']
    gathered_tests = module_tests.decorated_tests

    
    assert len(gathered_tests) == 1
    assert correct_item == gathered_tests[0].func.__closure__[-1].cell_contents.__name__



# TODO maybe update
@Test.case
def test_test_module_will_collect_this_function():

    t = 'test_test_module_will_collect_this_function'
    tests_container = get_test_container(test_function=t)

    assert len(tests_container['fake_real_tests.test_module_collector.tests']) == 1

    module_tests = tests_container['fake_real_tests.test_module_collector.tests']['test_collector']
    gathered_tests = module_tests.decorated_tests

    assert len(gathered_tests) == 1
    assert t == gathered_tests[0].func.__closure__[-1].cell_contents.__name__
