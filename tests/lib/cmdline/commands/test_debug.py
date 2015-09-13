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

import lib.cmdline.commands as commands

from .test_base import BaseCommandTest


class DebugTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Debug
        self.alias_commands = ['do_dbg']

    # note: need patch the default action using the mangled named
    @patch('lib.cmdline.commands.Debug._Debug__print_state')
    def test_default_command_action(self, mock_print_state):
        debug_cmd = self.get_instance()
        debug_cmd.do_debug('')
        self.assertTrue(mock_print_state.called)

    @patch('builtins.print')
    def test_print_state(self, mock_print):
        debug_cmd = self.get_instance()
        debug_cmd.do_debug('--print-state')
        self.assertTrue(mock_print.called)
        mock_print.assert_called_with(debug_cmd.engine)

    @patch('code.interact')
    def test_interactive(self, mock_interact):
        debug_cmd = self.get_instance()
        debug_cmd.do_debug('--interact')
        self.assertTrue(mock_interact.called)

    def test_new_state(self):
        debug_cmd = self.get_instance()
        debug_cmd.do_debug('--new-state')
        self.assertTrue(self.mock_engine.new_game.called)
