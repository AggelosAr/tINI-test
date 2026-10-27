from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import ___test_mocking_in_outside_function
from tini_test import Isolate, Mock, Shared, Test, WillRaise, must_equal, var
from tini_test.misc.exceptions import MockClassDefinitionError


class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add_more(self, z):
        return self.x + self.y + z


class MyClass2:
    def __init__(self, x, y):
        self.x = x
        self.y = y



@Isolate
@Test.case()
def test_mocking_as_context_manager():

    with Mock.mocking(MyClass, args=(1, 2)):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    instance = MyClass('?', '?')
    must_equal('?', instance.x)
    must_equal('?', instance.y)

    with Mock.mocking(MyClass, args=(1,), kwargs={'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, kwargs={'x': 1, 'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000,)):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass, args=(3, 4)):
        with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000_000,)):
            instance = MyClass('?', '?')
            must_equal(3, instance.x)
            must_equal(4, instance.y)
            must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
            print('works')

    print('works')


@Isolate
@Test.case()
def test_mocking_as_context_manager_test_test():
    def test():
        with Mock.mocking(MyClass, args=(1, 2)):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)
    
        instance = MyClass('?', '?')
        must_equal('?', instance.x)
        must_equal('?', instance.y)
    
        with Mock.mocking(MyClass, args=(1,), kwargs={'y': 2}):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)
    
        with Mock.mocking(MyClass, kwargs={'x': 1, 'y': 2}):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)
    
        with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000,)):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))
    
        with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': 1_000}):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))
    
        with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': 1_000}):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))
    
        with Mock.mocking(MyClass, args=(3, 4)):
            with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000_000,)):
                instance = MyClass('?', '?')
                must_equal(3, instance.x)
                must_equal(4, instance.y)
                must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
                print('works')
    
        print('works')

    test()
    test()


######################################################################################
######################################################################################



@Isolate
@Test.case
def test_nesting_mockings():
    with Mock.mocking(MyClass, args=(100, 200)):

        with Mock.mocking(MyClass, args=(1_000, 2_000)):
            instance = MyClass('?', '?')
            must_equal(1_000, instance.x)
            must_equal(2_000, instance.y)

        instance = MyClass('?', '?')
        must_equal(100, instance.x)
        must_equal(200, instance.y)

    instance = MyClass('?', '?')
    must_equal('?', instance.x)
    must_equal('?', instance.y)

    with Mock.mocking(MyClass, args=(100, 200)):
    
        with Mock.mocking(MyClass, args=(1_000, 2_000)):
            instance = MyClass('?', '?')
            must_equal(1_000, instance.x)
            must_equal(2_000, instance.y)

        instance = MyClass('?', '?')
        must_equal(100, instance.x)
        must_equal(200, instance.y)

    instance = MyClass('?', '?')
    must_equal('?', instance.x)
    must_equal('?', instance.y)


@Isolate
@Test.case
def test_nesting_mockings_test_test():
    def test():

        with Mock.mocking(MyClass, args=(100, 200)):
        
            with Mock.mocking(MyClass, args=(1_000, 2_000)):
                instance = MyClass('?', '?')
                must_equal(1_000, instance.x)
                must_equal(2_000, instance.y)
    
            instance = MyClass('?', '?')
            must_equal(100, instance.x)
            must_equal(200, instance.y)
    
        instance = MyClass('?', '?')
        must_equal('?', instance.x)
        must_equal('?', instance.y)
    
        with Mock.mocking(MyClass, args=(100, 200)):
        
            with Mock.mocking(MyClass, args=(1_000, 2_000)):
                instance = MyClass('?', '?')
                must_equal(1_000, instance.x)
                must_equal(2_000, instance.y)
    
            instance = MyClass('?', '?')
            must_equal(100, instance.x)
            must_equal(200, instance.y)
    
        instance = MyClass('?', '?')
        must_equal('?', instance.x)
        must_equal('?', instance.y)

    test()
    test()


######################################################################################
######################################################################################


# Validate low level mocking overrides higher level mocking

