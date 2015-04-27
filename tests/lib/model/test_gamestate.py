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
from .base import LibModelTest, ModelObjectTest, StateMixinTest

from lib import model
from lib.model import gamestate


class TestLibModelCoord(LibModelTest):
    def setUp(self):
        self.expected_exports = [gamestate.GameState]


class TestGameState(ModelObjectTest, StateMixinTest):
    def setUp(self):
        super().setUp()
        self.expected_state = (str, (tuple, type(None)), (tuple, type(None)))
        self.classname_in_repr = True
        self.expected_attrs = {'save_file': str, 'user': (model.User,
                                                          type(None)),
                               'galaxy': (model.Galaxy, type(None))}

    def get_new_instance(self):
        self.tmp_file = NamedTemporaryFile()
        return gamestate.GameState(save_file=self.tmp_file.name)

    def get_tst_state(self):
        return ('save_file', None, None)
