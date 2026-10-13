from tini_test import Test, must_equal
from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          run_test)


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

    # print(completed_process.stdout)
    # print(completed_process.stderr)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.DuplicateMockRegisteredOnTest: Duplicate mock function < __ > registered on test < %s >' % test_name
    ]

    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))

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

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.TestDecoratorUsedMoreThanOnce: Test decorator used more than once on test < %s >' % test_name
    ]

    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))

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

        must_equal(0, completed_process.returncode)

        conditions = [
            '| Test file load failures : 1',
            'tini_test.misc.exceptions.TestDecoratorUsedMoreThanOnce: Test decorator used more than once on test < %s >' % f'test_exceptions_3_{i}'
        ]
        for line in completed_process.stdout.splitlines():
            for condition in conditions:
                if condition in line:
                    conditions.remove(condition)

        must_equal(0, len(conditions))

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

    # print(completed_process.stdout)
    # print(completed_process.stderr)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.MockWasUsedOnWithoutTestDecorator: Missing test decorator for function decorated with mock function < %s >' % test_name
    ]
    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))

    delete_test_dir(test_name)


@Test.case
def test_MockMissingFunctionError() -> None:
    test_name = 'test_MockMissingFunctionError'
    content = '''
     
@Mock.mock(None, returns=42)
@Test.case
def %s() -> None:
    1/0
    ''' % test_name
    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.MockMissingFunctionError: Mock function is missing.'
    ]
    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))
    
    delete_test_dir(test_name)

    test_name = 'test_MockMissingFunctionError'
    content = '''
        
@Mock.mock(returns=42)
@Test.case
def %s() -> None:
    1/0
    ''' % test_name
    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.MockMissingFunctionError: Mock function is missing.'
    ]
    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))

    delete_test_dir(test_name)


@Test.case
def test_MockGotBothReturnValueAndArgs() -> None:
    test_name = 'test_MockGotBothReturnValueAndArgs'
    content = '''
     
@Mock.mock(lambda: 1, args=(), kwargs={}, returns=42)
@Test.case
def %s() -> None:
    1/0
    ''' % test_name
    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.MockDefinitionError: Mock should not accept both return value and arguments.'
    ]
    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))

    delete_test_dir(test_name)


@Test.case
def test_MockCallDefinitionErrorArgs() -> None:
    test_name = 'test_MockCallDefinitionErrorArgs'
    content = '''
     
@Mock.mock(lambda: 1, args=100,)
@Test.case
def %s() -> None:
    1/0
    ''' % test_name
    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.MockCallDefinitionError: Arguments should be of type tuple.'
    ]
    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))

    delete_test_dir(test_name)


@Test.case
def test_MockCallDefinitionErrorKwargs() -> None:
    test_name = 'test_MockCallDefinitionErrorKwargs'
    content = '''
     
@Mock.mock(lambda: 1, kwargs=100)
@Test.case
def %s() -> None:
    1/0
    ''' % test_name
    get_temp_file(content, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 1',
        'tini_test.misc.exceptions.MockCallDefinitionError: Keyword arguments should be of type dict.'
    ]
    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    must_equal(0, len(conditions))

    delete_test_dir(test_name)

