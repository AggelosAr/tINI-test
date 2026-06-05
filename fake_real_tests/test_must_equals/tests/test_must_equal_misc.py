from tini_test.context_manager import WillRaise
from tini_test.misc.exceptions import ExpectedWasDifferentFromActual
from tini_test.must_equals import must_equal
from tini_test.test_utils import Test


@Test.case
def test_must_equal_frozen_set_passes() -> None:

    s = frozenset({1, 2, 3})
    t = frozenset({1, 2, 3})

    must_equal(s, t)



@Test.case
def test_must_equal_type_none_case() -> None:

    s = type(None)
    t = type(None)
    
    must_equal(s, t)



@Test.case
def test_must_equal_type_case_different() -> None:

    s = type(1)
    t = type(None)
    
    with WillRaise(ExpectedWasDifferentFromActual) as e:
        must_equal(s, t)

    must_equal('''
<class 'int'> != <class 'NoneType'>
''', str(e.exception))



@Test.case
def test_must_equal_none_type() -> None:

    s = None
    t = type(None)
    
    with WillRaise(ExpectedWasDifferentFromActual) as e:
        must_equal(s, t)

    must_equal('''
ITEM: type mismatch
expected: <class 'NoneType'>
actual:   <class 'type'>
''', str(e.exception))



@Test.case
def test_must_equal_type_none() -> None:

    s = type(None)
    t = None
    
    with WillRaise(ExpectedWasDifferentFromActual) as e:
        must_equal(s, t)

    must_equal('''
ITEM: type mismatch
expected: <class 'type'>
actual:   <class 'NoneType'>
''', str(e.exception))
    


@Test.case
def test_test_wont_break() -> None:

    s1 = '{{{}}}'
    print(s1)

    s2 = '{}'
    print(s2)

    s3 = '{'
    print(s3)

    s4 = '}'
    print(s4)

    s5 = '%s%s%s%s'
    print(s5)

    s6 = '%%s%%s%%s%%s'
    print(s6)

    s7 = '%%%s%%%s%%s%%s'
    print(s7)

    class CustomException(Exception):

        def __init__(self, msg):
            super().__init__(msg)

    with WillRaise(CustomException) as e:
        raise CustomException(s1)
    
    print(e)
    print(str(e.exception))
    must_equal('{{{}}}', str(e.exception))

    with WillRaise(CustomException) as e:
        raise CustomException(s2)
    
    print(e)
    print(str(e.exception))
    must_equal(s2, str(e.exception))
    
    with WillRaise(CustomException) as e:
        raise CustomException(s3)
    
    print(e)
    print(str(e.exception))
    must_equal('{', str(e.exception))

    with WillRaise(CustomException) as e:
        raise CustomException(s4)
    
    print(e)
    print(str(e.exception))
    must_equal(s4, str(e.exception))

    with WillRaise(CustomException) as e:
        raise CustomException(s5)
    
    print(e)
    print(str(e.exception))
    must_equal('%s%s%s%s', str(e.exception))

    with WillRaise(CustomException) as e:
        raise CustomException(s6)
    
    print(e)
    print(str(e.exception))
    must_equal('%%s%%s%%s%%s', str(e.exception))

    with WillRaise(CustomException) as e:
        raise CustomException(s7)
    
    print(e)
    print(str(e.exception))
    must_equal('%%%s%%%s%%s%%s', str(e.exception))
