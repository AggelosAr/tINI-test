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
    stdout, _ = process.communicate(timeout=130)
    # print(stdout)
    
    summary = dict(re.findall(r'\|\s*([A-Za-z ]+?)\s*:\s*(\d+)', stdout))

    delete_test_dir(FOLDER)

    must_equal('1', summary.get('Total registered tests'))
    must_equal('1', summary.get('Total successes'))
    must_equal('0', summary.get('Total errors'))


    # ////////////////////////////
    test_server_manager()
    # ////////////////////////////




# @Test.case
def test_server_manager():
    # TODO this test has a side of generating a .coverage file in the current dir
    # Also this test should run ONLY after the < all_tests/test_coverage/tests/test_full_suite_coverage.py >
    # Since it yields  from _RECONCILATIONS. _RECONCILATIONS is not made to handle multiple concurrent tests.
    import json
    import os
    import shlex
    import socket
    import sys
    import tempfile
    import textwrap
    from pathlib import Path

    import tini_test.integrations.server as server_module
    from tini_test import WillRaise
    from tini_test._internals.consts import HEALTH_URL
    from tini_test.coverage._coverage import CoverageTracker
    from tini_test.integrations.server import ServerManager

    disabled = ServerManager(None, None, None)
    must_equal(False, disabled.is_enabled)
    must_equal(HEALTH_URL, disabled.health_url)
    must_equal(None, disabled.process)
    must_equal(None, ServerManager.null().process)


    with WillRaise(RuntimeError) as context:
        ServerManager._is_process(None)
    must_equal('Failed to start server process', str(context.exception))


    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]

    with tempfile.TemporaryDirectory() as temp_dir:
        report_path = Path(temp_dir, 'environment.json')
        command_source = textwrap.dedent(r'''
            import json
            import os
            from http.server import HTTPServer, SimpleHTTPRequestHandler

            with open(%s, 'w') as report:
                json.dump({
                    name: os.environ[name]
                    for name in (
                        'TINI_TEST_COVERAGE',
                        'TINI_TEST_COVERAGE_STORAGE',
                        'TINI_TEST_RECONCILE_PATH',
                        'PYTHONPATH',
                    )
                }, report)

            HTTPServer(('127.0.0.1', %s), SimpleHTTPRequestHandler).serve_forever()
        ''' % (repr(str(report_path)), port))
        command = '%s -c %s' % (shlex.quote(sys.executable),
                                shlex.quote(command_source))
        health_url = 'http://127.0.0.1:%s/missing' % port
        server = ServerManager(command, temp_dir, health_url)

        must_equal(True, server.is_enabled)

        must_equal(health_url, server.health_url)


        must_equal(True, ServerManager._is_process(server_module._ProcessGuard(object())))


        with server.server_online():
            must_equal(True, server.process.poll() is None)

            with report_path.open() as report:
                environment = json.load(report)

            must_equal('1', environment['TINI_TEST_COVERAGE'])

            must_equal(os.fspath(CoverageTracker.normalize_path(temp_dir)),
                       environment['TINI_TEST_COVERAGE_STORAGE'])
            
            must_equal(True, environment['TINI_TEST_RECONCILE_PATH'].startswith('_'))

            must_equal(
                True,
                os.path.dirname(server_module.__file__) in environment['PYTHONPATH'],
            )

        # ------------------------------

        must_equal(None, server.process)

        with WillRaise(ValueError) as context:
            with server.server_online():
                raise ValueError('inside server context')
            
        must_equal(None, server.process)
        must_equal('inside server context', str(context.exception))

        # ------------------------------

        command = '%s -c %s' % (shlex.quote(sys.executable),
                                shlex.quote('import time; time.sleep(5)'))
        timed_out = ServerManager(command, None, None)
        timed_out.timeout = 0
        with WillRaise(TimeoutError) as context:
            with timed_out.server_online():
                ...

        must_equal('Server did not become ready within the timeout period',
                   str(context.exception))
        must_equal(None, timed_out.process)

        # ------------------------------

        command = '%s -c %s' % (shlex.quote(sys.executable),
                                shlex.quote('raise SystemExit(2)'))
        crashed = ServerManager(command, None, None)

        with WillRaise(RuntimeError) as context:
            crashed.start()
        must_equal('Server exited unexpectedly with code 2', str(context.exception))
