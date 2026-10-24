import json
import os
import sys
import uuid

from tini_test import Test, must_equal
from tini_test.__main__ import _tini_test
from tini_test._internals.consts import COVERAGE_ROOT, PROJECT_ROOT
from tini_test.arg_parser import receive_args
from tini_test.coverage.consts import METADATA_FILE

# Set for the suite it runs so that suite does not start this whole chain again.
NESTED_ENV = 'TINI_TEST_FULL_SUITE_CHILD'

# Files only this nested run can cover, the traced child never runs them itself.
EXPECTED_COVERED = ('core.py', 'test.py', 'must_equals.py', os.path.join('_internals', '_ast_utils.py'))


@Test.case
def test_FullSuiteRunsFromCli() -> None:
    store = os.path.join(COVERAGE_ROOT, '%s_full_suite_%s' % (METADATA_FILE, uuid.uuid4()))

    # Same code path as `python -m tini_test <args>`, but in-process and traced.
    old_argv, old_path = sys.argv, list(sys.path)
    os.environ[NESTED_ENV] = '1'
    try:
        os.chdir(PROJECT_ROOT)
        sys.path.insert(0, str(PROJECT_ROOT))
        sys.argv = ['tini_test', '--coverage',
                    '--coverage-target', os.path.join(PROJECT_ROOT, 'src'),
                    '--coverage-store', store]
        _tini_test(*receive_args())
    finally:
        sys.argv = old_argv
        sys.path[:] = old_path
        # The nested suite wipes /tmp/python, the original cwd, so we cannot go back to it.
        os.chdir(PROJECT_ROOT)
        del os.environ[NESTED_ENV]

    with open(os.path.join(store, METADATA_FILE), 'r') as f:
        covered = json.load(f)

    for expected in EXPECTED_COVERED:
        must_equal(True, any(path.endswith(os.path.join('tini_test', expected)) and lines
                             for path, lines in covered.items()))
