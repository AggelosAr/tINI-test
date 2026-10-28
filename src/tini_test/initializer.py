import os
from time import perf_counter
from typing import Optional

from tini_test._internals.consts import _ROOT
from tini_test.core import TestSuite
from tini_test.enums import Coverage, RunMode, Verbosity
from tini_test.misc.annotations import (DirectoryPath, FileName,
                                        TestFunctionName)
from tini_test.module_collector import ModuleCollector


def initialize_test_suite(run_mode: RunMode,
                          verbosity: Verbosity,
                          coverage: Coverage,
                          coverage_target: DirectoryPath | FileName | None,
                          store_coverage_at: DirectoryPath | FileName | None,
                          search_dir: DirectoryPath,
                          file_name: Optional[FileName] = None, 
                          test_function: Optional[TestFunctionName] = None
                          ) -> TestSuite:
    
    test_collector = ModuleCollector(search_dir, file_name)

    test_collector.walk_and_collect_test_files(test_collector.root)
    test_collector.normalize_collected_data()
    test_collector.discovery_time = perf_counter()

    _ROOT[0] = search_dir if search_dir != '.' else os.getcwd()

    test_suite = TestSuite(root=_ROOT[0],
                           run_mode=run_mode,
                           verbosity=verbosity,
                           coverage=coverage,
                           coverage_target=coverage_target,
                           store_coverage_at=store_coverage_at,
                           test_function=test_function)
    
    test_suite.initialize_tests(_from=test_collector)
    test_suite.suite_init_time = perf_counter()

    return test_suite
