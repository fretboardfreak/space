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
from itertools import repeat

from .base import LibModelTest, ModelObjectTest, ModelObjectEqualityMixin

from lib.model import resources


class TestLibModelResources(LibModelTest):
    def setUp(self):
        self.expected_exports = ['ORE', 'METAL', 'THORIUM', 'HYDROCARBON',
                                 'DEUTERIUM', 'SUN', 'ELECTRICITY',
                                 'ALL_RESOURCES', 'TRADE_RATIO', 'Resources']


class TestResources(ModelObjectTest, ModelObjectEqualityMixin):
    def get_new_instance(self, *args, **kwargs):
        return resources.Resources(*args, **kwargs)

    def setUp(self):
        self.object = self.get_new_instance()
        self.classname_in_repr = False
        self.expected_attrs = dict(zip(['ore', 'metal', 'thorium',
                                        'hydrocarbon',
                                        'deuterium'], repeat(int)))

    def test_constructor_invalid_resource(self):
        self.assertRaises(KeyError, self.get_new_instance, flabber=3)

    def test_default_values(self):
        err = "Resource {} was not set to 0 as expected"
        for res in resources.ALL_RESOURCES:
            self.assertTrue(getattr(self.object, res.lower()) == 0,
                            err.format(res))

    def test_negative_values(self):
        self.object.ore = 3
        self.assertEqual(self.object.ore, 3)
        self.object['thorium'] = -3
        self.assertEqual(self.object.thorium, 3)
        self.object.metal = -3
        self.assertEqual(self.object.metal, 3)
        self.object.deuterium = -3
        self.assertEqual(self.object['deuterium'], 3)

    def get_test_values(self):
        for res in resources.ALL_RESOURCES:
            self.object[res] = 1
        test_res = self.get_new_instance()
        for res in resources.TRADE_RATIO:
            test_res.ore += resources.TRADE_RATIO[res]
        return test_res

    def test_tally_value_difference(self):
        test_res = self.get_test_values()
        self.assertEqual(
                0, self.object._tally_value_difference(self.object))
        self.assertEqual(0, test_res._tally_value_difference(self.object))

    def test_repr(self):
        super().test_repr()
        rep = repr(self.object)
        self.assertEqual(len(resources.ALL_RESOURCES),
                         len(re.findall(': \d+[,\)]', rep)))

    def test_str(self):
        super().test_str()
        string = str(self.object)
        self.assertFalse(string.startswith('('))
        self.assertFalse(string.endswith('('))
        self.assertEqual(len(resources.ALL_RESOURCES),
                         len(re.findall(': \d+\n?', string, re.MULTILINE)))

    def test_add(self):
        value = self.get_test_values()
        zero = self.get_new_instance()
        self.assertEqual(self.object, value + zero)
        non_zero = self.get_new_instance(ore=1)
        new_val = value + non_zero
        self.assertNotEqual(self.object, new_val)
        self.assertTrue(self.object < new_val)

    def test_sub(self):
        value = self.get_test_values()
        zero = self.get_new_instance()
        self.assertEqual(self.object, value + zero)
        non_zero = self.get_new_instance(ore=1)
        new_val = value - non_zero
        self.assertNotEqual(self.object, new_val)
        self.assertTrue(self.object > new_val)