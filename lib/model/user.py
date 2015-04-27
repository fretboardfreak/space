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

from lib.error import ObjectNotFound
from lib.rst import indent


class User(object):
    def __init__(self, name, home_planet_coords, home_planet):
        debug('Creating new user object %s' % name)
        self.name = name
        self.planets = {home_planet_coords: home_planet}
        home_planet.emperor = self.name

    def __repr__(self):
        return "{}(name: {}, planets: {})".format(
                self.__class__.__name__, self.name, self.planets)

    def __str__(self):
        return "{} name: {}\nplanets: {}".format(
                self.__class__.__name__, self.name, self.planets)

    def show_planets(self, verbose=None):
        debug("showing user %s's planets: verbose=%s" %
              (self.name, verbose))
        planets = ['Planets:']
        for coord, planet in self.planets.iteritems():
                planets.append(' %s: %s' % (coord, planet.show(verbose)))
        return '\n'.join(planets)

    def show(self, verbose=None):
        debug('showing user %s: verbose %s' % (self.name, verbose))
        planets = indent(self.show_planets(verbose), '    ')
        return ("User: %s\n%s" %
                (self.name, planets))

    def __getstate__(self):
        return (self.name, self.planets)

    def __setstate__(self, state):
        (self.name, self.planets) = state

    def get_planet(self, name):
        debug('retrieving planet %s' % name)
        for coord, planet in self.planets.items():
            if planet.name.lower() == name.lower():
                return (coord, planet)
        raise ObjectNotFound(name)
