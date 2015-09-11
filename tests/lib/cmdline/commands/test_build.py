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

import lib.model as model
import lib.cmdline.commands as commands

from .test_base import BaseCommandTest


class BuildTest(BaseCommandTest):
    def setUp(self):
        super().setUp()
        self.command_class = commands.Build
        self.alias_commands = []
        self.mock_planet = Mock()
        mock_building = Mock()
        mock_building.name = 'Mine'
        self.mock_planet.get_available_buildings.return_value = [
            (mock_building, 1)]
        self.mock_planet.build.return_value = True

    def test_build_no_current_planet(self):
        build = self.get_instance()
        build.current_object = None
        build.do_build('')
        self.assertEqual(build.current_object, None)

    def get_instance_with_current_object(self):
        build = self.get_instance()
        build.current_object = (model.Coord(), self.mock_planet)
        return build

    def test_build_no_specified_type(self):
        build = self.get_instance_with_current_object()
        build.do_build('')
        self.assertTrue(self.mock_planet.get_available_buildings.called)
        self.assertFalse(self.mock_planet.build.called)

    def test_build(self):
        build = self.get_instance_with_current_object()
        build.do_build('Mine')
        self.assertFalse(self.mock_planet.get_available_buildings.called)
        self.assertTrue(self.mock_planet.build.called)
