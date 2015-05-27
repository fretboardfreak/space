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

from tests.base import SpaceTest

import lib.engine as engine
import lib.model as model


class TestEngine(SpaceTest):

    def setUp(self):
        self.save_file = tempfile.NamedTemporaryFile()
        engine.GameState = model.GameState
        self.engine = engine.SpaceEngine(self.save_file)
        self.engine.state.save_file = self.save_file.name

    def test_load(self):
        orig_state = hash(self.engine.state)
        with open(self.save_file.name, "w") as fout:
            json.dump(self.engine.state.__getstate__(), fout)
        self.save_file.file.seek(0)

        self.engine.load()

        self.assertTrue(orig_state, hash(self.engine.state))

    def test_save(self):
        self.skipTest('NI')

    def test_system_callback(self):
        self.skipTest('NI')

    def test_new_game(self):
        self.skipTest('NI')

    def test_mock_new_game_info_cb(self):
        self.skipTest('NI: check that interface and return values are '
                      'consistent between the original and the mock methods.')
