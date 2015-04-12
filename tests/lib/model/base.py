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
from mock import Mock


class LibModelTest(unittest.TestCase):

    """Test the contribution of a module to the game model package var __all__.
    """

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.expected_exports = []  # to be set by subclasses

    def test_model(self):
        import lib.model
        for export in self.expected_exports:
            self.assertIn(export, lib.model.__all__)


class ModelObjectStateMixin(object):

    """Test state getting/setting of objects.

    Subclasses using this mixin need to define self.expected_state
    """

    def get_test_state(self):
        return tuple()

    def test_getstate(self):
        state = self.object.__getstate__()
        for actual, expected_type in zip(state, self.expected_state):
            self.assertIsInstance(actual, expected_type)

    def test_setstate(self):
        new_state = self.get_test_state()
        test_bld = self.get_new_instance()
        test_bld.__setstate__(new_state)


class ModelObjectEqualityMixin(object):

    def test_equal(self):
        test_obj = self.get_test_values()
        self.assertTrue(test_obj == self.object)
        self.assertFalse(test_obj != self.object)

    def test_equal_comparison(self):
        test_obj = self.get_test_values()
        self.assertTrue(test_obj <= self.object)
        self.assertTrue(test_obj >= self.object)
        self.assertFalse(test_obj > self.object)
        self.assertFalse(test_obj < self.object)
        self.assertTrue(self.object <= test_obj)
        self.assertTrue(self.object >= test_obj)
        self.assertFalse(self.object > test_obj)
        self.assertFalse(self.object < test_obj)

    def test_not_equal(self):
        test_obj = self.get_test_values()
        test_obj.ore += 1
        self.assertFalse(test_obj == self.object)
        self.assertTrue(test_obj != self.object)

    def test_not_equal_comparison(self):
        test_obj = self.get_test_values()
        test_obj.ore += 1
        self.assertFalse(test_obj <= self.object)
        self.assertTrue(test_obj >= self.object)
        self.assertTrue(test_obj > self.object)
        self.assertFalse(test_obj < self.object)
        self.assertTrue(self.object <= test_obj)
        self.assertFalse(self.object >= test_obj)
        self.assertFalse(self.object > test_obj)
        self.assertTrue(self.object < test_obj)


class ModelObjectTest(unittest.TestCase):

    """A minimal set of tests for the game model objects.

    All game model objects should pass this set of tests.

    Mixin base classes can provide additional tests for greater flexibility.
    """

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

        # These attributes need to be set by the subclass in setUp
        self.object = None
        self.classname_in_repr = False
        self.expected_attrs = dict()  # Key: str, attr name, Value: type

    def get_new_instance(self):
        """Subclasses should redefine this initialization code."""
        inst = Mock()

        def _repr(self):
            return '{}()'.format(self.object.__class__.__name__)

        def _str(self):
            return ''

        inst.__str__ = _str
        inst.__repr__ = _repr
        inst.__getstate__ = lambda self: tuple()
        inst.__setstate__ = lambda self, state: None
        return inst

    def get_test_values(self):
        return self.get_new_instance()

    def setUp(self):
        self.object = self.get_new_instance()

    def assert_attrs_in_string(self, string):
        lower = string.lower()
        for attr in self.expected_attrs:
            pattern = '{}: '.format(attr)
            self.assertIn(pattern, lower)

    def test_repr(self):
        rep = repr(self.object)
        if self.classname_in_repr:
            self.assertTrue(
                rep.startswith('{}('.format(self.object.__class__.__name__)))
        self.assertTrue(rep.endswith(')'))
        self.assert_attrs_in_string(rep)

    def test_str(self):
        string = str(self.object)
        self.assert_attrs_in_string(string)

    def test_attrs(self):
        for attr in self.expected_attrs:
            self.assertIn(attr, dir(self.object))
            self.assertIsInstance(getattr(self.object, attr),
                                  self.expected_attrs[attr])
