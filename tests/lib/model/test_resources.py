#!/usr/bin/env python

import unittest
import random
import re

from lib.model import resources


class TestResources(unittest.TestCase):
    def setUp(self):
        self.resources = resources.Resources()

    def test_model_all_resources_exported(self):
        err = 'Resource {} is missing from __all__'
        import lib.model
        for res in resources.ALL_RESOURCES:
            self.assertTrue(hasattr(lib.model, res.upper()), err.format(res))

    def test_all_resources_attrs(self):
        err = "Resource {} is missing from class Resources"
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


if __name__ == "__main__":
    unittest.main()
