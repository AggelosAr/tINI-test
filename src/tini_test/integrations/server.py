import os
import secrets
import shlex
import subprocess
import time
import urllib.error
import urllib.request
from contextlib import contextmanager
from itertools import repeat
from typing import Generator, TypeGuard

from tini_test._internals.consts import HEALTH_URL
from tini_test.coverage._coverage import CoverageTracker
from tini_test.misc.annotations import DirectoryPath, FileName

_RECONCILATIONS = (_ for _ in iter(int, 1) for _ in repeat('_%s' % secrets.token_hex(7), 2))


class _ProcessGuard:

    def __init__(self, process: subprocess.Popen[bytes]):
        self.process = process


    
class ServerManager:

    def __init__(self,
                 command: str | None,
                 store_path: DirectoryPath | FileName | None,
                 health_url: str | None) -> None:
        # Server manager can also be used as a proxy for a general coverage
        # In that case there is no need to handle the coverage tracker?
        self.command = command
        self.store_path = store_path

        self.health_url = health_url if health_url is not None else HEALTH_URL
        self.timeout = 30
        
        self._process = _ProcessGuard(self.null().process)

    @property
    def is_enabled(self) -> bool:
        return self.command is not None
    
    @property
    def deadline(self) -> float:
        return time.monotonic() + self.timeout

    @property
    def process(self) -> subprocess.Popen[bytes]:
        return self._process.process

    @process.setter
    def process(self, value: _ProcessGuard) -> None:
        self._process = value

    @staticmethod
    def _is_process(process: _ProcessGuard | None) -> TypeGuard[_ProcessGuard]:
        if process is None:
            raise RuntimeError('Failed to start server process')
        return True

    @staticmethod
    def null() -> _ProcessGuard:
        return _ProcessGuard(None)
        return _ProcessGuard(process=subprocess.Popen(shlex.split('echo'),
                                                      stdout=subprocess.DEVNULL,
                                                      stderr=subprocess.DEVNULL))
    def _start(self) -> None:
        env = os.environ.copy()

        env['TINI_TEST_COVERAGE']          = '1'
        env['TINI_TEST_COVERAGE_STORAGE']  = CoverageTracker.normalize_path(self.store_path)
        env['TINI_TEST_RECONCILE_PATH']    = next(_RECONCILATIONS)

        instrumentation_path = os.path.dirname(__file__)

        env['PYTHONPATH'] = instrumentation_path + os.pathsep + env.get('PYTHONPATH', '')

        _process = subprocess.Popen(shlex.split(self.command),
                                    env=env,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

        self.process = _ProcessGuard(process=_process)

    def wait_until_ready(self) -> None:

        while time.monotonic() < self.deadline:

            # Check whether the server process has crashed.
            return_code = self.process.poll()

            if return_code is not None:
                print('STDERR:', self.process.stderr.read().decode())
                raise RuntimeError('Server exited unexpectedly with code %d' % return_code)

            try:
                with urllib.request.urlopen(self.health_url, timeout=1):
                    return
                
            except urllib.error.HTTPError:
                # HTTP response received: server is reachable.
                return

            except (urllib.error.URLError, TimeoutError, OSError):
                time.sleep(0.25)

        self.stop()

        raise TimeoutError('Server did not become ready within the timeout period')

    def start(self) -> None:
        self._start()
        self.wait_until_ready()

    def stop(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        self._process = _ProcessGuard(self.null().process)

    @contextmanager
    def server_online(self) -> Generator[None, None, None]:
        if not self.is_enabled:
            yield
            return
        try:
            self.start()
            yield
        finally:
            self.stop()
