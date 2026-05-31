

class TooManyArgumentsGivenDirAndFile(Exception):

    def __init__(self, _ = ''):
        super().__init__('Module collector should accept either a directory or a file.')


class CantFindRelativePathToRoot(Exception):

    def __init__(self, _ = ''):
        super().__init__("Can't find the requested relative path to root.")


class NotSupportedMode(Exception):

    def __init__(self, msg):
        super().__init__(msg)


class TestNotFound(Exception):

    def __init__(self, _ = ''):
        super().__init__('Test function was not found.')


class WillRaiseReceivedNotAnException(Exception):

    def __init__(self, _ = ''):
        super().__init__('Objects passed to WillRaise should be exceptions.')
