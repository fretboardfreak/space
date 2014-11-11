from logging import debug

class ObjectNotFound(Exception):
    def __init__(self, name=None):
        msg = 'Object Not Found'
        extra = ': %s'
        if name:
            msg += extra % name
        super(ObjectNotFound, self).__init__(msg)
        debug(msg)
