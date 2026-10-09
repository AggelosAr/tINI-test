'''
NOTE: 
    For each test passing using this method, ensure there is a identical 
    test failing in the <> dir for coverage. 
    >>> The alternative is to run a custom coverage command, inside each 
    of these tests and merge the final coverage results with the main coverage report.

'''
# We have problem on async? Maybe ? do this a context manager.
# XXX Move passing tests to failing. And make the big tests 1

import os
import shutil
import subprocess
import tempfile
import uuid
from typing import Optional

ROOT = '/tmp/python/tini_test'

HEADERS = '''
from tini_test.test_utils import Test
from tini_test.mock import Mock
from tini_test.shared import SharedVar, Shared, var, NotInitialized
from tini_test.must_equals import must_equal

'''

def get_unique_folder_name() -> str:
    return str(uuid.uuid4())


def get_temp_file(content: str, folder_name: str) -> str:

    delete_test_dir(folder_name)
    
    temp_dir = os.path.join('/', 'tmp', 'python', 'tini_test', folder_name, 'tests')
    os.makedirs(temp_dir, exist_ok=True)

    data = '%s\n%s' % (HEADERS, content, )

    with tempfile.NamedTemporaryFile(mode='w',
                                     prefix='test_',
                                     suffix='.py',
                                     delete=False,
                                     dir=temp_dir) as f:
        f.write(data)

    return data


def delete_test_dir(folder_name: Optional[str] = '') -> None:
    if not folder_name:
        temp_dir = '/tmp/python'
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return
    
    temp_dir = os.path.join(ROOT, folder_name)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def run_test(folder_name: Optional[str] = None, 
             test_name: Optional[str] = None, 
             test_file: Optional[str] = None) -> subprocess.CompletedProcess:

    # TODO
    project_root = '/home/papaggalos/workspace/python_projects/tINI-test'
    env_path = '312venv/bin/activate'
    python_path_from_project = '312venv/bin/python'
    python_path_from_project = '.venv/bin/python'

    if not folder_name:
        folder_name = 'tini_test'

    python3 = os.path.join(project_root, python_path_from_project)

    commands = [
        'cd %s' % (ROOT, ),
        '%s -m tini_test -d %s' % (python3, folder_name, )
    ]
    
    if test_name:
        commands[-1] += ' -t %s' % test_name
    if test_file:
        commands[-1] += ' -f %s' % test_file

    completed_process = subprocess.run(' && '.join(commands),
                                       timeout=10, 
                                       text=True, 
                                       capture_output=True,
                                       shell=True)
    return completed_process
