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
from itertools import chain
from cmd import Cmd

from tests.base import SpaceTest

import lib.cmdline.commands as commands
from lib.cmdline.commands.base import CommandMixin
import lib.cmdline.interpreter as interpreter
from lib.engine import SpaceEngine


class TestInterpreterModule(SpaceTest):
    def setUp(self):
        self.mock_engine = Mock(spec=SpaceEngine)

    def test_command_mixin(self):
        cm = CommandMixin(self.mock_engine)
        self.assertTrue(hasattr(cm, 'engine'))
        self.assertEqual(cm.engine, self.mock_engine)

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
        sci.start()
        self.assertTrue(self.mock_engine.load.called)
        self.assertTrue(sci.cmdloop.called)
        self.assertTrue(self.mock_engine.save.called)
        self.assertFalse(sci.start_new_game.called)

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


class BaseCommandTest(SpaceTest):
    def setUp(self):
        self.command_class = CommandMixin
        self.alias_commands = []
        self.mock_engine = Mock(spec=SpaceEngine)

    def skip_base_class(self):
        if self.__class__.__name__ == 'BaseCommandTest':
            self.skipTest('base class, not valid test')

    def get_instance(self):
        return self.command_class(self.mock_engine)

    def test_required_methods(self):
        self.skip_base_class()
        required_methods = [meth.format(self.command_class.__name__.lower())
                            for meth in ['do_{}', 'help_{}']]
        inst = self.get_instance()
        for method in chain(required_methods, self.alias_commands):
            self.assertTrue(hasattr(inst, method), 'Class {} is missing '
                            'method {}'.format(self.command_class.__name__,
                                               method))


class QuitTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Quit
        self.alias_commands = ['do_q', 'do_EOF']


class ShowTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Show
        self.alias_commands = ['do_sh', 'do_s']


class DebugTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Debug
        self.alias_commands = []


class PlanetTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Planet
        self.alias_commands = ['do_p', 'do_pl']


class UserTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.User
        self.alias_commands = ['do_u']
