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
import re

from lib.model import resources
from lib.model import building


class TestModel(unittest.TestCase):
    def test_model(self):
        expected_exports = ['Mine', 'SolarPowerPlant', 'ALL_BUILDINGS',
                            'get_building', 'get_all_building_names',
                            'get_all_building_abbr']
        import lib.model
        for export in expected_exports:
            self.assertIn(export, lib.model.__all__)


@unittest.skip('not implemented yet')
class TestBuildingModule(unittest.TestCase):
    def test_all_buildings_list(self):
        pass

    def test_get_all_buildings(self):
        pass

    def test_get_all_abbr(self):
        pass

    def test_get_building(self):
        pass


@unittest.skip('not implemented yet')
class TestBuildingSubclasses(unittest.TestCase):
    def building_subclasses_have_names(self):
        pass

    def building_subclasses_have_abbr(self):
        pass


class TestBuildingRequirements(unittest.TestCase):
    def setUp(self):
        self.expected_attrs = {'resources': resources.Resources,
                               'research': dict,
                               'buildings': dict}
        self.reqs = building.BuildingRequirements()

    def assert_attrs_in_string(self, string):
        lower = string.lower()
        for attr in self.expected_attrs:
            pattern = '{}: '.format(attr)
            self.assertIn(pattern, lower)

    def test_repr(self):
        rep = repr(self.reqs)
        self.assertTrue(rep.startswith('BuildingRequirements('))
        self.assertTrue(rep.endswith(')'))
        self.assertEqual(0, rep.count('\n'))
        self.assert_attrs_in_string(rep)

    def test_str(self):
        string = str(self.reqs)
        self.assertEqual(2, string.count('\n'))
        self.assert_attrs_in_string(string)

    def test_attrs(self):
        for attr in self.expected_attrs:
            self.assertIn(attr, dir(self.reqs))
            self.assertIsInstance(getattr(self.reqs, attr),
                                  self.expected_attrs[attr])


@unittest.skip('not implemented yet')
class TestBuildingBaseClass(unittest.TestCase):
    pass


class BaseBuildingTest(unittest.TestCase):
    pass
