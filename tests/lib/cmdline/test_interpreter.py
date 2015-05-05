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

from unittest.mock import Mock
from itertools import chain

from tests.base import SpaceTest

import lib.cmdline.interpreter as interpreter
from lib.engine import SpaceEngine


class TestInterpreterModule(SpaceTest):
    def test_command_mixin(self):
        mock_engine = Mock(spec=SpaceEngine)
        cm = interpreter.CommandMixin(mock_engine)
        self.assertTrue(hasattr(cm, 'engine'))
        self.assertEqual(cm.engine, mock_engine)


class BaseCommandTest(SpaceTest):
    def setUp(self):
        self.command_class = interpreter.CommandMixin
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
        self.command_class = interpreter.Quit
        self.alias_commands = ['do_q', 'do_EOF']


class ShowTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = interpreter.Show
        self.alias_commands = ['do_sh', 'do_s']


class DebugTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = interpreter.Debug
        self.alias_commands = []


class PlanetTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = interpreter.Planet
        self.alias_commands = ['do_p', 'do_pl']


class UserTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = interpreter.User
        self.alias_commands = ['do_u']
