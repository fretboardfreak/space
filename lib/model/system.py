# Copyright 2015 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from random import randint
from logging import debug

from .planet import Planet


class System(object):
    size_range = (2, 15)

    def __init__(self):
        self.size = randint(*self.size_range)
        self.sun_brightness = randint(*self.get_brightness_bounds(self.size))
        debug('Constructing new system of size %s with sun brightness %s' %
              (self.size, self.sun_brightness))
        self.planets = [Planet(sun_brightness=self.sun_brightness,
                               sun_distance=i)
                        for i in range(1, self.size+1)]

    def __repr__(self):
        return "{}(Size: {}, Sun Brightness: {}, Planets: {})".format(
            self.__class__.__name__, self.size, self.sun_brightness,
            self.planets)

    def __str__(self):
        return "{}: Size: {}, Sun Brightness: {}\nPlanets:\n{}".format(
            self.__class__.__name__, self.size, self.sun_brightness,
            self.planets)

    def __getstate__(self):
        return (self.size, self.sun_brightness, self.planets)

    def __setstate__(self, state):
        (self.size, self.sun_brightness, self.planets) = state

    def __eq__(self, other):
        return (self.size == other.size and
                self.sun_brightness == other.sun_brightness and
                self.planets == other.planets)

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def get_brightness_bounds(cls, size):
        size_scale = 7
        _brightness_upper_bound = 1000 if size > size_scale else 500
        _brightness_lower_bound = 10 if size <= size_scale else 400
        return (_brightness_lower_bound, _brightness_upper_bound)
