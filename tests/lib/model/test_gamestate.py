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

from tempfile import NamedTemporaryFile
from collections import Iterable

from lib import model
from lib.model import gamestate

from .base import LibModelTest, ModelObjectTest, StateMixinTest


class TestLibModelCoord(LibModelTest):
    def setUp(self):
        self.expected_exports = [gamestate.GameState]


class TestGameState(ModelObjectTest, StateMixinTest):
    def setUp(self):
        self.user = model.User('nim', model.Coord())
        self.galaxy = model.Galaxy()
        system = self.galaxy.system(self.user.planets[0])
        planet = system.planets[int(self.user.planets[0].planet)]
        planet.emperor = self.user.name
        super().setUp()
        self.expected_state = (str, (tuple, type(None)), (tuple, type(None)))
        self.classname_in_repr = True
        self.expected_attrs = {'save_file': str, 'user': (model.User,
                                                          type(None)),
                               'galaxy': (model.Galaxy, type(None))}

    def get_new_instance(self):
        self.tmp_file = NamedTemporaryFile()
        state = gamestate.GameState(save_file=self.tmp_file.name)
        state.user = self.user
        state.galaxy = self.galaxy
        return state

    def get_tst_state(self):
        return ('save_file', self.user.__getstate__(),
                self.galaxy.__getstate__())

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
