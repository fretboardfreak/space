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

from logging import debug

from . import Coord


class User(object):
    def __init__(self, name, home_planet_coords=None):
        self.name = name
        self.planets = []
        if home_planet_coords is not None:
            self.planets.append(home_planet_coords)
        debug('Created new user {} with home planet {}'.format(
            self.name, ' '.join(repr(pl) for pl in self.planets)))

    def __repr__(self):
        return "{}(name: {}, planets: {})".format(
            self.__class__.__name__, self.name, self.planets)

    def __str__(self):
        return "{} name: {}\nplanets: {}".format(
            self.__class__.__name__, self.name, self.planets)

    def __getstate__(self):
        planets = [coord.__getstate__() for coord in self.planets]
        return (self.name, planets)

    def __setstate__(self, state):
        (self.name, planets) = state
        self.planets = []
        for pl in planets:
            coord = Coord()
            coord.__setstate__(pl)
            self.planets.append(coord)
