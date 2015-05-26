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
from collections import Callable
from unittest.mock import Mock

from tests.base import SpaceTest
from .base import (LibModelTest, ModelObjectTest, StateMixinTest,
                   EqualityMixinTest)

from lib.error import ObjectNotFound
from lib.model import building
from lib import model


class TestLibModelBuilding(LibModelTest):
    def setUp(self):
        self.expected_exports = [
            building.Mine, building.SolarPowerPlant, building.ALL_BUILDINGS,
            building.get_building, building.get_all_building_names,
            building.get_all_building_abbr]


class TestBuildingModule(SpaceTest):
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

    def test_are_requirements_met_resources(self):
        site = Mock(spec=model.Planet)
        bld = building.Mine
        site.resources = model.Resources()
        self.assertFalse(bld.are_requirements_met(site, level=1))

        site.resources.ore = 11
        self.assertTrue(bld.are_requirements_met(site))

    def test_are_requirements_met_buildings(self):
        self.skipTest('NI: Need to have buildings with building '
                      'requirements to test.')

    def test_are_requirements_met_research(self):
        self.skipTest('NI: Need to have buildings with research '
                      'requirements to test.')


class TestBuildingRequirements(ModelObjectTest, StateMixinTest):
    def get_new_instance(self):
        return building.BuildingRequirements()

    def get_tst_state(self):
        return (model.Resources(ore=3, metal=11), {'Mine', 3}, {})

    def setUp(self):
        self.object = self.get_new_instance()
        self.expected_attrs = {'resources': model.Resources,
                               'research': dict,
                               'buildings': dict}
        self.classname_in_repr = True
        self.expected_state = (model.Resources, dict, dict)

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


class TestBuildingBaseClass(ModelObjectTest, EqualityMixinTest):
    def get_new_instance(self, level=None):
        return building.Building(level=level)

    def setUp(self):
        self.max_level = 1000  # max level to consider for these tests
        self.sun_energy = 1  # must return int > 0
        self.level = random.randint(0, self.max_level)
        self.expected_state = (int, Callable)
        self.expected_attrs = {'level': int, 'modifier': model.Resources,
                               'requirements': building.BuildingRequirements,
                               'name': str, 'abbr': str}
        self.expected_modifier_type = model.Resources
        self.expected_requirements_type = building.BuildingRequirements
        self.object = self.get_new_instance()
        self.classname_in_repr = True

    def filter_presentation_attrs(self):
        self.expected_attrs.pop('name')
        self.expected_attrs.pop('abbr')

    def test_str(self):
        self.filter_presentation_attrs()
        super().test_str()

    def test_repr(self):
        self.filter_presentation_attrs()
        super().test_repr()

    def get_equal_tst_values(self):
        self.object = self.get_new_instance(self.level)
        return self.get_new_instance(self.level)

    def get_non_equal_tst_values(self):
        self.object = self.get_new_instance(self.level)
        return self.get_new_instance(self.level+1)

    def test_constructor(self):
        no_arg = self.get_new_instance()
        self.assertEqual(1, no_arg.level)
        arg = self.get_new_instance(level=self.level)
        self.assertEqual(self.level, arg.level)

    def test_modifier(self):
        self.assertIsInstance(self.object.modifier,
                              self.expected_modifier_type)

    def test_electricity(self):
        self.assertGreaterEqual(self.object.electricity(self.sun_energy), 0)

    def test_requirements(self):
        self.assertIsInstance(self.object.requirements,
                              self.expected_requirements_type)

    def test_compare(self):
        """
        Although value is based on level, modifier and electricity values
        the modifier and electricity values are calculated based on level.
        """
        test_obj = self.get_non_equal_tst_values()
        test_val = self.object._compare(test_obj)
        assert_a, _ = self.get_equality_assert_methods()
        assert_a(test_val < 0)
        test_val = test_obj._compare(self.object)
        assert_a(test_val > 0)


class TestMine(TestBuildingBaseClass):
    def get_new_instance(self, level=None):
        return building.Mine(level=level)

    def setUp(self):
        super().setUp()
        self.disable_prediction = False
        self.negative_equality_logic = False

    def test_electricity(self):
        self.assertLessEqual(self.object.electricity(self.sun_energy), 0)

    def predict_avg(self):
        low = self.get_new_instance(self.level)
        high = self.get_new_instance(self.level+1)
        retval = ((high.level - low.level) +
                  (high.modifier.trade_value - low.modifier.trade_value)) / 2.0
        return retval

    def get_non_equal_tst_values(self):
        if not self.disable_prediction:
            avg = self.predict_avg()
            self.negative_equality_logic = ((avg < 0) is True)
        return super().get_non_equal_tst_values()

    def test_not_equal_eq_ne(self):
        self.disable_prediction = True
        super().test_not_equal_eq_ne()

    def test_compare(self):
        self.disable_prediction = False
        super().test_compare()


class TestSolarPowerPlant(TestBuildingBaseClass):
    def get_new_instance(self, level=None):
        return building.SolarPowerPlant(level=level)

    def test_electricity(self):
        for level in range(1000):
            self.level = level
            test_spp = self.get_non_equal_tst_values()
            self.assertLessEqual(self.object.electricity(self.sun_energy),
                                 test_spp.electricity(self.sun_energy))
