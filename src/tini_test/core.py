import asyncio
from functools import cached_property
from time import perf_counter
from typing import Optional

from tini_test.enums import RunMode, Verbosity
from tini_test.misc.annotations import (Errors, Failures, Successes, SuiteSize,
                                        TestCollectionSize, TestFunctionName,
                                        TimeTakenForSuiteInitialization,
                                        TimeTakenForTestCollection,
                                        TimeTakenForTestDiscovery,
                                        TimeTakenToRunSuite)
from tini_test.misc.exceptions import TestNotFound
from tini_test.module_collector import ModuleCollector
from tini_test.test import TestCollection

# TODO create timed class


# class TestGenerator:

#     def __init__(self, container: dict[DirectoryPath, dict[FileName, Tests]])

#         self.container = container

#     def __iter__(self) -> Iterator[tuple[DirectoryPath, FileName]]:
#         for _, test_files in self.container.items():
#             for _, suite in test_files.items():
#                 yield 



class TestSuite:
    
    def __init__(self,
                 run_mode: RunMode,
                 verbosity: Verbosity,
                 test_function: Optional[TestFunctionName] = None
                 ) -> None:
        
        self.run_mode = run_mode
        self.verbosity = verbosity
        self.test_function = test_function

        self._discovery_time = 0.0
        self._start = perf_counter()
        self._init_time = 0.0
        self._suite_run_time = 0.0

        self._total_tests = 0
        self._successes = 0
        self._errors = 0
        self._failures = 0

        self.container = {}

    def __str__(self) -> str:
        raise NotImplementedError

    @cached_property
    def searching_single_test(self) -> bool:
        return self.test_function is not None
    
    @property
    def discovery_time(self) -> TimeTakenForTestDiscovery:
        return self._discovery_time

    @discovery_time.setter
    def discovery_time(self, dt: TimeTakenForTestDiscovery) -> None:
        self._discovery_time = dt

    @property
    def suite_init_time(self) -> TimeTakenForSuiteInitialization:
        return self._init_time

    @suite_init_time.setter
    def suite_init_time(self, dt: TimeTakenForSuiteInitialization) -> None:
        self._init_time = dt - self._start

    @property
    def total_tests(self) -> SuiteSize:
        return self._total_tests
    
    @total_tests.setter
    def total_tests(self, test_collection_size: TestCollectionSize) -> None:
        self._total_tests += test_collection_size

    @property
    def successes(self) -> Successes:
        return self._successes
    
    @successes.setter
    def successes(self, new_successes: Successes) -> None:
        self._successes += new_successes
        
    @property
    def errors(self) -> Errors:
        return self._errors
    
    @errors.setter
    def errors(self, new_errors: Errors) -> None:
        self._errors += new_errors

    @property
    def failures(self) -> Failures:
        return self._failures
    
    @failures.setter
    def failures(self, new_failures) -> None:
        self._failures += new_failures

    @property
    def suite_run_time(self) -> TimeTakenToRunSuite:
        return self._suite_run_time

    @suite_run_time.setter
    def suite_run_time(self, dt: TimeTakenToRunSuite) -> None:
        self._suite_run_time = dt - self._start

    def pprint_summary(self) -> None:
        print(self.get_summary())

    def get_summary(self) -> str:
        
        return '\n'.join([
        '\n'
        ' ------------------------------------------',
        '| Total registered tests  : %d' % (self.total_tests, ),
        '|',
        '| Total successes         : %d' % (self.successes, ),
        '| Total errors            : %d' % (self.errors, ),
        '| Total failures          : %d' % (self.failures, ),
        '|',
        '| Discovered Tests in     : ( %0.4f ) secs' % (self.discovery_time, ),
        '| Initialized Suite in    : ( %0.4f ) secs' % (self.suite_init_time, ),
        '| Run Tests in            : ( %0.4f ) secs' % (self.suite_run_time, ),
        ' ------------------------------------------'
        ])

    def initialize_tests(self, _from: ModuleCollector) -> None:
        
        self.discovery_time = _from.discovery_time

        for module_path, test_file in _from:
            
            # TODO do we need to try/catch here?
            tests = TestCollection(verbosity=self.verbosity, 
                                   module_path=module_path,
                                   file=test_file)
            
            collected_tests = tests.gather_tests(func_name=self.test_function)

            if not collected_tests:
                continue
            
            full_path = '%s.%s' % (module_path, test_file, )

            if self.searching_single_test:

                if self.test_function in collected_tests:

                    self.container[full_path] = tests
                    break
            
            self.container[full_path] = tests

        if self.searching_single_test and not self.container:
            raise TestNotFound

    def run_suite(self) -> None:
        
        for _f_path, test_collection in self.container.items():
            
            current_errors = test_collection.run_tests()
        
            self.suite_run_time = perf_counter()

            current_tests = test_collection.total_tests
            current_successes = current_tests - current_errors
            current_failures = current_tests - current_successes - current_errors

            self.total_tests = current_tests
            self.successes = current_successes
            self.errors = current_errors
            self.failures = current_failures

    async def _arun_suite(self) -> None:
        print()
        
        # Gather all suites from all modules
        all_test_collections: list[TestCollection] = []
        for _f_path, test_collection in self.container.items():
            all_test_collections.append(test_collection)
        
        # Run all suites concurrently # TODO what do we do with exceptions here ?
        results = await asyncio.gather(
            *[test_collection.arun_tests() for test_collection in all_test_collections],
            return_exceptions=False
        )

        for test_collection, current_errors in zip(all_test_collections, results):
            
            current_tests = test_collection.total_tests
            current_successes = current_tests - current_errors
            current_failures = current_tests - current_successes - current_errors

            self.total_tests = current_tests
            self.successes = current_successes
            self.errors = current_errors
            self.failures = current_failures
    
    def arun_suite(self) -> None:
        asyncio.run(self._arun_suite())

    def runner(self) -> None:

        self._start = perf_counter()

        match self.run_mode:

            case RunMode.SYNC:
                self.run_suite()

            case RunMode.ASYNC:
                
                self.arun_suite()

        self.suite_run_time = perf_counter()
