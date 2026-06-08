import io
import os
import subprocess
import sys
import tempfile
import threading
from contextlib import redirect_stdout
from time import perf_counter

from tini_test.__main__ import _tini_test
from tini_test.context_managers import WillRaise, _ThreadLocalStdout
from tini_test.core import TestSuite
from tini_test.enums import RunMode, Verbosity
from tini_test.initializer import initialize_test_suite
from tini_test.misc.exceptions import CantFindRelativePathToRoot, TestNotFound
from tini_test.module_collector import ModuleCollector
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def test_suite_run() -> None:

    command = ('cd %s && python3 -m tini_test -d test_must_equals -r sync' 
               % ('/home/papaggalos/workspace/python_projects/tINI-test/', ))

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

#     command = ('cd %s && python3 -m tini_test -d /not_there -r sync' 
#                % ('/home/papaggalos/workspace/python_projects/tINI-test/', ))

#     completed_process = subprocess.run(command, 
#                                        timeout=10, 
#                                        text=True, 
#                                        capture_output=True,
#                                        shell=True)
    
#     must_equal(1, completed_process.returncode)

#     must_equal('''
# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "/home/papaggalos/workspace/python_projects/tINI-test/src/tini_test/__main__.py", line 10, in <module>
#     test_suite = initialize_test_suite(**args)
#                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/papaggalos/workspace/python_projects/tINI-test/src/tini_test/initializer.py", line 18, in initialize_test_suite
#     test_collector = ModuleCollector(search_dir, file_name)
#                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/papaggalos/workspace/python_projects/tINI-test/src/tini_test/module_collector.py", line 46, in __init__
#     raise CantFindRelativePathToRoot
# tini_test.misc.exceptions.CantFindRelativePathToRoot: Can't find the requested relative path to root.
# '''.strip()+'\n', completed_process.stderr)
    
#     #   -------------------------------------------------------
#     # -------------------------------------------------------
#     #   -------------------------------------------------------
#     # -------------------------------------------------------
#     #   -------------------------------------------------------

#     command = ('cd %s && python3 -m tini_test -d . -r sync -t not_theressss.py' 
#                % ('/home/papaggalos/workspace/python_projects/tINI-test/', ))

#     completed_process = subprocess.run(command, 
#                                        timeout=10, 
#                                        text=True, 
#                                        capture_output=True,
#                                        shell=True)
    
#     must_equal(1, completed_process.returncode)

#     must_equal('''
# Traceback (most recent call last):
#   File "<frozen runpy>", line 198, in _run_module_as_main
#   File "<frozen runpy>", line 88, in _run_code
#   File "/home/papaggalos/workspace/python_projects/tINI-test/src/tini_test/__main__.py", line 10, in <module>
#     test_suite = initialize_test_suite(**args)
#                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   File "/home/papaggalos/workspace/python_projects/tINI-test/src/tini_test/initializer.py", line 29, in initialize_test_suite
#     test_suite.initialize_tests(_from=test_collector)
#   File "/home/papaggalos/workspace/python_projects/tINI-test/src/tini_test/core.py", line 169, in initialize_tests
#     raise TestNotFound
# tini_test.misc.exceptions.TestNotFound: Test function was not found.
# '''.strip()+'\n', completed_process.stderr)



@Test.case
def crash_main() -> None:
    
    with WillRaise(CantFindRelativePathToRoot):
        _tini_test({'run_mode': RunMode.ASYNC,
                    'verbosity': Verbosity.MINIMAL,
                    'search_dir': '././././where_is?',
                    'file_name': 'None',
                    'test_function': None})
        
    with WillRaise(TestNotFound):
        _tini_test({'run_mode': RunMode.ASYNC,
                    'verbosity': Verbosity.MINIMAL,
                    'search_dir': '.',
                    'file_name': 'None',
                    'test_function': '/./././where_is_it?'})



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
                           verbosity=Verbosity.NORMAL)
    
    test_suite.initialize_tests(_from=test_collector)
    test_suite.suite_init_time = perf_counter()
    
    print(test_suite.container)
    test_suite.runner()
    test_suite.pprint()

    must_equal(21, test_suite.total_tests)
    must_equal(2, test_suite.successes)
    must_equal(19, test_suite.errors)
    must_equal(1, test_suite.failures)

    must_equal(True, "Test files failed to load: ['test_fails_to_collect']" in test_suite.get_summary())

            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------

    test_suite = TestSuite(run_mode=RunMode.SYNC,
                           verbosity=Verbosity.MINIMAL)
    
    test_suite.initialize_tests(_from=test_collector)
    test_suite.suite_init_time = perf_counter()
    
    print(test_suite.container)
    test_suite.runner()
    test_suite.pprint()

    must_equal(21, test_suite.total_tests)
    must_equal(2, test_suite.successes)
    must_equal(19, test_suite.errors)
    must_equal(1, test_suite.failures)

    must_equal(True, "Test files failed to load: ['test_fails_to_collect']" in test_suite.get_summary())

            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------
            # -------------------------------------------------------
            #   -------------------------------------------------------

    test_suite = TestSuite(run_mode=RunMode.SYNC,
                           verbosity=Verbosity.MINIMAL_NO_STACK)
    
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
    must_equal(1, test_suite.failures)

    must_equal(True, "Test files failed to load: ['test_fails_to_collect']" in test_suite.get_summary())




@Test.case
def test_suite_run_sync_normal() -> None:

    suite = initialize_test_suite(run_mode=RunMode.SYNC,
                                  verbosity=Verbosity.NORMAL,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



@Test.case
def test_suite_run_sync_minimal() -> None:

    suite = initialize_test_suite(run_mode=RunMode.ASYNC,
                                  verbosity=Verbosity.MINIMAL,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



@Test.case
def test_suite_run_sync_minimal_no_stack() -> None:

    suite = initialize_test_suite(run_mode=RunMode.SYNC,
                                  verbosity=Verbosity.MINIMAL_NO_STACK,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



@Test.case
def test_suite_run_sync_super_minimal() -> None:

    suite = initialize_test_suite(run_mode=RunMode.ASYNC,
                                  verbosity=Verbosity.SUPER_MINIMAL,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()



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



@Test.case
def test_thread_local_stdout_isatty():
    default_buffer = io.StringIO()
    stdout = _ThreadLocalStdout(default_buffer)

    # StringIO doesn't implement isatty(), so fallback is False
    assert stdout.isatty() is False