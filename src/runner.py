from typing import Optional

from src.enums import Mode
from src.misc.exceptions import TestNotFound
from src.module_collector import ModuleCollector
from src.test_suite import TestsContainer, TestSuite


def get_test_container(mode: Optional[str | Mode] = None,
                       search_dir: Optional[str] = None, 
                       search_file: Optional[str] = None, 
                       test_function: Optional[str] = None) -> TestsContainer:

    search_dir = None
    #search_file = 'test_must_equal'
    mode = 'MINIMAL_NO_STACK'
    #mode = 'SORT'
    #test_function = 'test_dict_key_mismatch'

    #test_function = 'test_will_raise_fails_to_catch_exception'


    test_collector = ModuleCollector(search_dir, search_file)
    test_collector.walk_and_collect_test_files(test_collector.root)
    test_collector.normalize_collected_data()

    tests_container: TestsContainer = {}
    found_test = False


    for module, test_files in test_collector.test_modules.items():
        
        if module not in tests_container:
            tests_container[module] = {}

        for test_file in test_files:
            
            if found_test:
                break

            suite = TestSuite(module, test_file, mode)

            found_test |= test_function in suite.gather_tests(func_name=test_function)
          
            if test_function and not found_test:
                continue
            
            tests_container[module][test_file] = suite
            
        if not len(tests_container[module]):
            del tests_container[module]


    if test_function and not found_test:
        raise TestNotFound
   
    return tests_container


def run_tests(tests_container: TestsContainer) -> None:
    
    for _, test_files in tests_container.items():
        
        for _, test_suite in test_files.items():

            test_suite.run_tests()
