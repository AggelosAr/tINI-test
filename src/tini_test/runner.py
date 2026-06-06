import asyncio
from time import perf_counter
from typing import Optional

from .enums import Verbosity
from .misc.annotations import (DirectoryPath, FileName, TestFunctionName,
                               TimeTakenForTestDiscoveryAndSuiteInitialization)
from .module_collector import ModuleCollector
from .test_suite import TestSuite, TestsContainer, Tests


def initialize_test_suite(verbosity: Verbosity,
                          search_dir: DirectoryPath, 
                          file_name: Optional[FileName] = None, 
                          test_function: Optional[TestFunctionName] = None
                          ) -> tuple[TestsContainer, 
                                     TimeTakenForTestDiscoveryAndSuiteInitialization]:


    test_collector = ModuleCollector(search_dir, file_name)
    test_collector.walk_and_collect_test_files(test_collector.root)
    test_collector.normalize_collected_data()


    _start = perf_counter()

    test_suite = TestSuite(verbosity=verbosity,
                           collected_modules=test_collector,
                           test_function=test_function)
    tests_container = test_suite.get_tests_container()
   
    
    return tests_container, perf_counter() - _start


def run_tests(collection_time: TimeTakenForTestDiscoveryAndSuiteInitialization, 
              tests_container: TestsContainer) -> None:
    
    print()
    
    total_time = 0.0
    total_tests = 0

    total_successes = 0
    total_errors = 0

    for _, test_files in tests_container.items():
        
        for _, suite in test_files.items():
            
            _start = perf_counter()
            
            errors = suite.run_tests()

            module_test_duration = perf_counter() - _start

            total_time += module_test_duration
            total_tests += suite.total_tests

            total_successes += suite.total_tests - errors
            total_errors += errors

        print('\n\n------------------------------------------')

        print('| Total Tests         : %d' % (total_tests, ))

        print('|')
        print('| Total successes     : %d' % (total_successes, ))
        print('| Total errors        : %d' % (total_errors, ))
        print('|')

        print('| Collected Tests in  : (%0.4f) secs' % (collection_time, ))
        print('| Run Tests in        : (%0.4f) secs' % (total_time, ))

        print('------------------------------------------')


def arun_tests(collection_time: TimeTakenForTestDiscoveryAndSuiteInitialization, 
               tests_container: TestsContainer) -> None:
    
    asyncio.run(_arun_tests(collection_time, tests_container))


async def _arun_tests(collection_time: TimeTakenForTestDiscoveryAndSuiteInitialization, 
                      tests_container: TestsContainer) -> None:
    
    print()
    
    _start = perf_counter()
    
    # Gather all suites from all modules
    all_suites: list[Tests] = []
    for _, test_files in tests_container.items():
        for _, suite in test_files.items():
            all_suites.append(suite)
    
    # Run all suites concurrently # TODO what do we do with exceptions here ?
    results = await asyncio.gather(
        *[suite.arun_suite() for suite in all_suites],
        return_exceptions=False
    )
    
    # Aggregate results
    total_time = perf_counter() - _start
    
    total_tests = 0
    total_successes, total_errors = 0, 0


    for suite, errors in zip(all_suites, results):
        total_tests += suite.total_tests
        total_successes += suite.total_tests - errors
        total_errors += errors

    print('\n\n------------------------------------------')

    print('| Total Tests         : %d' % (total_tests, ))

    print('|')
    print('| Total successes     : %d' % (total_successes, ))
    print('| Total errors        : %d' % (total_errors, ))
    print('|')

    print('| Collected Tests in  : (%0.4f) secs' % (collection_time, ))
    print('| Run Tests in        : (%0.4f) secs' % (total_time, ))

    print('------------------------------------------')