@Isolate
@Mock.mock(MyClass, args=('xyz', 'xyz'))
@Mock.mock(MyClass2, args=('xyz', 'xyz'))
@Mock.mock(MyClass.add_more, args=('xyz', 'xyz',))
@Test.case()
def test_mocking_order():

    with Mock.mocking(MyClass, args=(1, 2)):
        instance = MyClass('?', '?')
        print('instance x:', instance.x)
        print('instance y:', instance.y)

        must_equal(1, instance.x)
        must_equal(2, instance.y)

        # Validate wrong items are not overridden by the low-level mock
        instance2 = MyClass2('?', '?')
        must_equal('xyz', instance2.x)
        must_equal('xyz', instance2.y)

    with Mock.mocking(MyClass, args=(1,), kwargs={'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, kwargs={'x': 1, 'y': 2}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000,)):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': 1_000}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass, args=(3, 4)):
        with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000_000,)):
            instance = MyClass('?', '?')
            must_equal(3, instance.x)
            must_equal(4, instance.y)
            must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
            print('works')

    print('works')



@Isolate
@Mock.mock(MyClass, args=('xyz', 'xyz'))
@Mock.mock(MyClass2, args=('xyz', 'xyz'))
@Mock.mock(MyClass.add_more, args=('xyz', 'xyz',))
@Test.case()
def test_mocking_order_test_test():

    def test():
        with Mock.mocking(MyClass, args=(1, 2)):
            instance = MyClass('?', '?')
            print('instance x:', instance.x)
            print('instance y:', instance.y)
    
            must_equal(1, instance.x)
            must_equal(2, instance.y)
    
            # Validate wrong items are not overridden by the low-level mock
            instance2 = MyClass2('?', '?')
            must_equal('xyz', instance2.x)
            must_equal('xyz', instance2.y)
    
        with Mock.mocking(MyClass, args=(1,), kwargs={'y': 2}):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)
    
        with Mock.mocking(MyClass, kwargs={'x': 1, 'y': 2}):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)
    
        with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000,)):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))
    
        with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': 1_000}):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))
    
        with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': 1_000}):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))
    
        with Mock.mocking(MyClass, args=(3, 4)):
            with Mock.mocking(MyClass.add_more, args=(MyClass, 1_000_000,)):
                instance = MyClass('?', '?')
                must_equal(3, instance.x)
                must_equal(4, instance.y)
                must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
                print('works')
    
        print('works')

    test()
    test()


######################################################################################
######################################################################################



# Test for nesting mockings with top level

@Isolate
@Test.case
@Mock.mock(MyClass, args=('xyz', 'xyz'))
def test_nesting_mockings_with_top_level():
    with Mock.mocking(MyClass, args=(100, 200)):

        with Mock.mocking(MyClass, args=(1_000, 2_000)):
            instance = MyClass('?', '?')
    
            must_equal(1_000, instance.x)
            must_equal(2_000, instance.y)

        instance = MyClass('?', '?')

        must_equal(100, instance.x)
        must_equal(200, instance.y)

    instance = MyClass('?', '?')
    
    must_equal('xyz', instance.x)
    must_equal('xyz', instance.y)

    with Mock.mocking(MyClass, args=(100, 200)):
    
        with Mock.mocking(MyClass, args=(1_000, 2_000)):
            instance = MyClass('?', '?')
    
            must_equal(1_000, instance.x)
            must_equal(2_000, instance.y)

        instance = MyClass('?', '?')

        must_equal(100, instance.x)
        must_equal(200, instance.y)

    instance = MyClass('?', '?')
    
    must_equal('xyz', instance.x)
    must_equal('xyz', instance.y)



@Isolate
@Test.case
@Mock.mock(MyClass, args=('xyz', 'xyz'))
def test_nesting_mockings_with_top_level_test_test():

    def test():
        with Mock.mocking(MyClass, args=(100, 200)):

            with Mock.mocking(MyClass, args=(1_000, 2_000)):
                instance = MyClass('?', '?')
        
                must_equal(1_000, instance.x)
                must_equal(2_000, instance.y)

            instance = MyClass('?', '?')

            must_equal(100, instance.x)
            must_equal(200, instance.y)

        instance = MyClass('?', '?')
        
        must_equal('xyz', instance.x)
        must_equal('xyz', instance.y)

        with Mock.mocking(MyClass, args=(100, 200)):
        
            with Mock.mocking(MyClass, args=(1_000, 2_000)):
                instance = MyClass('?', '?')
        
                must_equal(1_000, instance.x)
                must_equal(2_000, instance.y)

            instance = MyClass('?', '?')

            must_equal(100, instance.x)
            must_equal(200, instance.y)

        instance = MyClass('?', '?')
        
        must_equal('xyz', instance.x)
        must_equal('xyz', instance.y)


    test()
    test()




