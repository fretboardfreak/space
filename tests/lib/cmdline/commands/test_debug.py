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

from unittest import skip

import lib.cmdline.commands as commands

from .test_base import BaseCommandTest


class DebugTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Debug
        self.alias_commands = ['do_dbg']

    @skip('NI')
    def test_print_state(self):
        pass

    @skip('NI')
    def test_interactive(self):
        pass

    @skip('NI')
    def test_new_state(self):
        pass
