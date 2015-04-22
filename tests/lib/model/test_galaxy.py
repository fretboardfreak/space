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

# from lib import model
from lib.model import galaxy


class TestLibModelGalaxy(LibModelTest):
    def setUp(self):
        self.expected_exports = [galaxy.Galaxy]


class TestGalaxy(ModelObjectTest, StateMixinTest):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.expected_state = (dict,)
        self.classname_in_repr = True
        self.expected_attrs = {}

    def get_new_instance(self):
        return galaxy.Galaxy()

    def get_tst_state(self):
        return ({},)

    def test_system(self):
        self.skipTest('NIY')

    def test_planet(self):
        self.skipTest('NIY')
