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
    from tini_test.mock import MockDefinition

    with WillRaise(TiniTestInternalException) as context:
        import inspect

        from tini_test._internals.consts import _R_M_REG

        new_frame = inspect.currentframe()
        del new_frame.f_globals[_R_M_REG]
        MockDefinition._CX_get_globals(new_frame)

    must_equal('Global registry for mocks not found', str(context.exception))


    with WillRaise(TiniTestInternalException) as context:
        MockDefinition._CX_get_real_test(None)

    must_equal('Frame is None', str(context.exception))


    with WillRaise(TiniTestInternalException) as context:
        import inspect

        from tini_test._internals.consts import _R_M_REG
        
        new_frame = inspect.currentframe()
        new_frame.f_globals[_R_M_REG] = 'x'
        MockDefinition._CX_get_real_test(new_frame)
    
    must_equal('Real test not found', str(context.exception))
    