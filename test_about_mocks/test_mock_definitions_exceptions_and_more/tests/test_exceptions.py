from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          run_test)
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def test_DuplicateMockRegisteredOnTest() -> None:
    test_name = 'test_DuplicateMockRegisteredOnTest'
    content = '''

def __(a) -> None: ...

@Mock.mock(__, args=(1,))
@Mock.mock(__, args=(1,))
@Test.case
def test_DuplicateMockRegisteredOnTest() -> None:
    1/0
'''

    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(1, completed_process.returncode)

    err = 'tini_test.misc.exceptions.DuplicateMockRegisteredOnTest: Duplicate mock function < __ > registered on test < %s >' % test_name
    must_equal(err, completed_process.stderr.splitlines()[-1])

    delete_test_dir(test_name)




@Test.case
def test_TestDecoratorUsedMoreThanOnce() -> None:
    test_name = 'test_TestDecoratorUsedMoreThanOnce'

    content = '''

@Mock.mock
@Test.case
@Test.case
def %s() -> None:
    1/0

''' % test_name
    
    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(1, completed_process.returncode)
    err = 'tini_test.misc.exceptions.TestDecoratorUsedMoreThanOnce: Test decorator used more than once on test < %s >' % test_name
    unique_lines = list(map(lambda l: l.strip(), list(dict.fromkeys(completed_process.stderr.splitlines()))))

    passes = False
    for idx, line in enumerate(unique_lines):
            if err in line:
                passes = True
    must_equal(True, passes)

    delete_test_dir(test_name)


@Test.case
def test_TestDecoratorUsedMoreThanOnce_2() -> None:

    content = ['''

@Test.case
@Test.case
def %s() -> None:
    1/0

''',

'''
    
@Test.case()
@Test.case()
def %s() -> None:
    1/0

''',

'''

@Test.case()
@Test.case
def %s() -> None:
    1/0

''',

'''

@Test.case
@Test.case()
def %s() -> None:
    1/0

''',

'''
@Test.case
@Test.case()
@Test.case()
def %s() -> None:
    1/0

''',
]   
    for i, c in enumerate(content):
        c = c % f'test_exceptions_3_{i}'
        get_temp_file(c, f'test_exceptions_3_{i}')

        completed_process = run_test(f'test_exceptions_3_{i}', f'test_exceptions_3_{i}')

        # print(completed_process.stdout)
        # print(completed_process.stderr)

        must_equal(1, completed_process.returncode)
        unique_lines = list(map(lambda l: l.strip(), list(dict.fromkeys(completed_process.stderr.splitlines()))))

        err2 = 'tini_test.misc.exceptions.TestDecoratorUsedMoreThanOnce: Test decorator used more than once on test < %s >' % f'test_exceptions_3_{i}'
        must_equal(True, err2 in unique_lines)

        delete_test_dir(f'test_exceptions_3_{i}')



@Test.case
def test_MockWasUsedOnWithoutTestDecorator() -> None:
    test_name = 'test_MockWasUsedOnWithoutTestDecorator'
    content = '''

@Mock.mock
def %s() -> None:
    1/0
''' % test_name
    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(1, completed_process.returncode)

    err = 'tini_test.misc.exceptions.MockWasUsedOnWithoutTestDecorator: Missing test decorator for function decorated with mock function < %s >' % test_name
    must_equal(err, completed_process.stderr.splitlines()[-1])

    delete_test_dir(test_name)

