import io
import os
import subprocess
import sys
import tempfile
import threading
from contextlib import redirect_stdout
from time import perf_counter

from tini_test import Isolate, Test, must_equal
from tini_test.__main__ import _tini_test
from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          get_unique_folder_name, run_test)
from tini_test.context_managers import WillRaise, _ThreadLocalStdout
from tini_test.core import TestSuite
from tini_test.enums import Coverage, RunMode, Verbosity
from tini_test.initializer import initialize_test_suite
from tini_test.misc.exceptions import CantFindRelativePathToRoot
from tini_test.module_collector import ModuleCollector
from tini_test._internals.consts import PROJECT_ROOT

@Test.case
def test_suite_run() -> None:

    command = ('cd %s && python3 -m tini_test -d test_must_equals -r sync' 
               % (PROJECT_ROOT, ))

    completed_process = subprocess.run(command, 
                                       timeout=10, 
                                       text=True, 
                                       capture_output=True,
                                       shell=True)
    
    must_equal(0, completed_process.returncode)
    print(completed_process.returncode)
    print(completed_process.stderr)
    print(completed_process.stdout)
    print(completed_process.returncode)
    print(completed_process.stderr)

    #   -------------------------------------------------------
    # -------------------------------------------------------
    #   -------------------------------------------------------
    # -------------------------------------------------------
    #   -------------------------------------------------------




@Test.case
def crash_main() -> None:
    
    with WillRaise(CantFindRelativePathToRoot):
        _tini_test({'run_mode': RunMode.ASYNC,
                    'verbosity': Verbosity.MINIMAL,
                    'coverage': Coverage.DISABLED,
                    'coverage_target': None,
                    'store_coverage_at': None,
                    'search_dir': '././././where_is?',
                    'file_name': 'None',
                    'test_function': None})



@Isolate
@Test.case
def test_suite_run_solved_failing_tests_for_coverage() -> None:

    test_collector = ModuleCollector('.')
    test_collector.test_modules = {
        'fake_real_tests.DISABLED___this_tests_should_fail.DISABLED___tests':
        ['test_broken_test',
         'test_cleanup_works_on_fail',
         'test_db_cov',
         'test_fails',
         'test_must_equal_breaks',
         'test_fails_to_collect']
    }
    test_suite = TestSuite(run_mode=RunMode.ASYNC,
                           verbosity=Verbosity.NORMAL,
                           coverage=Coverage.DISABLED,
                           coverage_target=None,
                           store_coverage_at=None)
    
    test_suite.initialize_tests(_from=test_collector)
    test_suite.suite_init_time = perf_counter()
    
    print(test_suite.container)
    test_suite.runner()
    test_suite.pprint()

    
    must_equal(21, test_suite.total_tests)
    must_equal(2, test_suite.successes)
    must_equal(19, test_suite.errors)
    must_equal(1, test_suite.file_load_failures)

    
    lines = set(map(lambda l: l.strip(), list(dict.fromkeys(test_suite.get_summary().splitlines()))))

    conditions = [
        'Test files failed to load (1):',
        'test_fails_to_collect',
        'Reason: division by zero'
        ]
    for condition in conditions:
        at_least_some_part = False
        for line in lines:
            if condition in line:
                at_least_some_part = True

        must_equal(True, at_least_some_part)

            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------

    test_suite = TestSuite(run_mode=RunMode.SYNC,
                           verbosity=Verbosity.MINIMAL,
                           coverage=Coverage.DISABLED,
                           coverage_target=None,
                           store_coverage_at=None)
    
    test_suite.initialize_tests(_from=test_collector)
    test_suite.suite_init_time = perf_counter()
    
    print(test_suite.container)
    test_suite.runner()
    test_suite.pprint()

    must_equal(21, test_suite.total_tests)
    must_equal(2, test_suite.successes)
    must_equal(19, test_suite.errors)
    must_equal(1, test_suite.file_load_failures)

    lines = set(map(lambda l: l.strip(), list(dict.fromkeys(test_suite.get_summary().splitlines()))))
    conditions = [
        'Test files failed to load (1):',
        'test_fails_to_collect',
        'Reason: division by zero'
        ]
    for condition in conditions:
        at_least_some_part = False
        for line in lines:
            if condition in line:
                at_least_some_part = True

        must_equal(True, at_least_some_part)
        

            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------

    test_suite = TestSuite(run_mode=RunMode.SYNC,
                           verbosity=Verbosity.MINIMAL_NO_STACK,
                           coverage=Coverage.DISABLED,
                           coverage_target=None,
                           store_coverage_at=None)
    
    test_collector.test_modules['fake_real_tests.test_must_equals.tests'] = [
        'test_must_equal_bytes'
    ]

    test_suite.initialize_tests(_from=test_collector)
    test_suite.suite_init_time = perf_counter()
    
    print(test_suite.container)
    test_suite.runner()
    test_suite.pprint()

    must_equal(21+12, test_suite.total_tests)
    must_equal(2+12, test_suite.successes)
    must_equal(19, test_suite.errors)
    must_equal(1, test_suite.file_load_failures)

    lines = set(map(lambda l: l.strip(), list(dict.fromkeys(test_suite.get_summary().splitlines()))))
    conditions = [
        'Test files failed to load (1):',
        'test_fails_to_collect',
        'Reason: division by zero'
        ]
    for condition in conditions:
        at_least_some_part = False
        for line in lines:
            if condition in line:
                at_least_some_part = True

        must_equal(True, at_least_some_part)
        

