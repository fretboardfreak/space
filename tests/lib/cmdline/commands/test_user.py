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

import lib.cmdline.commands as commands
import lib.model as model

from .test_base import BaseCommandTest


class UserTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.User
        self.alias_commands = []
        self.username = 'username'
        self.mock_engine.user = model.User(self.username, self.mock_coord)

    def get_instance(self):
        self.mock_planet.emperor = self.username
        inst = super().get_instance()
        inst.engine.user_planets = Mock(return_value=[(self.mock_coord,
                                                       self.mock_planet)])
        return inst

    def test_print_stats(self):
        user = self.get_instance()
        user.do_user('')
        self.assertTrue(user.engine.user_planets.called)

    @patch('builtins.input')
    def test_change_name(self, mock_input):
        user_cmd = self.get_instance()
        mock_input.return_value = 'no'

        user_cmd.do_user('--change-name')
        self.assertEqual(self.username, user_cmd.engine.user.name)
        self.assertEqual(self.username, self.mock_planet.emperor)
        self.assertFalse(mock_input.called)
        mock_input.reset_mock()

        user_cmd.do_user('--change-name new-username')
        self.assertEqual(self.username, user_cmd.engine.user.name)
        self.assertEqual(self.username, self.mock_planet.emperor)
        self.assertTrue(mock_input.called)

        mock_input.return_value = 'yes'
        new_name = 'new-username'
        user_cmd.do_user('--change-name {}'.format(new_name))
        self.assertEqual(new_name, user_cmd.engine.user.name)
        self.assertEqual(new_name, self.mock_planet.emperor)
        self.assertTrue(mock_input.called)
