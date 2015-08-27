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

import collections
from unittest.mock import Mock, patch
from cmd import Cmd

from tests.base import SpaceTest

import lib.cmdline.interpreter as interpreter
from lib.engine import SpaceEngine


class TestInterpreterModule(SpaceTest):
    def setUp(self):
        self.mock_engine = Mock(spec=SpaceEngine)

    @patch('sys.exit', autospec=True)
    @patch('lib.cmdline.ui.input_bool', autospec=True)
    def test_start_new_game(self, mock_input_bool, mock_exit):
        mock_input_bool.return_value = False
        sci = interpreter.SpaceCmdInterpreter(self.mock_engine)
        sci.start_new_game()
        self.assertTrue(mock_input_bool.called)
        self.assertTrue(mock_exit.called)

        mock_input_bool.return_value = True
        sci.start_new_game()
        self.assertTrue(self.mock_engine.new_game.called)
        self.assertIsInstance(self.mock_engine.new_game.call_args[0][0],
                              collections.Callable)

    def get_interpreter_instance(self):
        sci = interpreter.SpaceCmdInterpreter(self.mock_engine)
        sci.cmdloop = Mock(spec=Cmd.cmdloop)
        sci.start_new_game = Mock(spec=sci.start_new_game)
        return sci

    def test_start_save_file_loads(self):
        sci = self.get_interpreter_instance()
        sci.onecmd = Mock()
        sci.start()
        self.assertTrue(self.mock_engine.load.called)
        self.assertTrue(sci.cmdloop.called)
        self.assertTrue(self.mock_engine.save.called)
        self.assertFalse(sci.start_new_game.called)
        self.assertTrue(sci.onecmd.called)  # current_object restored

    def test_start_no_save_file(self):
        self.mock_engine.load.side_effect = FileNotFoundError('foobar')
        sci = self.get_interpreter_instance()
        sci.start()
        self.assertTrue(self.mock_engine.load.called)
        self.assertTrue(sci.cmdloop.called)
        self.assertTrue(self.mock_engine.save.called)
        self.assertTrue(sci.start_new_game.called)

    def test_start_cmdloop_error(self):
        sci = self.get_interpreter_instance()
        sci.start()
        sci.cmdloop.side_effect = Exception('foobar')
        self.assertTrue(self.mock_engine.save.called)