######################################################################################
######################################################################################


@Isolate
@Test.case
def test_nesting_mockings_with_top_level_with_local_item():

    class MyClass3:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def add_more(self, z):
            return self.x + self.y + z
        
    with Mock.mocking(MyClass3, args=(100, 200)):

        with Mock.mocking(MyClass3, args=(1_000, 2_000)):
            instance = MyClass3('?', '?')
    
            must_equal(1_000, instance.x)
            must_equal(2_000, instance.y)

        instance = MyClass3('?', '?')

        must_equal(100, instance.x)
        must_equal(200, instance.y)

    instance = MyClass3('?', '?')
    
    must_equal('?', instance.x)
    must_equal('?', instance.y)

    with Mock.mocking(MyClass3, args=(100, 200)):
    
        with Mock.mocking(MyClass3, args=(1_000, 2_000)):

            with Mock.mocking(MyClass3, args=(1_000_000, 2_000_000)):

                with Mock.mocking(MyClass3, args=(1_000_000_000, 2_000_000_000)):
                    instance = MyClass3('?', '?')

                    print(instance.x)
                    print(instance.y)
                    must_equal(1_000_000_000, instance.x)
                    must_equal(2_000_000_000, instance.y)
            
            
            instance = MyClass3('?', '?')
    
            must_equal(1_000, instance.x)
            must_equal(2_000, instance.y)

        instance = MyClass3('?', '?')

        must_equal(100, instance.x)
        must_equal(200, instance.y)

    instance = MyClass3('?', '?')
    
    must_equal('?', instance.x)
    must_equal('?', instance.y)



@Isolate
@Test.case
def test_nesting_mockings_with_top_level_with_local_item_test_test():

    def test():
        class MyClass3:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def add_more(self, z):
                return self.x + self.y + z
            
        with Mock.mocking(MyClass3, args=(100, 200)):

            with Mock.mocking(MyClass3, args=(1_000, 2_000)):
                instance = MyClass3('?', '?')
        
                must_equal(1_000, instance.x)
                must_equal(2_000, instance.y)

            instance = MyClass3('?', '?')

            must_equal(100, instance.x)
            must_equal(200, instance.y)

        instance = MyClass3('?', '?')
        
        must_equal('?', instance.x)
        must_equal('?', instance.y)

        with Mock.mocking(MyClass3, args=(100, 200)):
        
            with Mock.mocking(MyClass3, args=(1_000, 2_000)):

                with Mock.mocking(MyClass3, args=(1_000_000, 2_000_000)):

                    with Mock.mocking(MyClass3, args=(1_000_000_000, 2_000_000_000)):
                        instance = MyClass3('?', '?')

                        print(instance.x)
                        print(instance.y)
                        must_equal(1_000_000_000, instance.x)
                        must_equal(2_000_000_000, instance.y)
                
                
                instance = MyClass3('?', '?')
        
                must_equal(1_000, instance.x)
                must_equal(2_000, instance.y)

            instance = MyClass3('?', '?')

            must_equal(100, instance.x)
            must_equal(200, instance.y)

        instance = MyClass3('?', '?')
        
        must_equal('?', instance.x)
        must_equal('?', instance.y)

    test()
    test()



######################################################################################
######################################################################################


