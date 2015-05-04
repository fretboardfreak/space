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

from unittest.mock import patch

from tests.base import SpaceTest

from lib.error import UserInputError
import lib.cmdline.ui as UI


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
