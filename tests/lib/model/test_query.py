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

import tempfile
from unittest.mock import Mock
from tests.base import SpaceTest
from .base import LibModelTest

from lib.model import query
import lib.model as model
from lib.engine import SpaceEngine


class TestLibModelQuery(LibModelTest):
    def setUp(self):
        self.expected_exports = [query.ModelQueryMixin]
        super().setUp()


class TestModelQuery(SpaceTest):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile()
        self.mq = query.ModelQueryMixin()
        engine = SpaceEngine(save_file=self.tempfile.name,
                             opts=Mock())
        engine.new_game(engine.mock_new_game_info_cb)
        self.mq.galaxy = engine.galaxy
        self.mq.user = engine.user

    def test_user_planets(self):
        result = self.mq.user_planets(self.mq.user)
        # ensure result is a map of some sort, i.e. list of tuples, vs. dict
        list(result)
        dict(result)
        for coord, planet in result:
            self.assertIsInstance(coord, model.Coord)
            self.assertIsInstance(planet, model.Planet)
