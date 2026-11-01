import os
import re
import subprocess
import uuid

from tini_test import Test, must_equal
from tini_test._internals._broken import (create_command, delete_test_dir,
                                          get_temp_file)
from tini_test._internals._isolate import Isolate
from tini_test._internals.consts import COVERAGE_ROOT, PROJECT_ROOT
from tini_test.coverage.consts import METADATA_FILE

FOLDER = 'test_full_suite_coverage'

# Set by the nested suite run, so that suite does not start this test again.
NESTED_ENV = 'TINI_TEST_FULL_SUITE_CHILD'

CASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'child_cases', 'full_suite_case.py')


def get_env() -> dict:
    env = os.environ.copy()

    env['TINI_TEST_COVERAGE']   = '1'
    env['USE_V2_COVERAGE']      = '1'

    store = os.path.join(*[COVERAGE_ROOT, '%s_ROOT_full_suite_%s' % (METADATA_FILE, uuid.uuid4())])
    env['TINI_TEST_COVERAGE_STORAGE'] = store

    instrumentation_path = os.path.join(PROJECT_ROOT, 'src', 'tini_test','integrations')

    env['PYTHONPATH'] = instrumentation_path + os.pathsep + env.get('PYTHONPATH', '')

    return env



@Isolate
@Test.case
def test_FullSuiteRunsInSubprocessWithCoverage() -> None:
    if os.environ.get(NESTED_ENV):
        return

    with open(CASE, 'r') as f:
        get_temp_file(f.read(), FOLDER)

    # The traced subprocess runs the whole suite through the cli in another subprocess.
    # completed_process = run_test(FOLDER, timeout=600)
    # stdout = completed_process.stdout
    # commands = ['python -c "import sitecustomize; print(sitecustomize.__file__)"']

    commands = create_command(FOLDER)
    env = get_env()

    process = subprocess.Popen(' && '.join(commands),
                               shell=True,
                               env=env,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL,
                               # stderr=subprocess.DEVNULL,
                               text=True)
    stdout, _ = process.communicate(timeout=100)
    # print(stdout)
    
    summary = dict(re.findall(r'\|\s*([A-Za-z ]+?)\s*:\s*(\d+)', stdout))


    delete_test_dir(FOLDER)

    must_equal('1', summary.get('Total registered tests'))
    must_equal('1', summary.get('Total successes'))
    must_equal('0', summary.get('Total errors'))
