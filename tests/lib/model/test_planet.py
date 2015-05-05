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

from unittest.mock import Mock
from .base import LibModelTest, ModelObjectTest, StateMixinTest

from lib.error import ModelObjectError
from lib import model
from lib.model.building import Building
from lib.model import planet


class TestLibModelCoord(LibModelTest):
    def setUp(self):
        self.expected_exports = [planet.Planet]


class TestPlanet(ModelObjectTest, StateMixinTest):
    def setUp(self):
        self.sun_brightness = 555
        self.sun_distance = 3
        self.expected_state = (str, (str, type(None)), model.Resources,
                               (int, float), dict, int, int)
        self.classname_in_repr = True
        self.expected_attrs = {
            'max_resources': model.Resources, 'name': str,
            'emperor': (type(None), str), 'resources': model.Resources,
            'last_update': float, 'sun_brightness': int,
            'sun_distance': int, 'rates': model.Resources,
            'ore': int, 'thorium': int, 'metal': int, 'hydrocarbon': int,
            'deuterium': int, 'sun': float, 'electricity': int,
            'research': dict, 'buildings': dict}
        super().setUp()

    def get_new_instance(self):
        return planet.Planet(self.sun_brightness, self.sun_distance)

    def get_tst_state(self):
        return ('name', 'emperor', model.Resources(), 123456, {}, 555, 3)

    def set_expected_attrs_for_representation(self):
        self.expected_attrs = {
            'name': str, 'emperor': (type(None), str),
            'resources': model.Resources, 'last_update': float,
            'rates': model.Resources, 'sun': float, 'electricity': int,
            'research': dict, 'buildings': dict}

    def test_repr(self):
        self.set_expected_attrs_for_representation()
        super().test_repr()

    def test_str(self):
        self.set_expected_attrs_for_representation()

        # name and rates are shown, the actual attr strings are not
        self.expected_attrs.pop('name')
        self.expected_attrs.pop('rates')
        super().test_str()

    def test_rates(self):
        for lvl in range(10):
            self.object.buildings[lvl] = Building(lvl)
            self.object.buildings[lvl].level = lvl
        self.assertEqual(self.object.rates,
                         model.Resources(ore=sum(range(10))))

    def prep_update_tst(self):
        planet.time = Mock(return_value=110.0)
        self.object.last_update = 100.0
        time_diff = 10.0
        self.object.buildings['bld'] = Building(1)
        expected_rate = 1  # Building defaults to 1 ore per time unit
        return time_diff, expected_rate

    def test_update(self):
        time_diff, expected_rate = self.prep_update_tst()
        start_res = self.object.resources.copy()
        self.object.update()
        end_res = self.object.resources.copy()
        res_diff = end_res - start_res
        self.assertEqual(res_diff.trade_value,
                         time_diff * expected_rate)

    def test_update_max_resources(self):
        time_diff, expected_rate = self.prep_update_tst()
        max_res = self.object.max_resources.copy()
        max_res.ore -= time_diff * expected_rate
        self.object.resources = max_res.copy()
        self.object.update()
        self.assertEqual(self.object.resources,
                         self.object.max_resources)

    def test_update_no_available_resources(self):
        """
        Test behaviour of the planet when consumtion is higher than
        production and the resources stockpile runs out.
        """
        self.skipTest('NI: Need to determine desired '
                      'behaviour here. Deferring tests for now.')

    def test_build(self):
        self.skipTest('NI')
        # no-blding -> lvl 1 vs lvl x -> lvl x+1
        # building reqs met vs not met (resources, bldings, research)
        # costs removed from planet

    def test_get_available_buildings(self):
        expected = [
            (model.Mine, 1, model.Resources(ore=10)),
            (model.SolarPowerPlant, 1, model.Resources(ore=15, metal=56)),
            (model.Mine, 10, model.Resources(ore=28, metal=45)),
            (model.SolarPowerPlant, 10, model.Resources(ore=60, metal=110))]
        self.assertEqual([], self.object.get_available_buildings())
        for bld, lvl, resources in expected:
            self.object.resources = resources
            if lvl > 1:
                self.object.buildings[bld] = bld(lvl - 1)
            avail = self.object.get_available_buildings()
            self.assertIn((bld, lvl), avail)

    def test_name_generation(self):
        num = 10
        names = set(self.get_new_instance().name for _ in range(num))
        self.assertEqual(num, len(names))

    def test_sun_distance(self):
        """Sun energy decreases as distance increases"""
        brightness = 500
        tests = [model.Planet(sun_distance=dist,
                              sun_brightness=brightness).sun
                 for dist in range(2, 15)]
        self.assertTrue(all(tests[i] >= tests[i+1]
                            for i in range(len(tests)-1)))

    def test_sun_brightness(self):
        """Sun energy increases as brightness increases"""
        distance = 1
        tests = [model.Planet(sun_distance=distance, sun_brightness=sb).sun
                 for sb in range(100, 1000, 50)]
        self.assertTrue(all(tests[i] <= tests[i+1]
                            for i in range(len(tests)-1)))

    def test_electricity(self):
        num_blds = 10
        elec_per_bld = 10
        for bld_num in range(num_blds):
            bldng = Building()
            bldng._electricity = elec_per_bld
            self.object.buildings[bld_num] = bldng
        self.assertEqual(self.object.electricity, num_blds * elec_per_bld)

    def test_sun_distance_invalid(self):
        self.assertRaises(ModelObjectError,
                          planet.Planet, self.sun_brightness, 0)
