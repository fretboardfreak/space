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


class ModelQueryMixin(object):

    """A drop in query interface for the game model.

    Engine object requires "self.galaxy" to be a valid Galaxy object. Any other
    assumption should be made by the engine class itself.
    """

    def user_planets(self, user):
        for coord in user.planets:
            yield coord, self.galaxy.planet(coord)
