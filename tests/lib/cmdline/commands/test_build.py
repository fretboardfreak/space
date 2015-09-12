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


class BuildTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Build
        self.mock_planet.get_available_buildings = Mock(return_value=[])

    def test_build_no_current_planet(self):
        build = self.get_instance()
        build.current_object = None
        build.do_build('')
        self.assertEqual(build.current_object, None)

    def test_build_no_specified_type(self):
        self.mock_planet.build = Mock()
        build = self.get_instance()
        build.do_build('')
        self.assertTrue(self.mock_planet.get_available_buildings.called)
        self.assertFalse(self.mock_planet.build.called)

    def test_build(self):
        self.mock_planet.build = Mock()
        build = self.get_instance()
        build.do_build('Mine')
        self.assertFalse(self.mock_planet.get_available_buildings.called)
        self.assertTrue(self.mock_planet.build.called)
