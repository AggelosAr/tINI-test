from src.utils import Test


GG = 0

def setup():
    global GG
    assert GG == 0
    print('inside setup current val-> %d' % (GG, ))
    GG = 1_000
    print('inside setup updated val-> %d' % (GG, ))

@Test.case(setup=lambda: setup())
def test_setup_provided():
    print('inside test_setup_provided val-----------> %d' % (GG, ))
    assert GG == 1_000
