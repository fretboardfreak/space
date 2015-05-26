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

from .base import LibModelTest, ModelObjectTest, StateMixinTest

from lib import model
from lib.model import galaxy


class TestLibModelGalaxy(LibModelTest):
    def setUp(self):
        self.expected_exports = [galaxy.Galaxy]


class TestGalaxy(ModelObjectTest, StateMixinTest):
    def setUp(self):
        super().setUp()
        self.expected_state = (list,)
        self.classname_in_repr = True
        self.expected_attrs = {}

    def get_new_instance(self):
        return galaxy.Galaxy()

    def get_tst_state(self):
        return ([],)

    def test_system(self):
        coord = model.Coord(1.3, 1.2, 4)
        galaxy = self.get_new_instance()
        system = galaxy.system(coord)
        system_coord = model.SystemCoord(1.3, 1.2)
        self.assertEqual(system, galaxy._systems[system_coord])

    def test_planet(self):
        system_coord = model.SystemCoord(7.6, 4.6)
        galaxy = self.get_new_instance()
        system = galaxy.system(system_coord)
        planet_index = randint(0, system.size - 1)
        coord = model.Coord(system_coord.x, system_coord.y, planet_index)
        planet = galaxy.planet(coord)
        self.assertEqual(planet, system.planets[planet_index])
