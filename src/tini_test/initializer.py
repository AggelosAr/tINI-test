import os
from time import perf_counter
from typing import Optional

from tini_test._internals.consts import _INIT, Init
from tini_test.core import CoverageTracker, TestSuite
from tini_test.enums import Coverage, RunMode, Verbosity
from tini_test.integrations.server import ServerManager
from tini_test.misc.annotations import (DirectoryPath, FileName,
                                        TestFunctionName)
from tini_test.module_collector import ModuleCollector
from tini_test.test_utils import TestStep



def initialize_test_suite(run_mode: RunMode,
                          verbosity: Verbosity,
                          
                          coverage: Coverage,
                          coverage_target: DirectoryPath | FileName | None,
                          store_coverage_at: DirectoryPath | FileName | None,

                          search_dir: DirectoryPath,
                          file_name: Optional[FileName] = None, 
                          test_function: Optional[TestFunctionName] = None,

                          server_command: Optional[str] = None,
                          health_url: Optional[str] = None,
                          ) -> TestSuite:
    
    _INIT.append(Init(_ROOT=os.getcwd(), 
                      _ANCHOR_FRAME=hex(id(TestStep.run_step.__code__))))

    test_collector = ModuleCollector(search_dir, file_name)

    test_collector.walk_and_collect_test_files(test_collector.root)
    test_collector.normalize_collected_data()
    test_collector.discovery_time = perf_counter()


    coverage_tracker = CoverageTracker(source=coverage_target, 
                                       runtime_covered_lines=None,
                                       metadata_save_path=store_coverage_at)

    
    server = ServerManager(command=server_command, 
                           store_path=store_coverage_at,
                           health_url=health_url)

    
    test_suite = TestSuite(root=_INIT[0]._ROOT,
                           run_mode=run_mode,
                           verbosity=verbosity,
                           coverage=coverage,
                           coverage_tracker=coverage_tracker,
                           server=server,
                           test_function=test_function)
    
    test_suite.initialize_tests(_from=test_collector)
    test_suite.suite_init_time = perf_counter()

    return test_suite
