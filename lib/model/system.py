import random
from functools import partial

from planet import Planet

class System(object):
    _size_range = (2, 15)
    def __init__(self):
        self._size = random.randint(*self._size_range)
        _brightness_upper_bound = 1000 if self._size > 7 else 500
        _brightness_lower_bound = 10 if self._size <= 7 else 400
        self.sun_brightness = random.randint(_brightness_lower_bound,
                                             _brightness_upper_bound)
        cb = lambda distance: (self.sun_brightness, distance)
        self.planets = [Planet(sun_data_cb=partial(cb, i+1))
                        for i in range(self._size)]

    def __repr__(self):
        return ("System(size=%s, sun_brightness=%s, planets=%s)" %
                (self._size, self.sun_brightness, self.planets))

    def show(self, coords=None):
        msg = "%s planet system"
        if coords is not None:
            msg += " at %s" % coords
        msg += "\n[%s]" % ', '.join([p.show() for p in self.planets])
        return msg
