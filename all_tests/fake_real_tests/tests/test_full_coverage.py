from tini_test import Test
from tini_test.context_managers import WillRaise
from tini_test.enums import RunMode, ScoreClass, TestStatus
from tini_test.misc.exceptions import TiniTestInternalException
from tini_test.must_equals import must_equal

# Some tests to satisfy coverage...

@Test.case
def test_RunMode_arg_parser_type():
    must_equal(RunMode.SYNC, RunMode.arg_parser_type('sync'))
    must_equal(RunMode.ASYNC, RunMode.arg_parser_type('async'))


@Test.case
def test_ScoreClass_get_score_category():
    must_equal(ScoreClass.EXCELLENT, ScoreClass.get_score_category(95))
    must_equal(ScoreClass.AVERAGE, ScoreClass.get_score_category(75))
    must_equal(ScoreClass.POOR, ScoreClass.get_score_category(49))


@Test.case
def test_Isolate():
    from tini_test import Isolate

    with WillRaise(RuntimeError) as context:

        @Test.case
        @Isolate(a=10)
        def raise_error(): ...

    must_equal('Isolate does not accept keyword arguments', str(context.exception))



@Test.case
def test_create_command():
    from tini_test._internals._broken import create_command

    commands = create_command()
    must_equal(True, isinstance(commands, list))

    commands = create_command('x', 'x', 'x')
    must_equal(True, isinstance(commands, list))


@Test.case
def test_GlobalRegistry():
    from tini_test.misc.annotations import GlobalRegistry

    registry = GlobalRegistry()
    registry['x'] = 'x'
    must_equal('x', registry['x'])
    must_equal('x', registry.get('x'))


@Test.case
def test_OperationState():
    from tini_test.state.state import OperationState

    # Maybe remove this? since it `seems` that it is not used...
    state = OperationState(status=TestStatus.SUCCESS)
    state.entry_msg = ['x']
    must_equal(['x'], state.entry_msg)


@Test.case
def test_MockType_none_none():
    from tini_test.enums import MockType

    with WillRaise(TiniTestInternalException) as context:
        MockType.get_type('unsupported_mock')

    must_equal('Unsupported mock type', str(context.exception))


@Test.case
def mock_internals_for_mock():
    import inspect
    from tini_test.mock import Mocking
    from tini_test._internals.consts import _R_M_REG, _R_T_REG

    with WillRaise(TiniTestInternalException) as context:
        Mocking(None)._rewind_frames()

    must_equal("Can't rewind frames from a None frame", str(context.exception))

    frame = inspect.currentframe()
    assert frame is not None
    mocking = Mocking(frame)
    mocking.rewinded_frames = [frame]

    missing = object()
    mock_registry = frame.f_globals.pop(_R_M_REG, missing)
    try:
        with WillRaise(TiniTestInternalException) as context:
            _ = mocking.frame_globals
    finally:
        if mock_registry is not missing:
            frame.f_globals[_R_M_REG] = mock_registry

    must_equal('Global registry for mocks not found', str(context.exception))

    with WillRaise(TiniTestInternalException) as context:
        old_mock_registry = frame.f_globals.get(_R_M_REG, missing)
        old_test_registry = frame.f_globals.get(_R_T_REG, missing)
        frame.f_globals[_R_M_REG] = {}
        frame.f_globals[_R_T_REG] = {}
        try:
            _ = mocking.real_test
        finally:
            if old_mock_registry is missing:
                frame.f_globals.pop(_R_M_REG, None)
            else:
                frame.f_globals[_R_M_REG] = old_mock_registry
            if old_test_registry is missing:
                frame.f_globals.pop(_R_T_REG, None)
            else:
                frame.f_globals[_R_T_REG] = old_test_registry

    must_equal('Real test not found', str(context.exception))
    