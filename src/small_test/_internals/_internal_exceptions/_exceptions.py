from typing import assert_never


class _LastOpNotExpected(Exception):

    def __init__(self, _ = ''):
        super().__init__('<small-test-error> Cleanup logic failed.')
        assert_never()


class _FailStateWasNotFail(Exception):

    def __init__(self, _ = ''):
        super().__init__('<small-test-error> Tried to set the fail state with a success or no op state.')
        assert_never()
