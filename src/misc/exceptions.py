

class LastOpNotExpected(Exception):

    def __init__(self, message = ''):
        super().__init__('Cleanup logic failed.')
