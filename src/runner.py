from collections import defaultdict
from typing import Optional

from src.enums import Mode
from src.misc.exceptions import TestFunctionNotFound
from src.module_collector import ModuleCollector
from src.utils import TestSuite, TestsContainer


def collect_tests(mode: Optional[str | Mode]=None,
                  search_dir: Optional[str]=None, 
                  search_file: Optional[str]=None, 
                  search_test_function: Optional[str]=None) -> TestsContainer:

    test_collector = ModuleCollector(search_dir=search_dir,
                                     search_file=search_file)
   
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_test_modules()

    tests_container: TestsContainer = {}

    found_specific_test = False

    for module, test_files in test_collector.test_modules.items():
        
        if module not in tests_container:
            tests_container[module] = {}

        # TODO run multiple test_files in the same time. what about modules? what about the collector in the test file?
        for test_file in test_files:
            
            # if 'test_cleanup_works_on_fail' != test_file:
            #     continue

            full_module_name = '%s.%s' % (module, test_file, )

            suite = TestSuite(module=full_module_name,
                              mode=mode)

            
            suite.gather_tests()


            if search_test_function:
                
                if search_test_function in suite.gathered_test_names:
                    suite.filter_tests(test_name=search_test_function)

                    if suite.decorated_tests:
                        found_specific_test = True
                        tests_container[module][test_file] = suite

            else:

                tests_container[module][test_file] = suite
    

    if search_test_function and not found_specific_test:
        raise TestFunctionNotFound
    
    # cleanup tests_container maybe implement it using defaultdict
    for module in list(tests_container.keys()):
        if not len(tests_container[module]):
            del tests_container[module]

    return tests_container


def run_tests(tests_container: TestsContainer) -> None:
    
    for module, test_files in tests_container.items():

        for test_file, test_suite in test_files.items():

            test_suite.run_tests()
