from collections import defaultdict
from typing import Optional

from src.enums import Mode
from src.misc.annotations import TestsContainer
from src.misc.exceptions import TestFunctionNotFound
from src.module_collector import ModuleCollector
from src.utils import TestSuite


def collect_tests(mode: str | Mode,
                  search_dir: Optional[str], 
                  search_file: Optional[str], 
                  search_test_function: Optional[str]) -> TestsContainer:

    test_collector = ModuleCollector(search_dir=search_dir,
                                     search_file=search_file)
   
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_test_modules()

    tests_container: TestsContainer = defaultdict(lambda: defaultdict(lambda: TestSuite))

    found_specific_test = False

    for module, test_files in test_collector.test_modules.items():
        

        # TODO run multiple test_files in the same time. what about modules? what about the collector in the test file?
        for test_file in test_files:
            
            # if 'test_cleanup_works_on_fail' != test_file:
            #     continue

            full_module_name = '%s.%s' % (module, test_file, )

            suite = TestSuite(module=full_module_name,
                              mode=mode)

            suite.gather_tests()

            
            if search_test_function:

                if search_test_function in suite.gathered_tests:
                    suite.filter_tests(test_name=search_test_function)

                    if suite.decorated_tests:
                        found_specific_test = True
                        tests_container[module][test_file] = suite

            else:

                tests_container[module][test_file] = suite
    

    if search_test_function and not found_specific_test:
        raise TestFunctionNotFound
    
    return tests_container


def run_tests(tests_container: TestsContainer) -> None:
    
    for module, test_files in tests_container.items():

        for test_file, test_suite in test_files.items():

            test_suite.run_tests()
