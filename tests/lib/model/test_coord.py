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

import random
import re

from tests.base import SpaceTest
from .base import LibModelTest

from lib.model import coord


class TestLibModelCoord(LibModelTest):
    def setUp(self):
        self.expected_exports = [coord.Coord, coord.SystemCoord]


class BaseCoordTest(SpaceTest):
    def setUp(self):
        self.object = coord.Coord(0, 0, 0)

    def test_sector(self):
        self._property_test('sector')

    def test_system(self):
        self._property_test('system')

    def _property_test(self, name):
        if name == 'planet':
            test_value = self.get_tst_values(planet=True)
        else:
            test_value = self.get_tst_values(planet=False)
        setattr(self.object, name, test_value)
        self.assertEqual(getattr(self.object, name), test_value)

    def get_tst_values(self, planet=False):
        count = 2
        if planet:
            count = 1
        return tuple([random.randint(0, 1000) for _ in range(count)])


class TestCoord(BaseCoordTest):
    def test_planet(self):
        self._property_test('planet')

    def test_hash(self):
        start_hash = hash(self.object)
        test_sector = self.get_tst_values()
        test_system = self.get_tst_values()
        test_planet = self.get_tst_values(planet=True)
        example_coord = coord.Coord()
        self.assertEqual(hash(example_coord), start_hash)
        example_coord.sector = test_sector
        example_coord.system = test_system
        example_coord.planet = test_planet
        self.object.sector = test_sector
        self.object.system = test_system
        self.object.planet = test_planet
        self.assertEqual(hash(self.object), hash(example_coord))

    def test_repr(self):
        expected = 'Coord\(\d\.\d, \d\.\d, \d\)'
        self.assertTrue(re.search(expected, repr(self.object)))

    def test_str(self):
        expected = '\(\'\d\.\d\', \'\d\.\d\', \'\d\'\)'
        self.assertTrue(re.search(expected, str(self.object)))

    def test_getstate(self):
        expected = ('0.0', '0.0', '0')
        self.assertEqual(expected, self.object.__getstate__())

    def test_setstate(self):
        self.object.sector = self.get_tst_values()
        self.object.system = self.get_tst_values()
        self.object.planet = self.get_tst_values(planet=True)
        test_obj = coord.Coord()
        test_obj.__setstate__((self.object.x, self.object.y,
                               self.object.planet))
        self.assertEqual((self.object.x, self.object.y, self.object.planet),
                         (test_obj.x, test_obj.y, test_obj.planet))


class TestSystemCoord(BaseCoordTest):
    def setUp(self):
        self.object = coord.SystemCoord(0, 0)

    def test_no_planet(self):
        self.assertFalse(hasattr(self.object, 'planet'))

    def test_hash(self):
        start_hash = hash(self.object)
        test_sector = self.get_tst_values()
        test_system = self.get_tst_values()
        example_coord = coord.SystemCoord()
        self.assertEqual(hash(example_coord), start_hash)
        example_coord.sector = test_sector
        example_coord.system = test_system
        self.object.sector = test_sector
        self.object.system = test_system
        self.assertEqual(hash(self.object), hash(example_coord))

    def test_getstate(self):
        expected = ('0.0', '0.0')
        self.assertEqual(expected, self.object.__getstate__())

    def test_repr(self):
        expected = 'SystemCoord\(\d\.\d, \d\.\d\)'
        self.assertTrue(re.search(expected, repr(self.object)))

    def test_str(self):
        expected = '\(\'\d\.\d\', \'\d\.\d\'\)'
        self.assertTrue(re.search(expected, str(self.object)))

    def test_setstate(self):
        self.object.sector = self.get_tst_values()
        self.object.system = self.get_tst_values()
        test_obj = coord.SystemCoord()
        test_obj.__setstate__((self.object.x, self.object.y))
        self.assertEqual((self.object.x, self.object.y),
                         (test_obj.x, test_obj.y))
