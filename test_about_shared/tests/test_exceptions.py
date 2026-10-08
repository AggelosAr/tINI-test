from tini_test._internals._broken import (delete_test_dir, get_temp_file,
                                          run_test)
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def usage_of_non_declared_shared_variable_raises_setup():
    test_name  = 'usage_of_non_declared_shared_variable_raises_setup'
    test = '''

def setup():
    print(var.var_a)
    var.var_a = 111

@Test.case(setup=setup)
def %s(): ...

''' % test_name
    err = 'tini_test.misc.exceptions.SharedVarDoesNotExistInThisContext: Shared variable < var_a > does not exist in this context.'

    _ = get_temp_file(test, test_name)
    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    for line in completed_process.stdout.splitlines():
        if 'SharedVarDoesNotExistInThisContext' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)


# THIS TEST doesn't need subprocess, anyway XXX
@Test.case
def usage_of_non_declared_shared_variable_raises_main():
    test_name = 'usage_of_non_declared_shared_variable_raises_main'
    test = '''

@Test.case
def %s():
    #print(var.var_y)
    print('HELLO')
    var.var_y = 111

''' % test_name
    
    err = 'tini_test.misc.exceptions.SharedVarDoesNotExistInThisContext: Shared variable < var_y > does not exist in this context.'

    _ = get_temp_file(test, test_name)

    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    for line in completed_process.stdout.splitlines():
        if 'SharedVarDoesNotExistInThisContext' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)



@Test.case
def usage_of_non_declared_shared_variable_raises_cleanup():
    test_name = 'usage_of_non_declared_shared_variable_raises_cleanup'
    test = '''

def cleanup():
    print(var.var_a)
    var.var_z = 111

@Test.case(cleanup=cleanup)
def %s(): ...

''' % test_name

    err = 'tini_test.misc.exceptions.SharedVarDoesNotExistInThisContext: Shared variable < var_z > does not exist in this context.'

    _ = get_temp_file(test, test_name)
    completed_process = run_test(test_name, test_name)
    
    must_equal(0, completed_process.returncode)

    for line in completed_process.stdout.splitlines():
        if 'SharedVarDoesNotExistInThisContext' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)


@Test.case
def shared_raises_on_not_defined_variable_case_setup_case_with_name():
    test_name = 'shared_raises_on_not_defined_variable_case_setup_case_with_name'
    test = '''
    
def setup():
    print(var.var_a)
    var.var_a = 111

@Shared(var.var_O)
@Test.case(setup=setup)
def %s(): ...
    
    ''' % test_name
    err = 'tini_test.misc.exceptions.SharedVarDoesNotExistInThisContext: Shared variable < var_a > does not exist in this context. For test < %s >' % test_name

    _ = get_temp_file(test, test_name)
    completed_process = run_test(test_name, test_name)

    must_equal(0, completed_process.returncode)

    for line in completed_process.stdout.splitlines():
        if 'SharedVarDoesNotExistInThisContext' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)


# THIS TEST doesn't need subprocess, anyway XXX
@Test.case
def shared_raises_on_not_defined_variable_case_main_case_with_name():
    test_name = 'shared_raises_on_not_defined_variable_case_main_case_with_name'
    test = '''

@Shared(var.var_O)
@Test.case
def %s():
    #print(var.var_y)
    print('HELLO')
    var.var_y = 111
    
    ''' % test_name
    err = 'tini_test.misc.exceptions.SharedVarDoesNotExistInThisContext: Shared variable < var_y > does not exist in this context. For test < %s >' % test_name

    _ = get_temp_file(test, test_name)

    completed_process = run_test(test_name, test_name)

    # print(completed_process.stdout)
    must_equal(0, completed_process.returncode)

    for line in completed_process.stdout.splitlines():
        if 'SharedVarDoesNotExistInThisContext' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)


# THIS TEST doesn't need subprocess, anyway XXX
@Test.case
def shared_raises_on_not_defined_variable_case_cleanup_case_with_name():
    test_name = 'shared_raises_on_not_defined_variable_case_cleanup_case_with_name'
    test = '''
    
def cleanup():
    print(var.var_a)
    var.var_z = 111

@Shared(var.var_O)
@Test.case(cleanup=cleanup)
def %s(): ...
    
    ''' % test_name
    
    err = 'tini_test.misc.exceptions.SharedVarDoesNotExistInThisContext: Shared variable < var_a > does not exist in this context. For test < %s >' % test_name

    _ = get_temp_file(test, test_name)
    completed_process = run_test(test_name, test_name)

    # print(completed_process.stdout)
    
    must_equal(0, completed_process.returncode)

    for line in completed_process.stdout.splitlines():
        if 'SharedVarDoesNotExistInThisContext' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)



@Test.case
def shared_rejects_same_variable_name():
    test_name = 'shared_rejects_same_variable_name'
    test = '''
@Shared(var.var_a, var.var_a)
@Test.case
def %s(): ...

''' % test_name

    err = 'tini_test.misc.exceptions.SharedVarAlreadyDefined: Shared variable < var_a > is already defined in this context. For test < %s >' % test_name
    
    _ = get_temp_file(test, test_name)
    completed_process = run_test(test_name, test_name)

    # print(completed_process.stderr)

    must_equal(1, completed_process.returncode)

    for line in completed_process.stderr.splitlines():
        if 'SharedVarAlreadyDefined' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)



@Test.case
def shared_raises_when_receiving_keyword_arguments():
    test_name = 'shared_raises_when_receiving_keyword_arguments'
    test = '''

@Shared(my_var=var.var_a)
@Test.case
def %s(): ...

''' % test_name

    err = 'tini_test.misc.exceptions.SharedOnlyAcceptsArguments: Shared only accepts positional arguments.'
    
    _ = get_temp_file(test, test_name)
    completed_process = run_test(test_name, test_name)

    # print(completed_process.stderr)
    
    must_equal(1, completed_process.returncode)

    for line in completed_process.stderr.splitlines():
        if 'SharedOnlyAcceptsArguments' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)



@Test.case
def shared_raises_when_receiving_argument_of_wrong_type():
    test_name = 'shared_raises_when_receiving_argument_of_wrong_type'
    test = '''

@Shared(1, var.var_a)
@Test.case
def %s(): ...

''' % test_name

    err = 'tini_test.misc.exceptions.SharedAcceptedInvalidArguments: Shared accepts only <var> variables.'

    _ = get_temp_file(test, test_name)
    completed_process = run_test(test_name, test_name)

    # print(completed_process.stderr)
    
    must_equal(1, completed_process.returncode)

    for line in completed_process.stderr.splitlines():
        if 'SharedAcceptedInvalidArguments' in line: 
            search_line = line

    must_equal(err, search_line)

    delete_test_dir(test_name)
