from typing import assert_never


class TooManyArgumentsDirAndFile(Exception):

    def __init__(self, _ = ''):
        super().__init__('Module collector should accept either a directory or a file.')


class CantFindRelativePathToRoot(Exception):

    def __init__(self, _ = ''):
        super().__init__("Can't find the requested relative path to root.")


class NotSupportedMode(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class TestFunctionNotFound(Exception):

    def __init__(self, _ = ''):
        super().__init__('Test function was not found.')


class LastOpNotExpected(Exception):

    def __init__(self, _ = ''):
        super().__init__('Cleanup logic failed.')


class FailStateWasNotFail(Exception):

    def __init__(self, _ = ''):
        super().__init__('Tried to set the fail state with a success or no op state.')
        assert_never()
