from src.utils import Test


GG = 0

def setup():
    global GG
    print('setup called GG-> %d' % (GG, ))
    GG = 1_000
    print('setup called GG-> %d' % (GG, ))

@Test.case(setup=lambda: setup())
def test_setup_provided():
    print('inside test_setup_provided GG-----------> %d' % (GG, ))
    assert GG == 1_000

