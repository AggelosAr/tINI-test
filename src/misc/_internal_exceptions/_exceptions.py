from typing import assert_never


class _LastOpNotExpected(Exception):

    def __init__(self, _ = ''):
        super().__init__('Cleanup logic failed.')


class _FailStateWasNotFail(Exception):

    def __init__(self, _ = ''):
        super().__init__('Tried to set the fail state with a success or no op state.')
        assert_never()
