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

from random import randint
from unittest.mock import Mock, patch

from tests.base import SpaceTest

from lib.error import UserInputError
import lib.cmdline.ui as UI
from lib import model


VALID_BOOL_INPUT = ['y', 'n', 'Y', 'N', 'yes', 'no', 'YES', 'NO']
INVALID_BOOL_INPUT = ['aoeu', '0', 'ay', 'bn']

VALID_INT_INPUT = ['0', '9  ', '   3  ']
INVALID_INT_INPUT = ['0two', '0x33', '987.234']

INVALID_TEXT_INPUT = [1, 3.9, '\n', '\t']


class BaseInputMethodTest(SpaceTest):
    def setUp(self):
        self.test_func = UI.input_bool
        self.message = 'gimme some test input: '
        self.valid_input = []
        self.invalid_input = []

    def skip_base_test(self):
        if self.__class__.__name__ == 'BaseInputMethodTest':
            self.skipTest('base class, not valid test')

    @patch('builtins.input')
    def test_valid_input(self, mock_input):
        self.skip_base_test()
        mock_input.side_effect = self.valid_input
        for _ in self.valid_input:
            self.test_func(self.message)

    @patch('builtins.input')
    def test_invalid_input(self, mock_input):
        self.skip_base_test()
        for invalid in self.invalid_input:
            mock_input.return_value = invalid
            self.assertRaises(UserInputError, self.test_func, self.message)
            self.assertEqual(UI.RETRY_ATTEMPTS, mock_input.call_count)
            mock_input.reset_mock()


class TestInputBool(BaseInputMethodTest):
    def setUp(self):
        super().setUp()
        self.test_func = UI.input_bool
        self.valid_input = VALID_BOOL_INPUT
        self.invalid_input = INVALID_BOOL_INPUT


class TestInputInt(BaseInputMethodTest):
    def setUp(self):
        super().setUp()
        self.test_func = UI.input_int
        self.valid_input = VALID_INT_INPUT
        self.invalid_input = INVALID_INT_INPUT


class TestInputText(BaseInputMethodTest):
    def setUp(self):
        super().setUp()
        self.test_func = UI.input_text
        self.valid_input = (VALID_BOOL_INPUT + VALID_INT_INPUT +
                            INVALID_BOOL_INPUT + INVALID_INT_INPUT)
        self.invalid_input = INVALID_TEXT_INPUT


class TestNewGame(SpaceTest):
    def setUp(self):
        self.input_integer = [randint(0, 100) for _ in range(4)]
        self.chosen_planet_index = 0
        self.input_integer.append(self.chosen_planet_index)
        self.input_text = 'Emperor Name'
        self.system = model.System()

    @patch('lib.cmdline.ui.input_text')
    @patch('lib.cmdline.ui.input_int')
    def test_get_new_game_info(self, mock_input_int, mock_input_text):
        mock_input_int.side_effect = self.input_integer
        mock_input_text.return_value = self.input_text
        system_callback = Mock(return_value=self.system)
        result = UI.get_new_game_info(system_callback)
        self.assertEqual(result[0], self.input_text)
        self.assertIsInstance(result[1], model.Coord)
        self.assertIsInstance(result[2], model.Planet)
        self.assertEqual(result[2],
                         self.system.planets[self.chosen_planet_index])
