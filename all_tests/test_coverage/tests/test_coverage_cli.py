import os
import re

from tini_test import Test, must_equal
from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          run_test)
from tini_test._internals._isolate import Isolate

FOLDER = 'test_coverage_cli'

CASES = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     '..', 'child_cases', 'coverage_cli_cases.py')


def _summary(stdout: str) -> dict[str, int]:
    keys = {
        'Total registered tests': 'total',
        'Total successes': 'successes',
        'Total errors': 'errors',
        'Test file load failures': 'load_failures',
    }
    found = {key: 0 for key in keys.values()}

    for label, value in re.findall(r'\|\s*([A-Za-z ]+?)\s*:\s*(\d+)', stdout):
        if label in keys:
            found[keys[label]] = int(value)

    return found

@Isolate
@Test.case
def test_CoverageCliCasesPassInsideSubprocess() -> None:
    with open(CASES, 'r') as f:
        content = f.read()

    get_temp_file(content, FOLDER)

    # The subprocess runs the cases with coverage enabled so the cli code is traced.
    completed_process = run_test(FOLDER)

    total = content.count('@Test.case(')
    summary = _summary(completed_process.stdout)

    if summary != {'total': total, 'successes': total, 'errors': 0, 'load_failures': 0}:
        # print(completed_process.stdout)
        # print(completed_process.stderr)
        ...

    must_equal({'total': total, 'successes': total, 'errors': 0, 'load_failures': 0}, summary)

    delete_test_dir(FOLDER)
