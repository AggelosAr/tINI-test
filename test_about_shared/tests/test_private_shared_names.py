import os

from tini_test import Isolate, NotInitialized, Shared, Test, must_equal, var
from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          get_unique_folder_name, run_test)


@Isolate
@Test.case
def test_shared_raises_for_globals_cases():
    test_name = 'test_shared_raises_for_globals_cases'
    _vars = [
        '_direct_mode',
        '__class__',
        '__init__',
        '_generating',
        '_maybe_globals',
        '_test_name',
        '_local_context',
        '__generating',
        '__maybe_globals',
        '__test_name',
        '__local_context',
        '__getattribute__',
        '__getattr__',
        '__setattr__',
        'get_meta_var',
        'get_context_from_shards',
        'with_lock',
        'raise_for_globals',
        'reset',
        'block',
        'update_local_context',
        'test_reset',
        'access_shard',
        '__new__',
        '_trace',
        '_stored_key',
        '_scope',
        '_stored_value',
        '__key__',
        'validate',
        'raise_for_duplicate_vars',
        'add_scope',
    ]
    test_case = lambda _var: '''

@Test.case
def %s(): ...

[var.%s]
''' % (test_name, _var)

    folder_name = get_unique_folder_name()
    
    for _var in _vars:
        _ = get_temp_file(test_case(_var), folder_name=os.path.join(folder_name, 'test_%s' % _var))

    completed_process = run_test(folder_name)
        
    must_equal(0, completed_process.returncode)

    conditions = [
        '| Test file load failures : 32',
    ]
    conditions.extend(['Global shared variable < %s >' % _var for _var in _vars])

    for line in completed_process.stdout.splitlines():
        for condition in conditions:
            if condition in line:
                conditions.remove(condition)

    print('Remaining conditions: ', conditions)
    must_equal(0, len(conditions))


    delete_test_dir(test_name)

# __class__
@Test.case
@Shared(var.__class__)
def test___class__():
    print('\n```````````````````\n')
    print('VAR __class__: ', var.__class__)
    must_equal(NotInitialized, var.__class__)
    var.__class__ = 100
    must_equal(100, var.__class__)
    print('VAR __class__ after assignment: ', var.__class__)
    print('\n```````````````````\n')


# __init__
@Test.case
@Shared(var.__init__)
def test___init__():
    print('\n```````````````````\n')
    print('VAR __init__: ', var.__init__)
    must_equal(NotInitialized, var.__init__)
    var.__init__ = 200
    must_equal(200, var.__init__)
    print('VAR __init__ after assignment: ', var.__init__)
    print('\n```````````````````\n')


# _generating
@Test.case
@Shared(var._generating)
def test_generating():
    print('\n```````````````````\n')
    print('VAR _generating: ', var._generating)
    must_equal(NotInitialized, var._generating)
    var._generating = 300
    must_equal(300, var._generating)
    print('VAR _generating after assignment: ', var._generating)
    print('\n```````````````````\n')



# _maybe_globals
@Test.case
@Shared(var._maybe_globals)
def test__maybe_globals():
    print('\n```````````````````\n')
    print('VAR _maybe_globals: ', var._maybe_globals)
    must_equal(NotInitialized, var._maybe_globals)
    var._maybe_globals = 400
    must_equal(400, var._maybe_globals)
    print('VAR _maybe_globals after assignment: ', var._maybe_globals)
    print('\n```````````````````\n')


# _test_name
@Test.case
@Shared(var._test_name)
def test__test_name():
    print('\n```````````````````\n')
    print('VAR _test_name: ', var._test_name)
    must_equal(NotInitialized, var._test_name)
    var._test_name = 500
    must_equal(500, var._test_name)
    print('VAR _test_name after assignment: ', var._test_name)
    print('\n```````````````````\n')


# _local_context
@Test.case
@Shared(var._local_context)
def test__local_context():
    print('\n```````````````````\n')
    print('VAR _local_context: ', var._local_context)
    must_equal(NotInitialized, var._local_context)
    var._local_context = 600
    must_equal(600, var._local_context)
    print('VAR _local_context after assignment: ', var._local_context)
    print('\n```````````````````\n')



# __generating
@Test.case
@Shared(var.__generating)
def test__generating():
    print('\n```````````````````\n')
    print('VAR __generating: ', var.__generating)
    must_equal(NotInitialized, var.__generating)
    var.__generating = 300
    must_equal(300, var.__generating)
    print('VAR __generating after assignment: ', var.__generating)
    print('\n```````````````````\n')



# __maybe_globals
@Test.case
@Shared(var.__maybe_globals)
def test___maybe_globals():
    print('\n```````````````````\n')
    print('VAR __maybe_globals: ', var.__maybe_globals)
    must_equal(NotInitialized, var.__maybe_globals)
    var.__maybe_globals = 400
    must_equal(400, var.__maybe_globals)
    print('VAR __maybe_globals after assignment: ', var.__maybe_globals)
    print('\n```````````````````\n')


