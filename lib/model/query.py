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
        """Retrieve tuples of (Coord, Planet) of the planets owned by user."""
        for coord in user.planets:
            yield coord, self.galaxy.planet(coord)

    def get_focusable_objects(self):
        """Return a list of objects that can be focussed on."""
        return list(self.user_planets(self.user))

    def get_object_id_map(self):
        """Map acceptable Object ID strings to the focusable objects."""
        id_map = {}
        for num, (coord, obj) in enumerate(self.get_focusable_objects()):
            value = (coord, obj)
            id_map[obj.name] = value
            id_map[obj.name.upper()] = value
            id_map[obj.name.lower()] = value
            id_map[str(num)] = value
        return id_map
