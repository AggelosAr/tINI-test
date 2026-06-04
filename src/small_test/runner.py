from time import perf_counter
from typing import Optional

from .enums import Mode
from .misc.annotations import TimeTakenForTestDiscoveryAndSuiteInitialization
from .misc.exceptions import TestNotFound
from .module_collector import ModuleCollector
from .test_suite import TestsContainer, TestSuite


def get_test_container(mode: Optional[str | Mode] = None,
                       search_dir: Optional[str] = None, 
                       search_file: Optional[str] = None, 
                       test_function: Optional[str] = None) -> tuple[TestsContainer, 
                                                                     TimeTakenForTestDiscoveryAndSuiteInitialization]:


    test_collector = ModuleCollector(search_dir, search_file)
    test_collector.walk_and_collect_test_files(test_collector.root)
    test_collector.normalize_collected_data()

    tests_container: TestsContainer = {}
    found_test = False

    _start = perf_counter()

    for module, test_files in test_collector.test_modules.items():
        
        if module not in tests_container:
            tests_container[module] = {}

        for test_file in test_files:
            
            if found_test:
                break
            
            suite = TestSuite(module, test_file, mode)
            collected_tests = suite.gather_tests(func_name=test_function)
        
            if not collected_tests:
                continue

            found_test |= test_function in collected_tests
            
            if test_function and not found_test:
                continue
            
            tests_container[module][test_file] = suite
            
        if not len(tests_container[module]):
            del tests_container[module]


    if test_function and not found_test:
        raise TestNotFound
   
    
    return tests_container, perf_counter() - _start


def run_tests(collection_time: TimeTakenForTestDiscoveryAndSuiteInitialization, 
              tests_container: TestsContainer) -> None:
    
    total_time = 0.0
    total_tests = 0

    total_successes = 0
    total_failures = 0

    for _, test_files in tests_container.items():
        
        for _, suite in test_files.items():

            module_test_duration, failures = suite.run_tests()

            print('Run Tests in module in (%f) secs.' % (module_test_duration, ))

            total_time += module_test_duration
            total_tests += suite.total_tests

            total_successes += suite.total_tests - failures
            total_failures += failures


    # TODO add a box function here.
    print('\n\n') 
    print('------------------------------------------')

    print('| Total Tests         : %d' % (total_tests, ))

    print('|')
    print('| Total successes     : %d' % (total_successes, ))
    print('| Total failures      : %d' % (total_failures, ))
    print('|')

    print('| Collected Tests in  : (%0.4f) secs' % (collection_time, ))
    print('| Run Tests in        : (%0.4f) secs' % (total_time, ))

    print('------------------------------------------')
