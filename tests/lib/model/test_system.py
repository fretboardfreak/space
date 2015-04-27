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

from .base import LibModelTest, ModelObjectTest, StateMixinTest

from lib import model
from lib.model import system


class TestLibModelSystem(LibModelTest):
    def setUp(self):
        self.expected_exports = [system.System]


class TestSystem(ModelObjectTest, StateMixinTest):
    def setUp(self):
        super().setUp()
        self.expected_state = (int, int, list)
        self.classname_in_repr = True
        self.expected_attrs = {'size': int, 'sun_brightness': int,
                               'planets': list}

    def get_new_instance(self):
        return system.System()

    def get_tst_state(self):
        return (10, 500, [model.Planet(sun_brightness=500, sun_distance=dist)
                          for dist in range(1, 11)])

    def test_size_in_valid_range(self):
        self.assertGreaterEqual(self.object.size, system.System.size_range[0])
        self.assertLessEqual(self.object.size, system.System.size_range[1])

    def test_brightness_within_bounds(self):
        test_bounds = system.System.get_brightness_bounds(self.object.size)
        self.assertGreaterEqual(self.object.sun_brightness, test_bounds[0])
        self.assertLessEqual(self.object.sun_brightness, test_bounds[1])

    def test_get_brightness_bounds(self):
        min_brightness = 10
        max_brightness = 1000
        for size in range(*system.System.size_range):
            bounds = system.System.get_brightness_bounds(size)
            self.assertGreaterEqual(bounds[0], min_brightness)
            self.assertLessEqual(bounds[1], max_brightness)

    def test_planet_count(self):
        self.assertEqual(len(self.object.planets), self.object.size)
