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

import lib.cmdline.commands as commands

from .test_base import BaseCommandTest


class CdTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Cd
        self.alias_commands = []

    def set_up_mock_object_id_map(self, object_name):
        target_object = (Mock(), Mock())
        target_object[1].name = object_name
        ret_val = {object_name: target_object}
        self.mock_engine.get_object_id_map = Mock(return_value=ret_val)
        return target_object

    def test_change_focussed(self):
        cd = self.get_instance()
        cd.do_list = Mock()
        object_name = 'some-object'
        target = self.set_up_mock_object_id_map(object_name)
        cd.current_object = None

        cd.do_cd('')
        self.assertTrue(cd.do_list.called)
        self.assertFalse(self.mock_engine.get_object_id_map.called)
        self.assertEqual(cd.current_object, None)
        cd.do_list.reset_mock()

        cd.do_cd(object_name)
        self.assertFalse(cd.do_list.called)
        self.assertTrue(self.mock_engine.get_object_id_map.called)
        self.assertEqual(cd.current_object, target)