# __test_name
@Test.case
@Shared(var.__test_name)
def test___test_name():
    print('\n```````````````````\n')
    print('VAR __test_name: ', var.__test_name)
    must_equal(NotInitialized, var.__test_name)
    var.__test_name = 500
    must_equal(500, var.__test_name)
    print('VAR __test_name after assignment: ', var.__test_name)
    print('\n```````````````````\n')


# __local_context
@Test.case
@Shared(var.__local_context)
def test___local_context():
    print('\n```````````````````\n')
    print('VAR __local_context: ', var.__local_context)
    must_equal(NotInitialized, var.__local_context)
    var.__local_context = 600
    must_equal(600, var.__local_context)
    print('VAR __local_context after assignment: ', var.__local_context)
    print('\n```````````````````\n')


# __getattribute__
@Test.case
@Shared(var.__getattribute__)
def test___getattribute__():
    print('\n```````````````````\n')
    print('VAR __getattribute__: ', var.__getattribute__)
    must_equal(NotInitialized, var.__getattribute__)
    var.__getattribute__ = 700
    must_equal(700, var.__getattribute__)
    print('VAR __getattribute__ after assignment: ', var.__getattribute__)
    print('\n```````````````````\n')


# __getattr__
@Test.case
@Shared(var.__getattr__)
def test___getattr__():
    print('\n```````````````````\n')
    print('VAR __getattr__: ', var.__getattr__)
    must_equal(NotInitialized, var.__getattr__)
    var.__getattr__ = 800
    must_equal(800, var.__getattr__)
    print('VAR __getattr__ after assignment: ', var.__getattr__)
    print('\n```````````````````\n')



# __setattr__
@Test.case
@Shared(var.__setattr__)
def test___setattr__():
    print('\n```````````````````\n')
    print('VAR __setattr__: ', var.__setattr__)
    must_equal(NotInitialized, var.__setattr__)
    var.__setattr__ = 900
    must_equal(900, var.__setattr__)
    print('VAR __setattr__ after assignment: ', var.__setattr__)
    print('\n```````````````````\n')



# get_meta_var
@Test.case
@Shared(var.get_meta_var)
def test_get_meta_var():
    print('\n```````````````````\n')
    print('VAR get_meta_var: ', var.get_meta_var)
    must_equal(NotInitialized, var.get_meta_var)
    var.get_meta_var = 1000
    must_equal(1000, var.get_meta_var)
    print('VAR get_meta_var after assignment: ', var.get_meta_var)
    print('\n```````````````````\n')


# get_context_from_shards
@Test.case
@Shared(var.get_context_from_shards)
def test_get_context_from_shards():
    print('\n```````````````````\n')
    print('VAR get_context_from_shards: ', var.get_context_from_shards)
    must_equal(NotInitialized, var.get_context_from_shards)
    var.get_context_from_shards = 1100
    must_equal(1100, var.get_context_from_shards)
    print('VAR get_context_from_shards after assignment: ', var.get_context_from_shards)
    print('\n```````````````````\n')


# with_lock
@Test.case
@Shared(var.with_lock)
def test_with_lock():
    print('\n```````````````````\n')
    print('VAR with_lock: ', var.with_lock)
    must_equal(NotInitialized, var.with_lock)
    var.with_lock = 1200
    must_equal(1200, var.with_lock)
    print('VAR with_lock after assignment: ', var.with_lock)
    print('\n```````````````````\n')



# raise_for_globals
@Test.case
@Shared(var.raise_for_globals)
def test_raise_for_globals():
    print('\n```````````````````\n')
    print('VAR raise_for_globals: ', var.raise_for_globals)
    must_equal(NotInitialized, var.raise_for_globals)
    var.raise_for_globals = 1300
    must_equal(1300, var.raise_for_globals)
    print('VAR raise_for_globals after assignment: ', var.raise_for_globals)
    print('\n```````````````````\n')


# reset
@Test.case
@Shared(var.reset)
def test_reset():
    print('\n```````````````````\n')
    print('VAR reset: ', var.reset)
    must_equal(NotInitialized, var.reset)
    var.reset = 1400
    must_equal(1400, var.reset)
    print('VAR reset after assignment: ', var.reset)
    print('\n```````````````````\n')



# block
@Test.case
@Shared(var.block)
def test_block():
    print('\n```````````````````\n')
    print('VAR block: ', var.block)
    must_equal(NotInitialized, var.block)
    var.block = 1500
    must_equal(1500, var.block)
    print('VAR block after assignment: ', var.block)
    print('\n```````````````````\n')



# update_local_context
@Test.case
@Shared(var.update_local_context)
def test_update_local_context():
    print('\n```````````````````\n')
    print('VAR update_local_context: ', var.update_local_context)
    must_equal(NotInitialized, var.update_local_context)
    var.update_local_context = 1600
    must_equal(1600, var.update_local_context)
    print('VAR update_local_context after assignment: ', var.update_local_context)
    print('\n```````````````````\n')



