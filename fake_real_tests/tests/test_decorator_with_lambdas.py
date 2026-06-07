from tini_test.must_equals import must_equal
from tini_test.test import Test

###############################################################################
# POSITIVE GLOBAL STATE HELPERS
###############################################################################

# --------------------------
# CASE 1: setup=setup, cleanup=cleanup
# --------------------------

_GG_POS_R = 0


def setup_pos_r():
    global _GG_POS_R
    must_equal(0, _GG_POS_R)
    _GG_POS_R = 10


def cleanup_pos_r():
    global _GG_POS_R
    must_equal(20, _GG_POS_R)
    _GG_POS_R = 30


def no_op_pos_r():
    global _GG_POS_R
    must_equal(30, _GG_POS_R)


@Test.case(setup=setup_pos_r, cleanup=cleanup_pos_r, _no_op=no_op_pos_r)
def test_setup_provided_pos_r():
    global _GG_POS_R
    must_equal(10, _GG_POS_R)
    _GG_POS_R = 20


# --------------------------
# CASE 2: setup=lambda: setup(), cleanup=lambda: cleanup()
# --------------------------

_GG_POS_R_L = 0


def _setup_pos_r_l():
    global _GG_POS_R_L
    must_equal(0, _GG_POS_R_L)
    _GG_POS_R_L = 100


def _cleanup_pos_r_l():
    global _GG_POS_R_L
    must_equal(200, _GG_POS_R_L)
    _GG_POS_R_L = 300


def no_op_pos_r_l():
    global _GG_POS_R_L
    must_equal(300, _GG_POS_R_L)


@Test.case(
    setup=lambda: _setup_pos_r_l(),
    cleanup=lambda: _cleanup_pos_r_l(),
    _no_op=no_op_pos_r_l,
)
def test_setup_provided_pos_r_l():
    global _GG_POS_R_L
    must_equal(100, _GG_POS_R_L)
    _GG_POS_R_L = 200


###############################################################################
# KEYWORD USAGE
###############################################################################

# --------------------------
# CASE 3: setup, cleanup (positional)
# --------------------------

_GG_KEY_R = 0


def setup_key_r():
    global _GG_KEY_R
    must_equal(0, _GG_KEY_R)
    _GG_KEY_R = 1000


def cleanup_key_r():
    global _GG_KEY_R
    must_equal(2000, _GG_KEY_R)
    _GG_KEY_R = 3000


def no_op_key_r():
    global _GG_KEY_R
    must_equal(3000, _GG_KEY_R)


@Test.case(setup_key_r, cleanup_key_r, _no_op=no_op_key_r)
def test_setup_provided_key_r():
    global _GG_KEY_R
    must_equal(1000, _GG_KEY_R)
    _GG_KEY_R = 2000


# --------------------------
# CASE 4: lambda: setup(), lambda: cleanup()
# --------------------------

_GG_KEY_R_L = 0


def _setup_key_r_l():
    global _GG_KEY_R_L
    must_equal(0, _GG_KEY_R_L)
    _GG_KEY_R_L = 10000


def _cleanup_key_r_l():
    global _GG_KEY_R_L
    must_equal(20000, _GG_KEY_R_L)
    _GG_KEY_R_L = 30000


def no_op_key_r_l():
    global _GG_KEY_R_L
    must_equal(30000, _GG_KEY_R_L)


@Test.case(
    lambda: _setup_key_r_l(),
    lambda: _cleanup_key_r_l(),
    _no_op=no_op_key_r_l,
)
def test_setup_provided_key_r_l():
    global _GG_KEY_R_L
    must_equal(10000, _GG_KEY_R_L)
    _GG_KEY_R_L = 20000