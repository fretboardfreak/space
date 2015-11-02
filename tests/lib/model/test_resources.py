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

import re
from itertools import repeat

from .base import LibModelTest, ModelObjectTest, EqualityMixinTest

from lib.model import resources


class TestLibModelResources(LibModelTest):
    def setUp(self):
        self.expected_exports = [
            resources.ORE, resources.METAL, resources.THORIUM,
            resources.HYDROCARBON, resources.DEUTERIUM, resources.SUN,
            resources.ELECTRICITY, resources.ALL_RESOURCES,
            resources.TRADE_RATIO, resources.Resources]


class TestResources(ModelObjectTest, EqualityMixinTest):
    def get_new_instance(self, *args, **kwargs):
        return resources.Resources(*args, **kwargs)

    def setUp(self):
        self.object = self.get_new_instance()
        self.classname_in_repr = False
        self.expected_attrs = dict(zip(['ore', 'metal', 'thorium',
                                        'hydrocarbon',
                                        'deuterium'], repeat(int)))
        self.expected_attrs['trade_value'] = float

    def test_constructor_invalid_resource(self):
        self.assertRaises(KeyError, self.get_new_instance, flabber=3)

    def test_default_values(self):
        err = "Resource {} was not set to 0 as expected"
        for res in resources.ALL_RESOURCES:
            self.assertTrue(getattr(self.object, res.lower()) == 0,
                            err.format(res))

    def get_equal_tst_values(self):
        for res in resources.ALL_RESOURCES:
            self.object[res] = 1
        test_res = self.get_new_instance()
        for res in resources.TRADE_RATIO:
            test_res.ore += resources.TRADE_RATIO[res]
        return test_res

    def get_non_equal_tst_values(self):
        obj = self.get_equal_tst_values()
        obj.ore += 1
        return obj

    def test_repr(self):
        super().test_repr()
        rep = repr(self.object)
        self.assertEqual(len(resources.ALL_RESOURCES + ['trade value']),
                         len(re.findall("[a-zA-Z ]+:\s+[\d\.]+", rep)))

    def test_str(self):
        super().test_str()
        string = str(self.object)
        self.assertFalse(string.startswith('('))
        self.assertFalse(string.endswith('('))
        self.assertEqual(len(resources.ALL_RESOURCES + ['trade_value']),
                         len(re.findall(':\s*\d+\n?', string, re.MULTILINE)))

    def test_add(self):
        value = self.get_equal_tst_values()
        zero = self.get_new_instance()
        self.assertEqual(self.object, value + zero)
        new_val = value + self.object
        self.assertNotEqual(self.object, new_val)
        self.assertLess(self.object, new_val)
        for res in new_val:
            self.assertEqual(new_val[res], value[res] + self.object[res])

    def test_sub(self):
        zero, one = self.get_new_instance(), self.get_new_instance(ore=1)
        two, neg = self.get_new_instance(ore=2), self.get_new_instance(ore=-1)
        self.assertEqual(one, one - zero)
        self.assertEqual(one, two - one)
        self.assertEqual(neg, one - two)

    def test_trade_value(self):
        # expected value: sum of relative values of resources in order: ore,
        # metal, hydrocarbon, thorium, deuterium
        expected_value = 1 + 2 + 3 + 4 + 5
        self.object = self.get_new_instance(ore=1, metal=1, thorium=1,
                                            hydrocarbon=1, deuterium=1)
        self.assertEqual(self.object.trade_value, expected_value)

    def test_copy(self):
        foo = self.object
        copy = self.object.copy()
        self.object.ore += 10
        self.assertEqual(foo, self.object)
        self.assertNotEqual(copy, self.object)
