

class WillRaise(object):

    def __init__(self, *exceptions):
        self.exceptions = exceptions
        # TODO validate 
        # print('Objects passed to WillRaise must be exceptions.')

    def __enter__(self):
        return self.exceptions

    def __exit__(self, exc_type, exc, exc_tb):
        if exc_type in self.exceptions:
            return True

