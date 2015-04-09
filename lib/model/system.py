from random import randint
from logging import debug

from .planet import Planet


__all__ = ['System']


class System(object):
    _size_range = (2, 15)
    def __init__(self):
        self.size = randint(*self._size_range)
        _brightness_upper_bound = 1000 if self.size > 7 else 500
        _brightness_lower_bound = 10 if self.size <= 7 else 400
        self.sun_brightness = randint(_brightness_lower_bound,
                                      _brightness_upper_bound)
        debug('Constructing new system of size %s with sun brightness %s' %
              (self.size, self.sun_brightness))
        self.planets = [Planet(sun_brightness=self.sun_brightness,
                               sun_distance=i)
                        for i in range(self.size)]

    def __repr__(self):
        return ("System(size=%s, sun_brightness=%s, planets=%s)" %
                (self.size, self.sun_brightness, self.planets))

    def show(self, coords=None):
        msg = "%s planet system"
        if coords is not None:
            msg += " at %s" % coords
        msg += "\n[%s]" % ', '.join([p.show() for p in self.planets])
        return msg

    def __getstate__(self):
        return (self.size, self.sun_brightness, self.planets)

    def __setstate__(self, state):
        (self.size, self.sun_brightness, self.planets) = state
