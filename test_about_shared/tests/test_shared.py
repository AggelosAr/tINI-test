from functools import partial

from tini_test.must_equals import must_equal
from tini_test.shared import NotInitialized, Shared, SharedVar, var
from tini_test.test_utils import Test


must_equal = partial(must_equal, comperator=SharedVar.__eq__)



@Shared()
@Test.case
def empty_shared_are_ignored_p(): ...

@Shared
@Test.case
def empty_shared_are_ignored_n_p(): ...


@Shared(var.var_a)
@Test.case
def shared_accepts_valid_arguments(): ...



@Test.case
def shared_raises_when_receiving_keyword_arguments():
    # SharedOnlyAcceptsArguments
    test = '''
@Shared(my_var=var.var_a)
@Test.case
def shared_raises_when_receiving_keyword_arguments(): ...
'''


@Test.case
def shared_raises_when_receiving_argument_of_wrong_type():
    # SharedAcceptedInvalidArguments
    tests = [
'''
@Shared(1, var.var_a)
@Test.case
def shared_raises_when_receiving_argument_of_wrong_type(): ...
''',

'''
@Shared(var.var_a, object)
@Test.case
def shared_raises_when_receiving_argument_of_wrong_type(): ...
''',

'''
@Shared(var.var_a, object)
@Test.case
def shared_raises_when_receiving_argument_of_wrong_type(): ...
''',

'''
@Shared(var.var_a, type)
@Test.case
def shared_raises_when_receiving_argument_of_wrong_type(): ...
'''

,

'''
@Shared(None)
@Test.case
def shared_raises_when_receiving_argument_of_wrong_type(): ...
'''
    ]
    expected_results = [
        
    ]





@Test.case
def shared_rejects_same_variable_name():
    # SharedVarAlreadyDefined
    test = '''
@Shared(var.var_a, var.var_a)
@Test.case
def shared_rejects_same_variable_name():
'''


# @Test.case
# def shared_raises_on_not_defined_variable_case_setup():
#     SharedVarDoesNotExistInThisContext
# @Test.case
# def shared_raises_on_not_defined_variable_case_main():
#     ...
# @Test.case
# def shared_raises_on_not_defined_variable_case_cleanup():
#     ...


@Shared(var.var_a)
@Test.case
def shared_initializes_shared_variable(): must_equal(NotInitialized, var.var_a)



@Shared(var.var_a)
@Test.case
def shared_allows_modification_of_shared_variable():
    must_equal(NotInitialized, var.var_a)
    var.var_a = 42
    must_equal(42, var.var_a)
    var.var_a = 44
    must_equal(44, var.var_a)



@Test.case
def usage_of_non_declared_shared_variable_raises_setup():
    test = '''
@Test.case(setup=lambda: print(var.var_a))
def usage_of_non_declared_shared_variable_raises_setup():
'''

@Test.case
def usage_of_non_declared_shared_variable_raises_main():
    test = '''
@Test.case
def usage_of_non_declared_shared_variable_raises_main():
'''

@Test.case
def usage_of_non_declared_shared_variable_raises_cleanup():
    test = '''
@Test.case(cleanup=lambda: print(var.var_a))
def usage_of_non_declared_shared_variable_raises_cleanup():
'''



def s1():
    must_equal(NotInitialized, var.var_a)
    var.var_a = 42
    must_equal(42, var.var_a)

@Shared(var.var_a)
@Test.case(s1, lambda: must_equal(42, var.var_a))
def var_mod_in_setup_persists_in_main_and_cleanup(): must_equal(42, var.var_a)




@Test.case(lambda: must_equal(NotInitialized, var.var_a), 
           lambda: must_equal(44, var.var_a))
@Shared(var.var_a)
def var_mod_in_main_persists_in_cleanup():
    var.var_a = 44



def s3():
    must_equal(NotInitialized, var.var_a)
    var.var_a = 46
    must_equal(46, var.var_a)

@Shared(var.var_a)
@Test.case(setup=s3, 
           cleanup=lambda: must_equal(47, var.var_a))
def var_mod_in_setup_and_main():
    must_equal(46, var.var_a)
    var.var_a = 47
    must_equal(47, var.var_a)
   


@Test.case(lambda: must_equal(NotInitialized, var.var_a), 
           lambda: must_equal(42, var.var_a))
@Shared(var.var_a)
def var_mod_in_main_does_not_exist_in_setup(): var.var_a = 42



# def c4(): var.var_a = 42
# @Shared(var.var_a)
# @Test.case(lambda: must_equal(NotInitialized, var.var_a), 
#            lambda: c4, 
#            lambda: must_equal(42, var.var_a))
# def var_mod_in_cleanup_does_not_exist_in_setup_and_main(): must_equal(NotInitialized, var.var_a)



# @Shared(var.var_a)
# @Test.case(lambda: must_equal(NotInitialized, var.var_a), 
#            lambda: must_equal(NotInitialized, var.var_a), 
#            lambda: must_equal(NotInitialized, var.var_a))
# def unused_shared_variable(): must_equal(NotInitialized, var.var_a)