@Isolate
@Test.case
def test_one_function():

    def test():

        def my_function(x, y):
            return x + y
            
        with Mock.mocking(my_function, args=(100, 200)):

            with Mock.mocking(my_function, args=(1_000, 2_000)):
                result = my_function('?', '?')

                must_equal(1_000 + 2_000, result)

            result = my_function('?', '?')

            must_equal(100 + 200, result)

        must_equal(2, my_function(1, 1))

        with Mock.mocking(my_function, args=(100, 200)):
        
            with Mock.mocking(my_function, args=(1_000, 2_000)):

                with Mock.mocking(my_function, args=(1_000_000, 2_000_000)):

                    with Mock.mocking(my_function, args=(1_000_000_000, 2_000_000_000)):
                        result = my_function('?', '?')

                        must_equal(1_000_000_000 + 2_000_000_000, result)

                result = my_function('?', '?')

                must_equal(1_000 + 2_000, result)

            result = my_function('?', '?')

            must_equal(100 + 200, result)

        must_equal(2, my_function(1, 1))

    test()
    test()


######################################################################################
######################################################################################


# Test shared integration

@Isolate
@Test.case
@Shared(var.a, var.b, var.c, var.d)
def test_mocking_as_context_manager_with_shared_integration():

    var.a, var.b = 1, 2
    
    with Mock.mocking(MyClass, args=(var.a, var.b)):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, args=(var.a,), kwargs={'y': var.b}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)

    with Mock.mocking(MyClass, kwargs={'x': var.a, 'y': var.b}):
        instance = MyClass('?', '?')
        must_equal(1, instance.x)
        must_equal(2, instance.y)


    var.c = 1_000

    with Mock.mocking(MyClass.add_more, args=(MyClass, var.c,)):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': var.c}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))

    with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': var.c}):
        must_equal(1 + 2 + 1_000, instance.add_more('?'))


    var.a, var.b = 3, 4
    var.c = 1_000_000
    var.d = MyClass

    with Mock.mocking(MyClass, args=(var.a, var.b)):
        with Mock.mocking(MyClass.add_more, args=(var.d, var.c,)):
            instance = MyClass('?', '?')
            must_equal(3, instance.x)
            must_equal(4, instance.y)
            must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
            print('works')

    print('works')




@Isolate
@Test.case
@Shared(var.a, var.b, var.c, var.d)
def test_mocking_as_context_manager_with_shared_integration_test_test():

    def test():
        var.a, var.b = 1, 2
        
        with Mock.mocking(MyClass, args=(var.a, var.b)):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)

        with Mock.mocking(MyClass, args=(var.a,), kwargs={'y': var.b}):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)

        with Mock.mocking(MyClass, kwargs={'x': var.a, 'y': var.b}):
            instance = MyClass('?', '?')
            must_equal(1, instance.x)
            must_equal(2, instance.y)


        var.c = 1_000

        with Mock.mocking(MyClass.add_more, args=(MyClass, var.c,)):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))

        with Mock.mocking(MyClass.add_more, args=(MyClass,), kwargs={'z': var.c}):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))

        with Mock.mocking(MyClass.add_more, kwargs={'self': MyClass, 'z': var.c}):
            must_equal(1 + 2 + 1_000, instance.add_more('?'))


        var.a, var.b = 3, 4
        var.c = 1_000_000
        var.d = MyClass

        with Mock.mocking(MyClass, args=(var.a, var.b)):
            with Mock.mocking(MyClass.add_more, args=(var.d, var.c,)):
                instance = MyClass('?', '?')
                must_equal(3, instance.x)
                must_equal(4, instance.y)
                must_equal(3 + 4 + 1_000_000, instance.add_more('?'))
                print('works')

        print('works')

    test()
    test()


######################################################################################
######################################################################################



# @Isolate
# @Test.case
# @Shared(var.a, var.b, var.c, var.d)
# def test_mocking_as_context_manager_maintains_state_of_shared():
#     var.a, var.b = 1, 'y'
#     with Mock.mocking(MyClass, args=(var.a, var.b)):

#         var.a, var.b = 10, 'yy'
#         with Mock.mocking(MyClass, args=(var.a, var.b)):

#             var.a, var.b = 100, 'yyy'
#             with Mock.mocking(MyClass, args=(var.a, var.b)):

#                 var.a, var.b = 1000, 'yyyy'
#                 with Mock.mocking(MyClass, args=(var.a, var.b)):

