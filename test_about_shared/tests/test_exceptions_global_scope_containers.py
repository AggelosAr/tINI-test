from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          run_test)
from tini_test.must_equals import must_equal
from tini_test.shared import Shared, var
from tini_test.test_utils import Test



@Shared(var.Z) # Force this test to run in isolation. XXX 3
@Test.case
def test_good_and_bad_tests():
    good_test = '''
@Test.case
def test_good_test(): ...
'''
    
    bad_test = '''
@Shared(var.int)
@Test.case
def test_bad_test(): ...

[var.int]
'''
    _ = get_temp_file(good_test, 'good_test')
    _ = get_temp_file(bad_test, 'bad_test')


    completed_process = run_test()

    # print(completed_process.stdout)
    # print(completed_process.stderr)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Total registered tests  : 1',
        '| Total successes         : 1',
        '| Test file load failures : 1',
        '[var.int]',
        'tini_test.misc.exceptions.GlobalSharedVarsAreNotSupported: Global shared variable < int > is not supported.'
        ]

    for line in completed_process.stdout.splitlines():
        f_line = line.strip()
        if f_line in conditions:
            conditions.remove(f_line)

    must_equal(0, len(conditions))
    delete_test_dir()


@Test.case
def test_solo_bad_test():
    bad_test = '''


@Test.case
def test_bad_test(): ...

[var.int]
'''

    _ = get_temp_file(bad_test, 'bad_test')
    
    completed_process = run_test()

    # print(completed_process.stdout)
    # print(completed_process.stderr)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Total registered tests  : 0',
        '| Test file load failures : 1',
        '[var.int]',
        'Reason: Global shared variable < int > is not supported.'
        ]

    for line in completed_process.stdout.splitlines():
        f_line = line.strip()
        if f_line in conditions:
            conditions.remove(f_line)

    must_equal(0, len(conditions))
    delete_test_dir()




_cases = [
'''
def in_scope_var(arg=var.a): ...   # >>> Refuses to give this <var.a> as default
@Test.case
@Shared(var.a, var.b)
def a(): ...
''',

'''
_ = {'key': var.b}                 # >>> Refuses to give this <var.b> as global
@Test.case
@Shared(var.b)
def b(): ...
''',

'''
class C:
    c = var.c                      # >>> Refuses to give this <var.c> as global
@Test.case
@Shared(var.c)
def c(): ...
''',

'''
_ = lambda: var.d                  # >>> Accepts to give this <var.d> as 'global'
@Test.case                         # Since this is a closure
@Shared(var.d)
def d(): _()                       # And test passes since it is in context
''',

'''
_ = lambda: var.e                  # >>> Accepts to give this <var.e> as 'global'
@Test.case                         # Since this is a closure
@Shared(var.a)
def e(): _()                       # And test fails since it is not in context
'''
]

@Shared(var.Z) # Force this test to run in isolation. XXX 3 
@Test.case
def cases():
    names = ['a', 'b', 'c', 'd', 'e']
    for test, name in zip(_cases, names):
        _ = get_temp_file(test, name)


    completed_process = run_test()

    print(completed_process.stdout)
    print(completed_process.stderr)

    must_equal(0, completed_process.returncode)

    conditions = [
        '| Total registered tests  : 2',
        '| Total successes         : 1',
        '| Total errors            : 1',
        '| Test file load failures : 3',

        'def in_scope_var(arg=var.a): ...   # >>> Refuses to give this <var.a> as default',
        'Reason: Global shared variable < a > is not supported.',

        "_ = {'key': var.b}                 # >>> Refuses to give this <var.b> as global",
        'Reason: Global shared variable < b > is not supported.',

        "c = var.c                      # >>> Refuses to give this <var.c> as global",
        'Reason: Global shared variable < c > is not supported.',
        
        "def e(): _()                       # And test fails since it is not in context",
        '         ~^^',
        "_ = lambda: var.e                  # >>> Accepts to give this <var.e> as 'global'",
        '            ^^^^^',
        'tini_test.misc.exceptions.SharedVarDoesNotExistInThisContext: Shared variable < e > does not exist in this context. For test < e >',
    ]
    conditions = set(c.strip() for c in conditions)

    for line in completed_process.stdout.splitlines():
        f_line = line.strip()
        if f_line in conditions:
            conditions.remove(f_line)

    must_equal(0, len(conditions))

    delete_test_dir()

