import unittest
import random
import re

from lib.model import coord


class BaseCoordTest(unittest.TestCase):
    def setUp(self):
        self.coord = coord.Coord(0, 0, 0)

    def test_sector(self):
        self._property_test('sector')

    def test_system(self):
        self._property_test('system')

    def _property_test(self, name):
        if name == 'planet':
            test_value = self.get_test_values(planet=True)
        else:
            test_value = self.get_test_values(planet=False)
        setattr(self.coord, name, test_value)
        self.assertEqual(getattr(self.coord, name), test_value)

    def get_test_values(self, planet=False):
        count = 2
        if planet:
            count = 1
        return tuple([random.randint(0, 1000) for _ in range(count)])


class TestCoord(BaseCoordTest):
    def test_planet(self):
        self._property_test('planet')

    def test_hash(self):
        start_hash = hash(self.coord)
        test_sector = self.get_test_values()
        test_system = self.get_test_values()
        test_planet = self.get_test_values(planet=True)
        example_coord = coord.Coord()
        self.assertEqual(hash(example_coord), start_hash)
        example_coord.sector = test_sector
        example_coord.system = test_system
        example_coord.planet = test_planet
        self.coord.sector = test_sector
        self.coord.system = test_system
        self.coord.planet = test_planet
        self.assertEqual(hash(self.coord), hash(example_coord))

    def test_repr(self):
        expected = 'Coord\(\d\.\d, \d\.\d, \d\)'
        self.assertTrue(re.search(expected, repr(self.coord)))

    def test_str(self):
        expected = '\(\'\d\.\d\', \'\d\.\d\', \'\d\'\)'
        self.assertTrue(re.search(expected, str(self.coord)))

    def test_getstate(self):
        expected = ('0.0', '0.0', '0')
        self.assertEqual(expected, self.coord.__getstate__())

    def test_setstate(self):
        self.coord.sector = self.get_test_values()
        self.coord.system = self.get_test_values()
        self.coord.planet = self.get_test_values(planet=True)
        test_obj = coord.Coord()
        test_obj.__setstate__((self.coord.x, self.coord.y, self.coord.planet))
        self.assertEqual((self.coord.x, self.coord.y, self.coord.planet),
                         (test_obj.x, test_obj.y, test_obj.planet))


class TestSystemCoord(BaseCoordTest):
    def setUp(self):
        self.coord = coord.SystemCoord(0, 0)

    def test_no_planet(self):
        self.assertFalse(hasattr(self.coord, 'planet'))

    def test_hash(self):
        start_hash = hash(self.coord)
        test_sector = self.get_test_values()
        test_system = self.get_test_values()
        example_coord = coord.SystemCoord()
        self.assertEqual(hash(example_coord), start_hash)
        example_coord.sector = test_sector
        example_coord.system = test_system
        self.coord.sector = test_sector
        self.coord.system = test_system
        self.assertEqual(hash(self.coord), hash(example_coord))

    def test_getstate(self):
        expected = ('0.0', '0.0')
        self.assertEqual(expected, self.coord.__getstate__())

    def test_repr(self):
        expected = 'SystemCoord\(\d\.\d, \d\.\d\)'
        self.assertTrue(re.search(expected, repr(self.coord)))

    def test_str(self):
        expected = '\(\'\d\.\d\', \'\d\.\d\'\)'
        self.assertTrue(re.search(expected, str(self.coord)))

    def test_setstate(self):
        self.coord.sector = self.get_test_values()
        self.coord.system = self.get_test_values()
        test_obj = coord.SystemCoord()
        test_obj.__setstate__((self.coord.x, self.coord.y))
        self.assertEqual((self.coord.x, self.coord.y),
                         (test_obj.x, test_obj.y))
