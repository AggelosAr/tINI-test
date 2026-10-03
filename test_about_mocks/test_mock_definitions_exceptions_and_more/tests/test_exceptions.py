import os
import shutil
import subprocess
import tempfile
from typing import Optional

from tini_test.must_equals import must_equal
from tini_test.test_utils import Test

# TODO fix missing test names


ROOT = '/tmp/python/tini_test'

HEADERS = '''
from tini_test.test_utils import Test
from tini_test.mock import Mock
'''


def get_temp_file(content: str, folder_name: str) -> None:

    temp_dir = os.path.join('/', 'tmp', 'python', 'tini_test', folder_name, 'tests')
    os.makedirs(temp_dir, exist_ok=True)

    with tempfile.NamedTemporaryFile(mode='w',
                                     prefix='test_',
                                     suffix='.py',
                                     delete=False,
                                     dir=temp_dir) as f:
        f.write(content)


def run_test(folder_name: str, 
             test_name: Optional[str] = None, 
             test_file: Optional[str] = None) -> subprocess.CompletedProcess:

    command = ('cd %s && python3 -m tini_test -d %s' 
                % (ROOT, folder_name))
    
    if test_name:
        command += ' -t %s' % test_name
    if test_file:
        command += ' -f %s' % test_file

    completed_process = subprocess.run(command, 
                                       timeout=10, 
                                       text=True, 
                                       capture_output=True,
                                       shell=True)
    return completed_process


@Test.case
def test_DuplicateMockRegisteredOnTest() -> None:

    content = HEADERS + '''

def __(a) -> None: ...

@Mock.mock(__, args=(1,))
@Mock.mock(__, args=(1,))
@Test.case
def test_DuplicateMockRegisteredOnTest() -> None:
    1/0
'''
    get_temp_file(content, 'test_exceptions_1')

    completed_process = run_test('test_exceptions_1', 'test_DuplicateMockRegisteredOnTest')

    try:
        must_equal(1, completed_process.returncode)
    
        err = 'tini_test.misc.exceptions.DuplicateMockRegisteredOnTest: Duplicate mock function < __ > registered on test <  >'
        must_equal(err, completed_process.stderr.splitlines()[-1])
    finally:
        shutil.rmtree('/tmp/python/tini_test/test_exceptions_1', ignore_errors=True)
   



@Test.case
def test_TestDecoratorUsedMoreThanOnce() -> None:

    content = HEADERS + '''

@Mock.mock
@Test.case
@Test.case
def test_TestDecoratorUsedMoreThanOnce() -> None:
    1/0
'''
    get_temp_file(content, 'test_exceptions_2')

    completed_process = run_test('test_exceptions_2', 'test_TestDecoratorUsedMoreThanOnce')

    try:
        print(completed_process.stdout)
        print(completed_process.stderr)
        must_equal(1, completed_process.returncode)
        # tini_test.misc.exceptions.TestDecoratorUsedMoreThanOnce: Test decorator used more than once on test < <function Test.case.<locals>.wrapper.<locals>._wrapper at 0x7ed68c2d0e00> >
        err = 'tini_test.misc.exceptions.TestDecoratorUsedMoreThanOnce: Test decorator used more than once on test '
        unique_lines = list(map(lambda l: l.strip(), list(dict.fromkeys(completed_process.stderr.splitlines()))))

        passes = False
        for idx, line in enumerate(unique_lines):
                if err in line:
                    passes = True
        must_equal(True, passes)
    finally:
        shutil.rmtree('/tmp/python/tini_test/test_exceptions_2', ignore_errors=True)


@Test.case
def test_TestDecoratorUsedMoreThanOnce_2() -> None:

    content = ['''

@Test.case
@Test.case
def test_TestDecoratorUsedMoreThanOnce_2x() -> None:
    1/0

''',

'''
    
@Test.case()
@Test.case()
def test_TestDecoratorUsedMoreThanOnce_2y() -> None:
    1/0

''',

'''

@Test.case()
@Test.case
def test_TestDecoratorUsedMoreThanOnce_2z() -> None:
    1/0

''',

'''

@Test.case
@Test.case()
def test_TestDecoratorUsedMoreThanOnce_2a() -> None:
    1/0

''',

'''
@Test.case
@Test.case()
@Test.case()
def test_TestDecoratorUsedMoreThanOnce_2b() -> None:
    1/0

''',
]   
    for i, c in enumerate(content):
        get_temp_file(HEADERS+c, f'test_exceptions_3_{i}')

        completed_process = run_test(folder_name=f'test_exceptions_3_{i}')

        print(completed_process.stdout)
        print(completed_process.stderr)

        try:
            must_equal(0, completed_process.returncode)
            unique_lines = list(map(lambda l: l.strip(), list(dict.fromkeys(completed_process.stdout.splitlines()))))

            err1 = 'Test files failed to load (1):'
            err2 = 'tini_test.misc.exceptions.TestDecoratorUsedMoreThanOnce: Test decorator used more than once on test < None >'
            must_equal(True, err1 in unique_lines and err2 in unique_lines)
        finally:
            shutil.rmtree(f'/tmp/python/tini_test/test_exceptions_3_{i}', ignore_errors=True)



@Test.case
def test_MockWasUsedOnWithoutTestDecorator() -> None:

    content = HEADERS + '''

@Mock.mock
def test_MockWasUsedOnWithoutTestDecorator() -> None:
    1/0
'''
    get_temp_file(content, 'test_exceptions_4')

    completed_process = run_test('test_exceptions_4', 'test_MockWasUsedOnWithoutTestDecorator')

    try:
        must_equal(1, completed_process.returncode)
    
        err = 'tini_test.misc.exceptions.MockWasUsedOnWithoutTestDecorator: Missing test decorator for function decorated with mock function < test_MockWasUsedOnWithoutTestDecorator >'
        must_equal(err, completed_process.stderr.splitlines()[-1])
    finally:
        shutil.rmtree('/tmp/python/tini_test/test_exceptions_4', ignore_errors=True)
   
