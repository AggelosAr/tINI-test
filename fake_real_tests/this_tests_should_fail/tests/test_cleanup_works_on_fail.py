from src.utils import Test


GG = 2_999

def __cleanup():
    global GG
    print('__cleanup called val-> %d' % (GG, ))
    GG = 3_999
    print('__cleanup called change val-> %d' % (GG, ))

def __no_op():
    global GG
    print('__no_op called val-> %d' % (GG, ))
    #assert GG == 3_999

@Test.case(cleanup=lambda: __cleanup(), _no_op=lambda: __no_op())
def test_cleanup_works_even_if_test_fails():
    1/0
