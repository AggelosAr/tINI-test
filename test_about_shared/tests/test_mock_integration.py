import os

from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          get_unique_folder_name, run_test)
from tini_test.context_managers import WillRaise
from tini_test.misc.exceptions import SharedVarDoesNotExistInThisContext
from tini_test.mock import Mock
from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, var
from tini_test.test_utils import Test


class MyNewClass:
    pass


def mocked_function_return(*args, var_a, **kwargs):

    var.klass = MyNewClass
    var.callable = lambda: 111
    var.int = 46
    var.none = 'X'
    return args, var_a, kwargs



@Test.case
@Mock.mock(mocked_function_return, returns=(123,))
@Shared(var.int, var.klass, var.callable, var.none)
def test_integration_mock_return():
    class MyClass:
        pass
    var.klass = MyClass
    var.callable = lambda: 100
    var.int = 42
    var.none = None

    res = mocked_function_return(var_a=var.int)
    must_equal((123, ), res)

    must_equal(MyClass, var.klass)
    must_equal(100, var.callable())
    must_equal(42, var.int)
    must_equal(None, var.none)


####################################


def mocked_function_call(*args, var_a, **kwargs):

    var.klass = MyNewClass
    var.callable = lambda: 111
    var.int = 46
    var.none = 'X'

    return args, var_a, kwargs


@Test.case
@Mock.mock(mocked_function_call, args=(123,), kwargs={'var_a': 123})
@Shared(var.int, var.klass, var.callable, var.none)
def test_integration_mock_call():
    var.int = 123
    var.klass = type('MyClass', (), {})
    var.callable = lambda: 100
    var.none = None

    args, var_a, kwargs = mocked_function_call(var_a=var.int)

    must_equal(MyNewClass, var.klass)
    must_equal(111, var.callable())
    must_equal(46, var.int)
    must_equal('X', var.none)



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


_cases = [
'''
def mocked_function(): ...
@Shared(var.a)
@Mock.mock(mocked_function, returns=(var.a,))            # XXX 2
@Test.case
def a(): ...
''',

'''
def mocked_function(args): ...
@Shared(var.b)
@Mock.mock(mocked_function, args=(var.b,))               # ^
@Test.case
def b(): ...
''',

'''
def mocked_function(args): ...
@Shared(var.c)
@Mock.mock(mocked_function, kwargs={'var_c': var.c})     # ^
@Test.case
def c(): ...
'''
]
@Test.case
def cases():

    folder_name = get_unique_folder_name()
    names = ['a', 'b', 'c']
    for test, name in zip(_cases, names):
        _ = get_temp_file(test, folder_name=os.path.join(folder_name, name))


    completed_process = run_test(folder_name=folder_name)

    print(completed_process.stdout)
    print(completed_process.stderr)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Total registered tests  : 0',
        '| Total successes         : 0',
        '| Total errors            : 0',
        '| Test file load failures : 3',

        'Reason: Global shared variable < a > is not supported.',
        '@Mock.mock(mocked_function, returns=(var.a,))            # XXX 2',

        'Reason: Global shared variable < b > is not supported.',
        '@Mock.mock(mocked_function, args=(var.b,))               # ^',

        'Reason: Global shared variable < c > is not supported.',
        "@Mock.mock(mocked_function, kwargs={'var_c': var.c})     # ^",

    ]
    conditions = set(c.strip() for c in conditions)

    for line in completed_process.stdout.splitlines():
        f_line = line.strip()
        if f_line in conditions:
            conditions.remove(f_line)

    must_equal(0, len(conditions))

    delete_test_dir(folder_name)


   
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def mocker(*args, **kwargs):
    var.y
    return args, kwargs


@Test.case
@Mock.mock(mocker, returns=(100,))
@Shared(var.int)
def mocker_raises_not_in_context_returns():
    must_equal((100,), mocker())
    


@Test.case
@Mock.mock(mocker, args=(100,))
@Shared(var.int)
def mocker_raises_not_in_context_args():
    with WillRaise(SharedVarDoesNotExistInThisContext) as context:
        mocker(var.int)

    print(str(context.exception))
    err = 'Shared variable < y > does not exist in this context. For test < mocker_raises_not_in_context_args >'
    must_equal(err, str(context.exception))



@Test.case
@Mock.mock(mocker, kwargs={'var_c': 100})
@Shared(var.int)
def mocker_raises_not_in_context_kwargs():
    with WillRaise(SharedVarDoesNotExistInThisContext) as context:
        mocker(var.int)

    print(str(context.exception))
    err = 'Shared variable < y > does not exist in this context. For test < mocker_raises_not_in_context_kwargs >'
    must_equal(err, str(context.exception))



def mocker2(*args, **kwargs):
    return args, kwargs

@Test.case
@Mock.mock(mocker2, kwargs={'var_c': lambda: var.Z})
@Shared(var.int)
def mocker_raises_on_container():
    with WillRaise(SharedVarDoesNotExistInThisContext) as context:
        mocker2(var.int)[1][ 'var_c' ]()

    print(str(context.exception))
    err = 'Shared variable < Z > does not exist in this context. For test < mocker_raises_on_container >'
    must_equal(err, str(context.exception))



@Test.case
@Mock.mock(mocker2, kwargs={'var_c': lambda: var.Z})
@Shared(var.Z)
def mocker_wont_raise_on_container_if_in_context():
    res = mocker2(var.Z)[1][ 'var_c' ]()
    must_equal(NotInitialized, res)

