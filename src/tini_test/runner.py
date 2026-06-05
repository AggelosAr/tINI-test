import asyncio
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
            
            # TODO add failures
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


async def arun_tests(collection_time: TimeTakenForTestDiscoveryAndSuiteInitialization, 
                     tests_container: TestsContainer) -> None:
    
    print()
    
    _start = perf_counter()
    
    # Gather all suites from all modules
    all_suites: list[TestSuite] = []
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


def run_tests(collection_time: TimeTakenForTestDiscoveryAndSuiteInitialization, 
              tests_container: TestsContainer) -> None:
    
    asyncio.run(arun_tests(collection_time, tests_container))
