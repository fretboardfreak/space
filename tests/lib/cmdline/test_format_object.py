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

from unittest.mock import Mock, patch

from tests.base import SpaceTest

from lib.cmdline import format_object
from lib import model

# TODO: add test for format_object.planet_available_buildings


class TestPrinObject(SpaceTest):
    @patch('builtins.print', autospec=True)
    def test_print_object(self, mock_print):
        mock_func = Mock()
        format_object.print_object(mock_func, 3, test='foo')
        self.assertTrue(mock_func.called)
        args, kwargs = mock_func.call_args
        self.assertEqual(args, (3,))
        self.assertEqual(kwargs, {'test': 'foo'})
        self.assertTrue(mock_print.called)


class BaseFormatMethodTest(SpaceTest):
    def setUp(self):
        # these variables must be set by subclasses
        self.func = None
        self.test_obj = None
        self.has_verbose_opt = True

    def skip_base_class(self):
        if self.__class__.__name__ == 'BaseFormatMethodTest':
            self.skipTest('base class, not valid test')

    def test_format_method(self):
        self.skip_base_class()
        result = self.func(self.test_obj)
        self.assertIsInstance(result, str)
        if self.has_verbose_opt:
            result = self.func(self.test_obj, verbose=True)
            self.assertIsInstance(result, str)


class TestFormatGalaxy(BaseFormatMethodTest):
    def setUp(self):
        self.func = format_object.galaxy
        self.test_obj = model.Galaxy()
        self.has_verbose_opt = False


class TestFormatUser(BaseFormatMethodTest):
    def setUp(self):
        self.func = format_object.user
        self.test_obj = model.User('username', model.Coord(0, 0, 0))
        self.has_verbose_opt = True


class TestFormatUserPlanets(TestFormatUser):
    def setUp(self):
        super().setUp()
        self.func = format_object.user_planets


class TestFormatSystem(BaseFormatMethodTest):
    # TODO: add tests for the "_coord" flag, or refactor it away
    def setUp(self):
        self.func = format_object.system
        self.test_obj = model.System()
        self.has_verbose_opt = False
