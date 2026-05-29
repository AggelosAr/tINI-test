

class LastOpNotExpected(Exception):
    def __init__(self, message, field):
        self.field = field
        super().__init__('Cleanup logic failed.')
