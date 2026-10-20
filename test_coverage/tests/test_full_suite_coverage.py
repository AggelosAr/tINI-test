import os
import re

from tini_test import Test, must_equal
from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          run_test)

FOLDER = 'test_full_suite_coverage'

# Set by the nested suite run, so that suite does not start this test again.
NESTED_ENV = 'TINI_TEST_FULL_SUITE_CHILD'

CASE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', 'child_cases', 'full_suite_case.py')


@Test.case
def test_FullSuiteRunsInSubprocessWithCoverage() -> None:
    if os.environ.get(NESTED_ENV):
        return

    with open(CASE, 'r') as f:
        get_temp_file(f.read(), FOLDER)

    # The traced subprocess runs the whole suite through the cli in another subprocess.
    completed_process = run_test(FOLDER, timeout=600)

    summary = dict(re.findall(r'\|\s*([A-Za-z ]+?)\s*:\s*(\d+)', completed_process.stdout))

    delete_test_dir(FOLDER)

    must_equal('1', summary.get('Total registered tests'))
    must_equal('1', summary.get('Total successes'))
    must_equal('0', summary.get('Total errors'))
