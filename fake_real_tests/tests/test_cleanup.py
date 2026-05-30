from src.test_utils import Test

__GG = 0

def _setup():
    global __GG
    assert __GG == 0
    print('_setup called val was-> %d' % (__GG, ))
    __GG = -10
    print('_setup called val is-> %d' % (__GG, ))
    assert __GG == -10

def _cleanup():
    global __GG
    assert __GG == -20
    print('_cleanup called val was-> %d' % (__GG, ))
    __GG = 1_000
    print('_cleanup called val is-> %d' % (__GG, ))
    assert __GG == 1_000

def _no_op():
    global __GG
    print('_no_op called val-> %d' % (__GG, ))
   

@Test.case(setup=lambda: _setup(), cleanup=lambda: _cleanup(), _no_op=lambda: _no_op())
def test_setup_cleanup_provided():
    global __GG
    print('main called val was-> %d' % (__GG, ))
    assert __GG == -10
    __GG = -20
    assert __GG == -20
    print('main called val is-> %d' % (__GG, ))



_GG = 999

def cleanup():
    global _GG
    print('cleanup called val was-> %d' % (_GG, ))
    _GG = 2_000
    print('cleanup called val is-> %d' % (_GG, ))

def no_op():
    global _GG
    print('no_op called val-> %d' % (_GG, ))
    assert _GG == 2_000

@Test.case(cleanup=lambda: cleanup(), _no_op=lambda: no_op())
def test_cleanup_provided():
    print('main called val is-> %d' % (_GG, ))
    assert _GG == 999



