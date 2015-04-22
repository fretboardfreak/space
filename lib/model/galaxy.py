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

from collections import defaultdict
from logging import debug

from lib.rst import indent

from .system import System
from .coord import SystemCoord


class Galaxy(object):
    def __init__(self):
        self._systems = defaultdict(System)

    def system(self, coord):
        system_coord = SystemCoord(coord.x, coord.y)
        debug('looking up system: %s' % system_coord)
        return self._systems[system_coord]

    def planet(self, coord):
        system = self.system(coord)
        debug('looking up planet: %s' % coord)
        return system.planets[coord.planet]

    def __repr__(self):
        systems = ','.join(['{}: {}'.format(coord, repr(system))
                            for coord, system in self._systems.items()])
        return "{}(systems: [{}])".format(self.__class__.__name__, systems)

    def __str__(self):
        systems = '\n'.join(['{}: {}'.format(coord, str(system))
                             for coord, system in self._systems.items()])
        systems.replace('\n', '\n    ')  # indent the systems a bit
        return '{}: systems:\n{}'.format(self.__class__.__name__, systems)

    def show(self):
        systems = []
        debug('showing the galaxy...')
        for c, s in self._systems.iteritems():
            sys = indent(s.show(), '  ')[2:]
            systems.append('%s %s' % (c, sys))
        return 'Galaxy:\n%s' % indent('\n'.join(systems), '  ')

    def __getstate__(self):
        return (dict(self._systems),)

    def __setstate__(self, state):
        self._systems = defaultdict(System, state[0])
