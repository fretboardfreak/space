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
        return system.planets[int(coord.planet)]

    def __repr__(self):
        systems = ','.join('{}: {}'.format(coord, repr(system))
                           for coord, system in self._systems.items())
        return "{}(systems: [{}])".format(self.__class__.__name__, systems)

    def __str__(self):
        systems = '\n'.join('{}: {}'.format(coord, str(system))
                            for coord, system in self._systems.items())
        systems.replace('\n', '\n    ')  # indent the systems a bit
        return '{}: systems:\n{}'.format(self.__class__.__name__, systems)

    def __getstate__(self):
        systems = []
        for coord in dict(self._systems):
            systems.append((coord.__getstate__(),
                            self._systems[coord].__getstate__()))
        return (systems,)

    def __setstate__(self, state):
        systems = state[0]
        self._systems = defaultdict(System)
        for coord_state, system_state in systems:
            coord = SystemCoord()
            coord.__setstate__(coord_state)
            sys_obj = System()
            sys_obj.__setstate__(system_state)
            self._systems[coord] = sys_obj
