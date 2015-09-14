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
from unittest.mock import Mock, patch, mock_open

from tests.base import SpaceTest

import lib.engine as engine
import lib.model as model


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

    @patch('json.dump')
    def test_save(self, mock_dump):
        self.object.__getstate__ = Mock(return_value=('state',))
        current_obj = (model.Coord(), model.Planet(sun_brightness=1000,
                                                   sun_distance=1))
        with patch('builtins.open', mock_open()):
            self.object.save(current_obj)

        self.assertTrue(self.object.__getstate__.called)
        args, _ = mock_dump.call_args
        self.assertEqual(args[0], (current_obj[1].name, ('state',)))

    def test_system_callback(self):
        self.object.galaxy = Mock()
        system, coord = 'system', 'coord'
        self.object.galaxy.system.return_value = system
        ret_val = self.object._system_callback(coord)
        self.object.galaxy.system.assert_called_with(coord)
        self.assertEqual(ret_val, system)

    def test_new_game(self):
        username = 'name'
        coord = model.Coord()
        orig_galaxy, orig_user = self.object.galaxy, self.object.user
        self.object.new_game(lambda system_cb: (username, coord))
        self.assertNotEqual(orig_galaxy, self.object.galaxy)
        self.assertNotEqual(orig_user, self.object.user)
        self.assertEqual(self.object.user.name, username)
        self.assertEqual(1, len(self.object.user.planets))
        self.assertEqual(coord, self.object.user.planets[0])

        planet = self.object.galaxy.planet(self.object.user.planets[0])
        self.assertEqual(username, planet.emperor)
        self.assertNotEqual(0, planet.resources.trade_value)

    def test_mock_new_game_info_cb(self):
        """The new game info callback defines the new user."""
        test_value = self.object.mock_new_game_info_cb(Mock())
        model.User(*test_value)

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
