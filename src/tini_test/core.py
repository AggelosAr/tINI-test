import asyncio
import traceback
from functools import cached_property
from itertools import repeat
from time import perf_counter
from typing import Optional

from tini_test.enums import RunMode, Verbosity
from tini_test.misc.annotations import (DotPythonPath, Errors, FileFailReason,
                                        FileLoadFailures, FileName, Successes,
                                        SuiteSize, TestCollectionSize,
                                        TestFunctionName,
                                        TimeTakenForSuiteInitialization,
                                        TimeTakenForTestDiscovery,
                                        TimeTakenToRunSuite)
from tini_test.misc.exceptions import TestNotFound
from tini_test.module_collector import ModuleCollector
from tini_test.shared import MetaSharedVar
from tini_test.test import TestCollection


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

        self._file_load_failures = 0
        self._failed_to_collect_test_files: dict[FileName, FileFailReason] = {}

        self.container: dict[DotPythonPath, TestCollection] = {}

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
    def file_load_failures(self) -> FileLoadFailures:
        return self._file_load_failures
    
    @file_load_failures.setter
    def file_load_failures(self, new_failures: FileLoadFailures) -> None:
        self._file_load_failures += new_failures

    @property
    def suite_run_time(self) -> TimeTakenToRunSuite:
        return self._suite_run_time

    @suite_run_time.setter
    def suite_run_time(self, dt: TimeTakenToRunSuite) -> None:
        self._suite_run_time = dt - self._start

    @property
    def failed_to_collect_test_files_reasons(self) -> dict[FileName, FileFailReason]:
        return self._failed_to_collect_test_files

    @failed_to_collect_test_files_reasons.setter
    def failed_to_collect_test_files_reasons(self, new_file: FileName, reason: FileFailReason) -> None:
        self._failed_to_collect_test_files[new_file] = reason

    def format_file_failure_traceback(self, tb: str) -> str:
        # Crop all lines involving importlib
        lines = tb.splitlines()
        i = 0
        for i in range(len(lines) - 1, -1, -1):
            if 'importlib' in lines[i]:
                if i < len(lines) - 1:
                    i += 1
                break

        return '\n'.join(lines[i:])

    def update_summary_stats(self, total_tests: TestCollectionSize, new_errors: Errors) -> None:
        current_tests = total_tests
        current_successes = current_tests - new_errors
        current_file_load_failures = current_tests - current_successes - new_errors

        self.total_tests = current_tests
        self.successes = current_successes
        self.errors = new_errors
        self.file_load_failures = current_file_load_failures

    def pprint(self) -> None:
        print(self.get_summary())

    def get_summary(self) -> str:
        _r = [
            '\n'
                ' ------------------------------------------',
                '| Total registered tests  : %d' % (self.total_tests, ),
                '|',
                '| Total successes         : %d' % (self.successes, ),
                '| Total errors            : %d' % (self.errors, ),
                '| Test file load failures : %d' % (self.file_load_failures, ),
                '|',
                '| Discovered Tests in     : ( %0.4f ) secs' % (self.discovery_time, ),
                '| Initialized Suite in    : ( %0.4f ) secs' % (self.suite_init_time, ),
                '| Run Tests in            : ( %0.4f ) secs' % (self.suite_run_time, ),
                ' ------------------------------------------', # <
                    '\n',
                    '\n',
                        'Test files failed to load (%d):\n\n%s'
                            % 
                            (
                                len(__r := self.failed_to_collect_test_files_reasons),
                                (
                                    '\n\n'\
                                    '%s\n'\
                                    '%s\n\n' 
                                        % 
                                        (
                                            ''.join(repeat('~', 40)), 
                                            ''.join(repeat('~', 40)), 
                                        )
                                ).join(
                                    '\t\t(%d). File: %s\n\n'\
                                    '\t\t\tReason: %s' 
                                        % 
                                        (
                                            idx, 
                                            file, 
                                            reason, 
                                        )
                                        for idx, (file, reason) in 
                                        enumerate(__r.items(), start=1)
                                    ),
                            ),
        ]

        return '\n'.join(_r if self.file_load_failures else _r[:-2]) 

    # XXX Async init of tests
    def initialize_tests(self, _from: ModuleCollector) -> None:
        self.discovery_time = _from.discovery_time

        # Used to give fail reason while searching for a single test file
        single_test_file = None

        shared_meta = MetaSharedVar.get_meta_var()

        for module_path, test_file in _from:

            tests = TestCollection(verbosity=self.verbosity, 
                                   module_path=module_path,
                                   file=test_file,
                                   shared_meta=shared_meta)
            
            try:
                tests._import()

                collected_tests = tests.gather_tests(func_name=self.test_function)

                tests.raise_for_globals()
                   
            except Exception as e:
                self.file_load_failures = 1
                tb = self.format_file_failure_traceback(traceback.format_exc())
                self.failed_to_collect_test_files_reasons[test_file] = '%s\n%s' % (str(e), tb, )
                single_test_file = test_file
                continue

            finally:
                tests.reset_shared_meta()

                if not tests.has_tests:
                    continue


            if self.searching_single_test:

                if self.test_function in collected_tests:

                    self.container[tests.dot_python_path] = tests
                    break
            
            self.container[tests.dot_python_path] = tests


        if self.searching_single_test and not self.container:
            # TODO while searching for a single test, provide more context in the fail reason.
            # Currently the get_summary is skipped.
            # Because the test may be found but it has an error
            # Also there is a case there is a failure in another file 
            # while collecting, as a result we also show the other failures
            # Is this possible to improve the fail reason further? (probably)
            fail_reason = ''
            if single_test_file:
                fail_reason = self.failed_to_collect_test_files_reasons[single_test_file]

            raise TestNotFound(extra_msg=fail_reason)

    def run_suite(self) -> None:
        for _, test_collection in self.container.items():

            current_errors = test_collection.run_tests()

            self.suite_run_time = perf_counter()
            self.update_summary_stats(total_tests=test_collection.total_tests, new_errors=current_errors)

    async def _arun_suite(self) -> None:
        # @ XXX 1
        
        all_test_collections: list[TestCollection] = []
        for _, test_collection in self.container.items():
            all_test_collections.append(test_collection)
        
        results = await asyncio.gather(
            *[test_collection.arun_tests() for test_collection in all_test_collections],
            return_exceptions=True
        )
        for test_collection, current_errors in zip(all_test_collections, results):
            self.update_summary_stats(total_tests=test_collection.total_tests, new_errors=current_errors)

    def runner(self) -> None:
        self._start = perf_counter()
        
        match self.run_mode:

            case RunMode.SYNC:
                self.run_suite()

            case RunMode.ASYNC:
                asyncio.run(self._arun_suite())

        self.suite_run_time = perf_counter()
