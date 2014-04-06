import random

from planet import Planet

class System(object):
    def __init__(self):
        self._size_range = (4, 20)
        self.planets = [Planet() for i in
                        range(random.randint(*self._size_range))]

    def __repr__(self):
        return ("System(size=%s, planets=%s)" %
                (self._size_range, self.planets))

    def show(self, coords=None):
        msg = "%s planet system"
        if coords is not None:
            msg += " at %s" % coords
        msg += "\n[%s]" % ', '.join([p.show() for p in self.planets])
        return msg
