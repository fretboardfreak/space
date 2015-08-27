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

import json
import tempfile
from collections import Iterable
from unittest.mock import Mock

from tests.base import SpaceTest

import lib.engine as engine


class TestSpaceEngine(SpaceTest):
    def setUp(self):
        self.save_file = tempfile.NamedTemporaryFile()
        self.object = engine.SpaceEngine(self.save_file)
        self.object.save_file = self.save_file.name

    def test_load(self):
        orig_state = hash(self.object)
        current_obj_name = 'current_obj_name'
        with open(self.save_file.name, "w") as fout:
            json.dump((current_obj_name, self.object.__getstate__()), fout)
        self.save_file.file.seek(0)

        saved_current_obj = self.object.load()
        self.assertTrue(orig_state, hash(self.object))
        self.assertEqual(current_obj_name, saved_current_obj)

    def test_save(self):
        self.skipTest('NI')

    def test_system_callback(self):
        self.skipTest('NI')

    def test_new_game(self):
        self.skipTest('NI')

    def test_mock_new_game_info_cb(self):
        self.skipTest('NI: check that interface and return values are '
                      'consistent between the original and the mock methods.')

    def recurse_objects(self, state, frame):
        """Recursively yield every item in state."""
        print('STARTING FRAME {}'.format(frame))
        frame += 1
        try:
            for obj in state:
                print("obj {} is type {}".format(obj, type(obj)))
                if isinstance(obj, str):  # don't iterate over strings
                    print('  yielding a string')
                    yield obj
                elif isinstance(obj, dict):
                    print('  recursing over dict...')
                    for key, value in obj.items():
                        yield key
                        print('  descending into dict value')
                        for sub_obj in self.recurse_objects(value, frame):
                            yield sub_obj
                elif isinstance(obj, Iterable):
                    print('  recursing...')
                    for sub_obj in self.recurse_objects(obj, frame):
                        yield sub_obj
                else:
                    print('  yielding the obj')
                    yield obj
        except:
            yield state

    def test_state_contents(self):
        """
        Recursively iterate through the state and verify only iterables or
        primitives are used.
        """
        valid_types = (int, float, str, type(None), tuple)
        for obj in self.recurse_objects(self.object.__getstate__(), 0):
            self.assertIsInstance(obj, valid_types)
            if isinstance(obj, tuple):  # dict keys
                for sub_obj in obj:
                    self.assertIsInstance(obj, valid_types)

    def test_focusable_objects(self):
        self.object.user = Mock()
        self.object.user_planets = Mock(return_value=[])
        ret_val = self.object.get_focusable_objects()
        self.assertIsInstance(ret_val, list)
        self.assertTrue(self.object.user_planets.called)

    def test_get_object_id_map(self):
        obj1, obj2 = Mock(), Mock()
        obj1.name, obj2.name = 'obJ1', 'oBj2'
        coord1, coord2 = 'coord1', 'coord2'
        focusable_objs = [(coord1, obj1), (coord2, obj2)]
        self.object.get_focusable_objects = Mock(return_value=focusable_objs)
        id_map = self.object.get_object_id_map()
        id_multiplier = 4  # exact, lowercase, uppercase, index
        self.assertTrue(len(focusable_objs) * id_multiplier,
                        len(id_map.keys()))
        self.assertEqual(set([(coord1, obj1), (coord2, obj2)]),
                         set(id_map.values()))
