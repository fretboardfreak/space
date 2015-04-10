from collections import defaultdict, UserDict

class AttrDict(UserDict):
    """ Dictionary who's keys become attributes.

        Causes memory leak on python < 2.7.3 and python < 3.2.3
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class DefaultAttrDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DefaultAttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getattribute__(self, name):
        try:
            return super(DefaultAttrDict, self).__getattribute__(name)
        except AttributeError:
            return self[name]
