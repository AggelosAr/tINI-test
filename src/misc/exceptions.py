

from typing import Any, Type


class TooManyArgumentsGivenDirAndFile(Exception):

    def __init__(self) -> None:
        super().__init__('Module collector should accept either a directory or a file.')


class CantFindRelativePathToRoot(Exception):

    def __init__(self) -> None:
        super().__init__("Can't find the requested relative path to root.")


class NotSupportedMode(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class TestNotFound(Exception):

    def __init__(self) -> None:
        super().__init__('Test function was not found.')


class WillRaiseReceivedNotAnException(Exception):

    def __init__(self) -> None:
        super().__init__('Objects passed to WillRaise should be exceptions.')


class ExpectedWasDifferentFromActual(Exception):
    def __init__(self, msg: str = '') -> None:
        self.msg = msg
        super().__init__(msg)

    def _get_detail(self) -> str:
        return f"------DIFF------\n{self.msg}\n------DIFF------"


class MustEqualReceivedNotKnownTypes(Exception):

    def __init__(self) -> None:
        super().__init__('Pleace provide a custom compare function to the must_equals function')
