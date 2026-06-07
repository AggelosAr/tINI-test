import subprocess

from tini_test.enums import RunMode, Verbosity
from tini_test.initializer import initialize_test_suite
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

    suite = initialize_test_suite(run_mode=RunMode.SYNC,
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

    suite = initialize_test_suite(run_mode=RunMode.SYNC,
                                  verbosity=Verbosity.SUPER_MINIMAL,
                                  search_dir='test_must_equals')
    
    print(suite.container)
    suite.runner()
    suite.pprint()