from src.utils import Test



__GG = 0

def _setup():
    global __GG
    __GG = -10
    print('_setup called val-> %d' % (__GG, ))

def _cleanup():
    global __GG
    __GG = 10
    print('_cleanup called val-> %d' % (__GG, ))

def _no_op():
    global __GG
    print('_no_op called val-> %d' % (__GG, ))
    assert __GG == 10

@Test.case(setup=lambda: _setup(), cleanup=lambda: _cleanup(), _no_op=lambda: _no_op())
def test_setup_cleanup_provided():
    print('This should show !~')
    assert __GG == -10



_GG = 999

def cleanup():
    global _GG
    _GG = 2_000
    print('cleanup called val-> %d' % (_GG, ))

def no_op():
    global __GG
    print('no_op called val-> %d' % (_GG, ))
    assert _GG == 2_000

@Test.case(cleanup=lambda: cleanup(), _no_op=lambda: no_op())
def test_cleanup_provided():
    assert _GG == 999
