import os
import shlex
import subprocess
import time
import urllib.request
import urllib.error


class ServerManager:

    def __init__(self,
                 command: str,
                 health_url: str='http://127.0.0.1:8000/',
                 timeout: int=30):
        
        self.command = command
        self.health_url = health_url
        self.timeout = timeout
        self.process = None

    @property
    def deadline(self) -> float:
        return time.monotonic() + self.timeout

    def start(self) -> None:
        env = os.environ.copy()

        env['TINI_TEST_COVERAGE'] = '1'
        env['TINI_TEST_COVERAGE_STORAGE'] = '/home/papaggalos/workspace/python_projects/library/coverage_reports.json'

        instrumentation_path = os.path.dirname(__file__)

        env['PYTHONPATH'] = instrumentation_path + os.pathsep + env.get('PYTHONPATH', '')

        self.process = subprocess.Popen(shlex.split(self.command),
                                        env=env,
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)

        self.wait_until_ready()

    def wait_until_ready(self) -> None:

        while time.monotonic() < self.deadline:

            # Check whether the server process has crashed.
            return_code = self.process.poll()

            if return_code is not None:
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

    def stop(self) -> None:
        if self.process and self.process.poll() is None:
            self.process.terminate()

            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

        self.process = None