from time import perf_counter
from typing import Optional

from small_test.enums import Mode
from small_test.misc.annotations import \
    TimeTakenForTestDiscoveryAndSuiteInitialization
from small_test.misc.exceptions import TestNotFound
from small_test.module_collector import ModuleCollector
from small_test.test_suite import TestsContainer, TestSuite


def get_test_container(mode: Optional[str | Mode] = None,
                       search_dir: Optional[str] = None, 
                       search_file: Optional[str] = None, 
                       test_function: Optional[str] = None) -> tuple[TestsContainer, 
                                                                     TimeTakenForTestDiscoveryAndSuiteInitialization]:


    # mode = 'SORT'
    # mode = 'SUPER_MINIMAL'

    # search_dir = 'test_must_equals'
    # search_file = 'test_must_equal_works' # custom compartor n diff problem of repr
    # test_function = 'test_must_equal_type_case_different'
    # search_file = 'test_must_equal_strings'


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
            
            #try:
            suite = TestSuite(module, test_file, mode)
            collected_tests = suite.gather_tests(func_name=test_function)
            #except ImportError:
            #    continue # if the python is broken this will fail in case the mode is set to seach for single files
            

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

            print('Run Tests in module %f' % (module_test_duration, ))

            total_time += module_test_duration
            total_tests += suite.total_tests

            total_successes += suite.total_tests - failures
            total_failures += failures
            
    print()

    print('Total Tests         : %d' % (total_tests, ))

    print('Total successes     : %d' % (total_successes, ))
    print('Total failures      : %d' % (total_failures, ))

    print('Collected Tests in  : %f' % (collection_time, ))
    print('Run Tests in        : %f' % (total_time, ))

    print()
