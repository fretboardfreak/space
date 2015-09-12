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
from unittest.mock import patch

import lib.cmdline.commands as commands

from .test_base import BaseCommandTest


class ListTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.List
        self.alias_commands = ['do_ls']

    @patch('lib.cmdline.format_object.print_object')
    def test_list_planets(self, print_object):
        ls = self.get_instance()
        ls.do_ls('-a')
        self.assertTrue(print_object.called)
        self.assertTrue(self.mock_engine.get_focusable_objects.called)

    @skip('NI')
    def test_show_focussed_no_current_object(self):
        ls = self.get_instance()
        ls.do_ls('-a')


    @skip('NI')
    def test_show_focussed(self):
        pass