# test_reset
@Test.case
@Shared(var.test_reset)
def test_test_reset():
    print('\n```````````````````\n')
    print('VAR test_reset: ', var.test_reset)
    must_equal(NotInitialized, var.test_reset)
    var.test_reset = 1700
    must_equal(1700, var.test_reset)
    print('VAR test_reset after assignment: ', var.test_reset)
    print('\n```````````````````\n')


# access_shard
@Test.case
@Shared(var.access_shard)
def test_access_shard():
    print('\n```````````````````\n')
    print('VAR access_shard: ', var.access_shard)
    must_equal(NotInitialized, var.access_shard)
    var.access_shard = 1800
    must_equal(1800, var.access_shard)
    print('VAR access_shard after assignment: ', var.access_shard)
    print('\n```````````````````\n')


###################################################

# __new__
@Test.case
@Shared(var.__new__)
def test___new__():
    print('\n```````````````````\n')
    print('VAR __new__: ', var.__new__)
    must_equal(NotInitialized, var.__new__)
    var.__new__ = 1900
    must_equal(1900, var.__new__)
    print('VAR __new__ after assignment: ', var.__new__)
    print('\n```````````````````\n')


# _trace
@Test.case
@Shared(var._trace)
def test__trace():
    print('\n```````````````````\n')
    print('VAR _trace: ', var._trace)
    must_equal(NotInitialized, var._trace)
    var._trace = 2000
    must_equal(2000, var._trace)
    print('VAR _trace after assignment: ', var._trace)
    print('\n```````````````````\n')


# _stored_key
@Test.case
@Shared(var._stored_key)
def test__stored_key():
    print('\n```````````````````\n')
    print('VAR _stored_key: ', var._stored_key)
    must_equal(NotInitialized, var._stored_key)
    var._stored_key = 2100
    must_equal(2100, var._stored_key)
    print('VAR _stored_key after assignment: ', var._stored_key)
    print('\n```````````````````\n')


# _scope
@Test.case
@Shared(var._scope)
def test__scope():
    print('\n```````````````````\n')
    print('VAR _scope: ', var._scope)
    must_equal(NotInitialized, var._scope)
    var._scope = 2200
    must_equal(2200, var._scope)
    print('VAR _scope after assignment: ', var._scope)
    print('\n```````````````````\n')



# _stored_value
@Test.case
@Shared(var._stored_value)
def test__stored_value():
    print('\n```````````````````\n')
    print('VAR _stored_value: ', var._stored_value)
    must_equal(NotInitialized, var._stored_value)
    var._stored_value = 2300
    must_equal(2300, var._stored_value)
    print('VAR _stored_value after assignment: ', var._stored_value)
    print('\n```````````````````\n')



# __key__
@Test.case
@Shared(var.__key__)
def test___key__():
    print('\n```````````````````\n')
    print('VAR __key__: ', var.__key__)
    must_equal(NotInitialized, var.__key__)
    var.__key__ = 2400
    must_equal(2400, var.__key__)
    print('VAR __key__ after assignment: ', var.__key__)
    print('\n```````````````````\n')


# validate
@Test.case
@Shared(var.validate)
def test_validate():
    print('\n```````````````````\n')
    print('VAR validate: ', var.validate)
    must_equal(NotInitialized, var.validate)
    var.validate = 2500
    must_equal(2500, var.validate)
    print('VAR validate after assignment: ', var.validate)
    print('\n```````````````````\n')


# raise_for_duplicate_vars
@Test.case
@Shared(var.raise_for_duplicate_vars)
def test_raise_for_duplicate_vars():
    print('\n```````````````````\n')
    print('VAR raise_for_duplicate_vars: ', var.raise_for_duplicate_vars)
    must_equal(NotInitialized, var.raise_for_duplicate_vars)
    var.raise_for_duplicate_vars = 2600
    must_equal(2600, var.raise_for_duplicate_vars)
    print('VAR raise_for_duplicate_vars after assignment: ', var.raise_for_duplicate_vars)
    print('\n```````````````````\n')


# add_scope
@Test.case
@Shared(var.add_scope)
def test_add_scope():
    print('\n```````````````````\n')
    print('VAR add_scope: ', var.add_scope)
    must_equal(NotInitialized, var.add_scope)
    var.add_scope = 2700
    must_equal(2700, var.add_scope)
    print('VAR add_scope after assignment: ', var.add_scope)
    print('\n```````````````````\n')




################################

# _direct_mode
@Test.case
@Shared(var._direct_mode)
def test__direct_mode():
    print('\n```````````````````\n')
    print('VAR _direct_mode: ', var._direct_mode)
    must_equal(NotInitialized, var._direct_mode)
    var._direct_mode = 2800
    must_equal(2800, var._direct_mode)
    print('VAR _direct_mode after assignment: ', var._direct_mode)
    print('\n```````````````````\n')

