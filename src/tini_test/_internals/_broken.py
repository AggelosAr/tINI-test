# TODO cleanup here
# We have problem on async? Maybe ? do this a context manager.


import os
import shutil
import subprocess
import tempfile
import uuid
from typing import Optional

USING_COVERAGE = True
USING_COVERAGE = False

COVERAGE_ROOT = '/tmp/coverages/tini_test/'

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

    
    project_root = '/home/papaggalos/workspace/python_projects/tINI-test'
    env_path = '312venv/bin/activate'
    python_path_from_project = '312venv/bin/python'
    # python_path_from_project = '.venv/bin/python'

    if not folder_name:
        folder_name = 'tini_test'

    python3 = os.path.join(project_root, python_path_from_project)

    
    commands = [
        'cd %s' % (ROOT, ),
    ]


    run_tini_test_command = '%s -m tini_test -d %s' % (python3, folder_name, )

    if USING_COVERAGE:
        if not os.path.exists(COVERAGE_ROOT):
            os.makedirs(COVERAGE_ROOT, exist_ok=True)

        tini_test_source = '/home/papaggalos/workspace/python_projects/tINI-test/src'
        coverage_command = ('%s -m '\
                            'coverage run '\
                            '--source=%s '\
                            '--data-file=%s.coverage.run_%s '\
                            '-m '
                                % 
                                (
                                    python3, 
                                    tini_test_source, 
                                    COVERAGE_ROOT, get_unique_folder_name(), 
                                )
                            )
        
        run_tini_test_command = '%s tini_test -d %s' % (coverage_command, folder_name, )
    
    if test_name:
        run_tini_test_command += ' -t %s' % test_name
    if test_file:
        run_tini_test_command += ' -f %s' % test_file

    
    commands.append(run_tini_test_command)


    completed_process = subprocess.run(' && '.join(commands),
                                       timeout=10, 
                                       text=True, 
                                       capture_output=True,
                                       shell=True)
    return completed_process