@Test.case
def test_suite_run_sync_normal() -> None:

    suite = initialize_test_suite(run_mode=RunMode.SYNC,
                                  verbosity=Verbosity.NORMAL,
                                  coverage=Coverage.DISABLED,
                                  coverage_target=None,
                                  store_coverage_at=None,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



@Isolate
@Test.case
def test_suite_run_sync_minimal() -> None:

    suite = initialize_test_suite(run_mode=RunMode.ASYNC,
                                  verbosity=Verbosity.MINIMAL,
                                  coverage=Coverage.DISABLED,
                                  coverage_target=None,
                                  store_coverage_at=None,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



@Test.case
def test_suite_run_sync_minimal_no_stack() -> None:

    suite = initialize_test_suite(run_mode=RunMode.SYNC,
                                  verbosity=Verbosity.MINIMAL_NO_STACK,
                                  coverage=Coverage.DISABLED,
                                  coverage_target=None,
                                  store_coverage_at=None,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



@Test.case
def test_suite_run_sync_super_minimal() -> None:

    suite = initialize_test_suite(run_mode=RunMode.ASYNC,
                                  verbosity=Verbosity.SUPER_MINIMAL,
                                  coverage=Coverage.DISABLED,
                                  coverage_target=None,
                                  store_coverage_at=None,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



# XXX update test
@Test.case
def test_thread_local_stdout():
    default_buffer = io.StringIO()
    thread_buffer = io.StringIO()
    _local_thread = threading.local()

    stdout = _ThreadLocalStdout(default_buffer)

    # Without thread-local stream, writes go to default stream
    stdout.write("default")
    stdout.flush()

    assert type(default_buffer.getvalue()) # == "default"
    assert type(thread_buffer.getvalue()) # == ""

    # With thread-local stream, writes go there instead
    _local_thread.stream = thread_buffer

    stdout.write("thread")
    stdout.flush()

    assert type(default_buffer.getvalue())
    assert type(thread_buffer.getvalue()) # == "thread"

    # Cleanup
    del _local_thread.stream



# XXX update test
@Test.case
def test_thread_local_stdout_fallback_after_cleanup():
    default_buffer = io.StringIO()
    thread_buffer = io.StringIO()
    _local_thread = threading.local()

    stdout = _ThreadLocalStdout(default_buffer)

    _local_thread.stream = thread_buffer
    stdout.write("thread")

    del _local_thread.stream

    stdout.write("default")

    assert type(thread_buffer.getvalue()) # == "thread"
    assert type(default_buffer.getvalue()) # == "default"



# XXX update test 
@Test.case
def test_thread_local_stdout_isatty():
    default_buffer = io.StringIO()
    stdout = _ThreadLocalStdout(default_buffer)

    # StringIO doesn't implement isatty(), so fallback is False
    assert stdout.isatty() is False


@Isolate
@Test.case
def test_suite_find_duplicates() -> None:
    duplicate_test = '''

@Test.case
def test_duplicate():
    pass

@Shared(var.int)
@Test.case
def test_duplicate():
    pass
'''
    normal_test = '''

@Test.case
def test_normal():
    pass
'''
    file_names = ['duplicate_test', 'normal_test']

    folder_name = get_unique_folder_name()
    
    for test, name in zip([duplicate_test, normal_test], file_names):
        _ = get_temp_file(test, folder_name=os.path.join(folder_name, name))

    completed_process = run_test(folder_name=folder_name)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Total registered tests  : 1',
        '| Total successes         : 1',
        '| Total errors            : 0',
        '| Test file load failures : 1',
        'Reason: Duplicate test(s) found: < test_duplicate >'

    ]

    for line in completed_process.stdout.splitlines():
        __line = line.strip()
        if __line in conditions:
            conditions.remove(__line)

    must_equal(0, len(conditions))

    delete_test_dir()