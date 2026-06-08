from tini_test.test import Test


GG = 2_999

def __cleanup():
    global GG
    print('__cleanup called val-> %d' % (GG, ))
    GG = 3_999
    print('__cleanup called change val-> %d' % (GG, ))

def __no_op():
    global GG
    print('__no_op called val-> %d' % (GG, ))
    assert GG == 3_999

@Test.case(cleanup=lambda: __cleanup(), _no_op=lambda: __no_op())
def test_cleanup_works_even_if_test_fails():
    1/0



# Is there even a point to this test ? XXX
_GG = 2_999
def _setup():
    global _GG
    print('_setup called val-> %d' % (_GG, ))
    1/0

def _cleanup():
    global _GG
    print('_cleanup called val-> %d' % (_GG, ))
    _GG = 2_999
    print('_cleanup called change val-> %d' % (_GG, ))

def _no_op():
    global _GG
    print('_no_op called val-> %d' % (_GG, ))
    assert _GG == 2_999

@Test.case(setup=lambda: _setup(), 
           cleanup=lambda: _cleanup(), 
           _no_op=lambda: _no_op())
def test_cleanup_works_even_if_setup_fails():
    ...



_GGX = 2_999
def _setupX():
    global _GGX
    print('_setupX called val-> %d' % (_GGX, ))
    1/0

def _cleanupX():
    global _GGX
    print('_cleanupX called val-> %d' % (_GGX, ))
    print('_cleanupX will now break')
    1/0
    
def _no_opX():
    global _GGX
    print('_no_opX called val-> %d' % (_GGX, ))
    assert _GGX == 2_999

@Test.case(setup=lambda: _setupX(), 
           cleanup=lambda: _cleanupX(), 
           _no_op=lambda: _no_opX())
def test_cleanup_works_even_if_setup_fails_and_then_breaks():
    ...
