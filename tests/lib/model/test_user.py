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

from random import randint
from .base import LibModelTest, ModelObjectTest, StateMixinTest

from lib import model
from lib.model import user


class TestLibModelCoord(LibModelTest):
    def setUp(self):
        self.expected_exports = [user.User]


class TestUser(ModelObjectTest, StateMixinTest):
    def setUp(self):
        super().setUp()
        self.expected_state = (str, list)
        self.classname_in_repr = True
        self.expected_attrs = {'name': str, 'planets': list}

    def get_new_instance(self):
        self.home_coord = model.Coord(*[randint(0, 10) for _ in range(3)])
        return user.User('name', self.home_coord)

    def get_tst_state(self):
        return ('name', [])
