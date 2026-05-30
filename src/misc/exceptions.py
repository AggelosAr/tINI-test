

class LastOpNotExpected(Exception):

    def __init__(self, _ = ''):
        super().__init__('Cleanup logic failed.')



class TooManyArgumentsDirAndFile(Exception):

    def __init__(self, _ = ''):
        super().__init__('Module collector should accept either a directory or a file')


class CantFindRelativePathToRoot(Exception):

    def __init__(self, _ = ''):
        super().__init__("Can't find the requested relative path to root")
