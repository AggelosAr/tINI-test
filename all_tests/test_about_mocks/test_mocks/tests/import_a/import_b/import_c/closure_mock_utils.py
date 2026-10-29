

X = 10
Y = 10
UPDATED = {'X', 'Y'}


def imported_closure_as_function(x):

    def inner():
        return x + 100

    return inner()


def imported_closure_with_namny_args(*args, **kwargs):

    def inner():
        return sum(args) + sum(kwargs.values())

    return inner()


def imported_closure_with_global_defined(*args):

    def inner():
        global X
        res = X + 10
        return res

    return inner()



def imported_closure_with_global(*args):

    def inner():
        res = X + 10
        return res

    return inner()


def imported_combination_closure(y):

    def inner():
        global Y
        res = Y + y
        return res

    return inner()



def imported_closure_with_free_var(x):

    def inner(y):
        return x + y

    return inner(x)



def imported_closure_modify_global_X():

    def inner():
        UPDATED.discard('X')

    return inner()


def imported_closure_modify_global_Y():

    def inner():
        UPDATED.discard('Y')

    return inner()



def imported_closure_with_class(arg1):

    class Inner:
        def __init__(self, _value_a, _value_b):
            self._value_a = _value_a
            self._value_b = _value_b


    def inner(arg2):
        obj = Inner(arg1, arg2)
        return obj

    arg2 = 'X'
    return inner(arg2)