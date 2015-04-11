#!/usr/bin/env python

import unittest
import re

from lib.model import resources


class TestModule(unittest.TestCase):
    def test_model_all_resources_exported(self):
        err = 'Resource {} is missing from __all__'
        import lib.model
        for res in resources.ALL_RESOURCES:
            self.assertTrue(hasattr(lib.model, res.upper()), err.format(res))


class TestResources(unittest.TestCase):
    def setUp(self):
        self.resources = resources.Resources()

    def test_all_resources_attrs(self):
        err = "Resource {} is missing from class Resources attribute list"
        for res in resources.ALL_RESOURCES:
            self.assertTrue(hasattr(self.resources, res.lower()),
                            err.format(res))

    def test_constructor_invalid_resource(self):
        self.assertRaises(KeyError, resources.Resources, flabber=3)

    def test_default_values(self):
        err = "Resource {} was not set to 0 as expected"
        for res in resources.ALL_RESOURCES:
            self.assertTrue(getattr(self.resources, res.lower()) == 0,
                            err.format(res))

    def test_negative_values(self):
        self.resources.ore = 3
        self.assertEqual(self.resources.ore, 3)
        self.resources['thorium'] = -3
        self.assertEqual(self.resources.thorium, 3)
        self.resources.metal = -3
        self.assertEqual(self.resources.metal, 3)
        self.resources.deuterium = -3
        self.assertEqual(self.resources['deuterium'], 3)

    def _get_test_values(self):
        for res in resources.ALL_RESOURCES:
            self.resources[res] = 1
        test_res = resources.Resources()
        for res in resources.TRADE_RATIO:
            test_res.ore += resources.TRADE_RATIO[res]
        return test_res

    def test_tally_value_difference(self):
        test_res = self._get_test_values()
        self.assertEqual(
                0, self.resources._tally_value_difference(self.resources))
        self.assertEqual(0, test_res._tally_value_difference(self.resources))

    def test_equal(self):
        test_res = self._get_test_values()
        self.assertTrue(test_res == self.resources)
        self.assertFalse(test_res != self.resources)
        self.assertTrue(test_res <= self.resources)
        self.assertTrue(test_res >= self.resources)
        self.assertFalse(test_res > self.resources)
        self.assertFalse(test_res < self.resources)
        self.assertTrue(self.resources <= test_res)
        self.assertTrue(self.resources >= test_res)
        self.assertFalse(self.resources > test_res)
        self.assertFalse(self.resources < test_res)

    def test_not_equal(self):
        test_res = self._get_test_values()
        test_res.ore += 1
        self.assertFalse(test_res == self.resources)
        self.assertTrue(test_res != self.resources)
        self.assertFalse(test_res <= self.resources)
        self.assertTrue(test_res >= self.resources)
        self.assertTrue(test_res > self.resources)
        self.assertFalse(test_res < self.resources)
        self.assertTrue(self.resources <= test_res)
        self.assertFalse(self.resources >= test_res)
        self.assertFalse(self.resources > test_res)
        self.assertTrue(self.resources < test_res)

    def test_repr(self):
        rep = repr(self.resources)
        self.assertTrue(rep.startswith('('))
        self.assertTrue(rep.endswith(')'))
        for resource in resources.ALL_RESOURCES:
            self.assertIn(resource, rep)
        self.assertEqual(len(resources.ALL_RESOURCES),
                         len(re.findall(': \d+[,\)]', rep)))

    def test_str(self):
        string = str(self.resources)
        self.assertFalse(string.startswith('('))
        self.assertFalse(string.endswith('('))
        for resource in resources.ALL_RESOURCES:
            self.assertIn(resource, string)
        self.assertEqual(len(resources.ALL_RESOURCES),
                         len(re.findall(': \d+\n?', string, re.MULTILINE)))

    def test_add(self):
        value = self._get_test_values()
        zero = resources.Resources()
        self.assertEqual(self.resources, value + zero)
        non_zero = resources.Resources(ore=1)
        new_val = value + non_zero
        self.assertNotEqual(self.resources, new_val)
        self.assertTrue(self.resources < new_val)

    def test_sub(self):
        value = self._get_test_values()
        zero = resources.Resources()
        self.assertEqual(self.resources, value + zero)
        non_zero = resources.Resources(ore=1)
        new_val = value - non_zero
        self.assertNotEqual(self.resources, new_val)
        self.assertTrue(self.resources > new_val)


if __name__ == "__main__":
    unittest.main()