#                     instance = MyClass('?', '?')
#                     must_equal(1000, instance.x)
#                     must_equal('yyyy', instance.y)

#             instance = MyClass('?', '?')
#             must_equal(100, instance.x)
#             must_equal('yyy', instance.y)

#         instance = MyClass('?', '?')
#         must_equal(10, instance.x)
#         must_equal('yy', instance.y)

#     instance = MyClass('?', '?')
#     must_equal('?', instance.x)
#     must_equal('?', instance.y)

#     var.a, var.b = 1, 'y'
#     with Mock.mocking(MyClass, args=(var.a, var.b)):

#         var.a, var.b = 10, 'yy'
#         with Mock.mocking(MyClass, args=(var.a, var.b)):

#             var.a, var.b = 100, 'yyy'
#             with Mock.mocking(MyClass, args=(var.a, var.b)):

#                 var.a, var.b = 1000, 'yyyy'
#                 with Mock.mocking(MyClass, args=(var.a, var.b)):

#                     instance = MyClass('?', '?')
#                     must_equal(1000, instance.x)
#                     must_equal('yyyy', instance.y)

#             instance = MyClass('?', '?')
#             must_equal(100, instance.x)
#             must_equal('yyy', instance.y)

#         instance = MyClass('?', '?')
#         must_equal(10, instance.x)
#         must_equal('yy', instance.y)

#     instance = MyClass('?', '?')
#     must_equal('?', instance.x)
#     must_equal('?', instance.y)


######################################################################################
######################################################################################



# Test mocking exceptions
@Isolate
@Test.case()
def test_exceptions():

    def func_e(arg1, arg2, k_val_1=1000, k_val_2=2000):
        return (arg1 or 0) + (arg2 or 0) + (k_val_1 or 0) + (k_val_2 or 0)

    with WillRaise(TypeError) as context:
        with Mock.mocking(func_e, args=(None, None, 100, 100), kwargs={'k_val_2': 100}):
            func_e('?')

    must_equal("multiple values for argument 'k_val_2'", str(context.exception))
  
    class MyClass:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def add(self):
            return self.x + self.y

    with WillRaise(MockClassDefinitionError) as context:
        with Mock.mocking(MyClass, returns=MyClass(100, 100)):
            MyClass('?')

    must_equal('Mock class only accepts initialization arguments.', str(context.exception))



######################################################################################
######################################################################################



# Test mocking in outside function

def test_mocked_function(*args, **kwargs):
    return sum(args) + sum(kwargs.values())


def test_mocking_in_outside_function(*args, **kwargs):
    with Mock.mocking(test_mocked_function, args=(5, 5), kwargs={'k_val_1': 5}):
        result = test_mocked_function('?')
    must_equal(15, result)
    return result


@Isolate
@Test.case
def test_mocking_in_outside_function_isolated():
    must_equal(15, test_mocking_in_outside_function('?'))
    must_equal(15, test_mocking_in_outside_function('?'))


# test for mocking on top of outside function, AKA ignore context
@Isolate
@Test.case
@Mock.mock(test_mocking_in_outside_function, args=('?', '?'), kwargs={'k_val_1': '?'})
def test_mocking_on_top_of_outside_function_isolated():
    must_equal(15, test_mocking_in_outside_function('?'))
    must_equal(15, test_mocking_in_outside_function('?'))

######################################################################################
######################################################################################



# Test mocking in imported function

@Isolate
@Test.case
def test_mocking_in_outside_imported_function_isolated():
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        ___test_mocking_in_outside_function
    must_equal(15, ___test_mocking_in_outside_function('?'))
    must_equal(15, ___test_mocking_in_outside_function('?'))



# test for mocking on top of imported function, AKA ignore context

@Isolate
@Test.case
@Mock.mock(___test_mocking_in_outside_function, args=('?', '?'), kwargs={'k_val_1': '?'})
def test_mocking_on_top_of_imported_function_isolated():
    from test_about_mocks.test_mocks.tests.import_a.import_b.import_c.m_c import \
        ___test_mocking_in_outside_function
    must_equal(15, ___test_mocking_in_outside_function('?'))
    must_equal(15, ___test_mocking_in_outside_function('?'))
