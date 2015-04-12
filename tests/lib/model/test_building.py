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

import unittest
import random

from .base import LibModelTest, ModelObjectTest

from lib.error import ObjectNotFound
from lib.model import resources
from lib.model import building


class TestLibModelBuilding(LibModelTest):
    def setUp(self):
        self.expected_exports = ['Mine', 'SolarPowerPlant', 'ALL_BUILDINGS',
                                 'get_building', 'get_all_building_names',
                                 'get_all_building_abbr']


class TestBuildingModule(unittest.TestCase):
    def setUp(self):
        self.expected_building_classes = ['Mine', 'SolarPowerPlant']
        self.expected_building_names = ['Mine', 'Solar Power Plant']
        self.expected_building_abbrs = ['Mn', 'SPP']

    def _get_building_subclass_count(self):
        building_subclass_count = 0
        for attr in dir(building):
            obj = getattr(building, attr, None)
            if not isinstance(obj, type):
                continue
            if obj and obj.__base__ is building.Building:
                building_subclass_count += 1
        return building_subclass_count

    def test_expected_vars(self):
        """Try to catch developer ommissions"""
        subclass_count = self._get_building_subclass_count()
        self.assertEqual(subclass_count, len(self.expected_building_classes))
        self.assertEqual(subclass_count, len(self.expected_building_names))
        self.assertEqual(subclass_count, len(self.expected_building_abbrs))

    def test_all_buildings_list(self):
        self.assertEqual(len(self.expected_building_classes),
                         len(building.ALL_BUILDINGS))
        all_building_names = [bld.__name__ for bld in building.ALL_BUILDINGS]
        for bldng in self.expected_building_classes:
            self.assertIn(bldng, all_building_names)

    def test_get_all_building_names(self):
        all_building_names = building.get_all_building_names()
        self.assertEqual(set(all_building_names),
                         set(self.expected_building_names))

    def test_get_all_building_abbr(self):
        all_building_abbr = building.get_all_building_abbr()
        self.assertEqual(set(all_building_abbr),
                         set(self.expected_building_abbrs))

    def test_get_building_not_found(self):
        self.assertRaises(ObjectNotFound, building.get_building, 'flabber')

    def test_get_building_type_no_level(self):
        for building_type in building.ALL_BUILDINGS:
            test_val = building.get_building(building_type)
            self.assertEqual(building_type, test_val)

    def test_get_building_name_no_level(self):
        for building_type in building.ALL_BUILDINGS:
            test_val = building.get_building(building_type.name)
            self.assertEqual(building_type, test_val)

    def test_get_building_abbr_no_level(self):
        for building_type in building.ALL_BUILDINGS:
            test_val = building.get_building(building_type.abbr)
            self.assertEqual(building_type, test_val)

    def test_get_building_type(self):
        level = 1
        for building_type in building.ALL_BUILDINGS:
            test_val = building.get_building(building_type, level=level)
            self.assertIsInstance(test_val, building_type)

    def test_get_building_name(self):
        level = 1
        for building_type in building.ALL_BUILDINGS:
            test_val = building.get_building(building_type.name, level=level)
            self.assertIsInstance(test_val, building_type)

    def test_get_building_abbr(self):
        level = 1
        for building_type in building.ALL_BUILDINGS:
            test_val = building.get_building(building_type.abbr, level=level)
            self.assertIsInstance(test_val, building_type)


class TestBuildingRequirements(ModelObjectTest):
    def get_new_instance(self):
        return building.BuildingRequirements()

    def setUp(self):
        self.object = self.get_new_instance()
        self.expected_attrs = {'resources': resources.Resources,
                               'research': dict,
                               'buildings': dict}
        self.classname_in_repr = True

    def test_repr(self):
        super().test_repr()
        rep = repr(self.object)
        self.assertTrue(rep.startswith('BuildingRequirements('))
        self.assertTrue(rep.endswith(')'))
        self.assertEqual(0, rep.count('\n'))
        self.assert_attrs_in_string(rep)

    def test_str(self):
        super().test_str()
        string = str(self.object)
        self.assertEqual(2, string.count('\n'))


class TestBuildingBaseClass(unittest.TestCase):
    pass


class BaseBuildingTest(unittest.TestCase):
    pass


class TestMine(BaseBuildingTest):
    pass


class TestSolarPowerPlant(BaseBuildingTest):
    pass
