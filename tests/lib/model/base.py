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

from warnings import warn
from collections import Callable

from tests.base import SpaceTest


class LibModelTest(SpaceTest):

    """Test the contribution of a module to the game model package var __all__.
    """

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.expected_exports = []  # to be set by subclasses

    def test_model(self):
        if self.__class__.__name__ == 'LibModelTest':
            self.skipTest('base class, not a real test')
        import lib.model
        for export in self.expected_exports:
            self.assertIn(export, lib.model.__all__)


class ModelObjectTest(SpaceTest):

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
        if self.__class__.__name__ == 'ModelObjectTest':
            self.skipTest('base class, not a real test')

    def setUp(self):
        self.object = self.get_new_instance()

    def assert_attrs_in_string(self, string):
        lower = string.lower()
        for attr in self.expected_attrs:
            attr = attr.replace('_', ' ')
            patterns = ['{}:{}'.format(attr, sep) for sep in (' ', '\n')]
            self.assertTrue(any(pat in lower for pat in patterns),
                            "Expected Attr {} is missing from model "
                            "{}".format(attr, type(self.object)))

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
        actual = set(attr for attr in dir(self.object)
                     if not attr.startswith('_') and
                     not isinstance(getattr(self.object, attr),
                                    (property, classmethod, Callable,)))
        if self.warnings_to_errors:
            self.assertEqual(set(self.expected_attrs.keys()), actual)
        else:
            unexpected = actual.difference(set(self.expected_attrs.keys()))
            missing = set(self.expected_attrs.keys()).difference(actual)
            if len(unexpected) > 0 or len(missing) > 0:
                msg = ("{}: Missing Attrs: {} Unexpected Attrs: "
                       "{}".format(self.object.__class__.__name__,
                                   missing, unexpected))
                warn(msg)
        for attr in self.expected_attrs:
            self.assertIn(attr, dir(self.object),
                          "Attr {} is missing.".format(attr))
            expected_type = self.expected_attrs[attr]
            self.assertIsInstance(getattr(self.object, attr),
                                  expected_type, "Attr {} is not of type "
                                  "{}".format(attr, expected_type))


class StateMixinTest(object):

    """Test state getting/setting of objects.

    Subclasses using this mixin need to define self.expected_state, and
    implement self.get_tst_state
    """

    def get_tst_state(self):
        """Subclasses should redefine this method."""
        self.skipTest('base class, not a real test')

    def test_getstate(self):
        state = self.object.__getstate__()
        for actual, expected_type in zip(state, self.expected_state):
            self.assertIsInstance(actual, expected_type)

    def test_setstate(self):
        new_state = self.get_tst_state()
        test_bld = self.get_new_instance()
        test_bld.__setstate__(new_state)


class EqualityMixinTest(object):

    def get_equal_tst_values(self):
        """Subclasses should redefine this method if needed."""
        self.object = self.get_new_instance()
        return self.get_new_instance()

    def get_non_equal_tst_values(self):
        """Subclasses should redefine this method if needed.

        Return Value should be greater than that returned by
        self.get_equal_tst_values()
        """
        self.object = self.get_new_instance()
        return self.get_new_instance()

    def get_equality_assert_methods(self):
        if self.__class__.__name__ == 'EqualityMixinTest':
            self.skipTest('base class, not a real test')
        if (hasattr(self, 'negative_equality_logic') and
                getattr(self, 'negative_equality_logic')):
            return self.assertFalse, self.assertTrue
        return self.assertTrue, self.assertFalse

    def test_equal_eq_ne(self):
        test_obj = self.get_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_a(test_obj == self.object)
        assert_b(test_obj != self.object)

    def test_equal_gt(self):
        test_obj = self.get_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_b(test_obj > self.object)
        assert_b(self.object > test_obj)

    def test_equal_lt(self):
        test_obj = self.get_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_b(test_obj < self.object)
        assert_b(self.object < test_obj)

    def test_equal_le(self):
        test_obj = self.get_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_a(test_obj <= self.object)
        assert_a(self.object <= test_obj)

    def test_equal_ge(self):
        test_obj = self.get_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_a(test_obj >= self.object)
        assert_a(self.object >= test_obj)

    def test_not_equal_eq_ne(self):
        test_obj = self.get_non_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_b(test_obj == self.object)
        assert_a(test_obj != self.object)

    def test_not_equal_gt(self):
        test_obj = self.get_non_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_a(test_obj > self.object)
        assert_b(self.object > test_obj)

    def test_not_equal_lt(self):
        test_obj = self.get_non_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_b(test_obj < self.object)
        assert_a(self.object < test_obj)

    def test_not_equal_ge(self):
        test_obj = self.get_non_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_a(test_obj >= self.object)
        assert_b(self.object >= test_obj)

    def test_not_equal_le(self):
        test_obj = self.get_non_equal_tst_values()
        assert_a, assert_b = self.get_equality_assert_methods()
        assert_b(test_obj <= self.object)
        assert_a(self.object <= test_obj)
