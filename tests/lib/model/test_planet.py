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

import unittest

from .base import LibModelTest, ModelObjectTest, ModelObjectStateMixin

from lib import model
from lib.model import planet


class TestLibModelCoord(LibModelTest):
    def setUp(self):
        self.expected_exports = ['Planet']


class TestPlanet(ModelObjectTest, ModelObjectStateMixin):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.sun_brightness = 5555
        self.sun_distance = 3
        self.expected_state = (str, (str, type(None)), model.Resources,
                               (int, float), dict, int, int)
        self.classname_in_repr = True
        self.expected_attrs = {
            'max_resources': model.Resources, 'name': str,
            'emperor': (type(None), str), 'resources': model.Resources,
            'last_update': float, 'sun_brightness': int,
            'sun_distance': int, 'rates': model.Resources,
            'ore': int, 'thorium': int, 'metal': int, 'hydrocarbon': int,
            'deuterium': int, 'sun': float, 'electricity': int,
            'research': dict}

    def get_new_instance(self):
        return planet.Planet(self.sun_brightness, self.sun_distance)

    def get_test_state(self):
        return ('name', 'emperor', model.Resources(), 123456, {}, 555, 3)

    @unittest.skip('Planet.__repr__ needs refactoring')
    def test_repr(self):
        pass

    @unittest.skip('Planet.__str__ needs refactoring/implementing')
    def test_str(self):
        pass
