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

class BaseCoord(object):
    def __init__(self, x=None, y=None):
        if x is None:
            x = 0
        if y is None:
            y = 0
        self.x = str(float(x))
        self.y = str(float(y))

    @property
    def sector(self):
        return (int(self.x.split('.')[0]),
                int(self.y.split('.')[0]))

    @sector.setter
    def sector(self, value):
        sec_x = str(int(value[0]))
        sec_y = str(int(value[1]))
        self.x = '.'.join([sec_x, str(self.x).split('.')[1]])
        self.y = '.'.join([sec_y, str(self.y).split('.')[1]])

    @property
    def system(self):
        return (int(self.x.split('.')[1]),
                int(self.y.split('.')[1]))

    @system.setter
    def system(self, value):
        sys_x = str(int(value[0]))
        sys_y = str(int(value[1]))
        self.x = '.'.join([str(self.x).split('.')[0], sys_x])
        self.y = '.'.join([str(self.y).split('.')[0], sys_y])

    def __ne__(self, other):
        return not self.__eq__(other)


class Coord(BaseCoord):
    def __init__(self, x=None, y=None, planet=None):
        if planet is None:
            planet = 0
        self.planet = str(int(planet))
        super().__init__(x, y)

    def __eq__(self, other):
        return (other.x == self.x and
                other.y == self.y and
                other.planet == self.planet)

    def __hash__(self):
        return hash((self.x, self.y, self.planet))

    def __repr__(self):
        return "Coord({}, {}, {})".format(self.x, self.y, self.planet)

    def __str__(self):
        return str((self.x, self.y, self.planet))

    def __getstate__(self):
        return (self.x, self.y, self.planet)

    def __setstate__(self, state):
        self.x, self.y, self.planet = state


class SystemCoord(Coord):
    def __init__(self, x=None, y=None):
        super().__init__(x, y, None)
        del(self.planet)

    def __eq__(self, other):
        return (other.x == self.x and
                other.y == self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "SystemCoord({}, {})".format(self.x, self.y)

    def __str__(self):
        return str((self.x, self.y))

    def __getstate__(self):
        return (self.x, self.y)

    def __setstate__(self, state):
        self.x, self.y = state
