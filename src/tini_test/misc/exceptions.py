

class NotSupportedVerbosity(Exception):

    def __init__(self, reason: str = ''):
        super().__init__(reason)


class NotSupportedRunMode(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)


class CantFindRelativePathToRoot(Exception):

    def __init__(self) -> None:
        super().__init__("Can't find the requested relative path to root.")


class TestNotFound(Exception):

    def __init__(self) -> None:
        super().__init__('Test function was not found.')


class WillRaiseReceivedNotAnException(Exception):

    def __init__(self) -> None:
        super().__init__('Objects passed to WillRaise should be exceptions.')


class ExpectedWasDifferentFromActual(Exception):
    def __init__(self, msg: str = '') -> None:
        super().__init__(msg)
        self.msg = msg
    
    def _get_detail(self) -> str:
        return f'\n{self.msg}\n'

  
class ComperatorWasNotProvided(Exception):

    def __init__(self) -> None:
        super().__init__('Unknown type encountered and a comperator was not provided.')


class ComperatorIsNotValid(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)


class ExceptionWasNotRaised(Exception):

    def __init__(self, reason: str = '') -> None:
        super().__init__(reason)