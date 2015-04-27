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

import lib.model


class GameState(object):
    def __init__(self, save_file=None):
        self.save_file = save_file
        self.user = None
        self.galaxy = None

    def __repr__(self):
        return "{}(save file: {}, user: {}, galaxy: {})".format(
                self.__class__.__name__, self.save_file, repr(self.user),
                repr(self.galaxy))

    def __getstate__(self):
        user_state = None if self.user is None else self.user.__getstate__()
        gxy_state = None if self.galaxy is None else self.galaxy.__getstate__()
        return (self.save_file, user_state, gxy_state)

    def __setstate__(self, state):
        (self.save_file, user_state, galaxy_state) = state
        self.user = None
        self.galaxy = None
        if not user_state is None:
            self.user = lib.model.User(name='')
            self.user.__setstate__(user_state)
        if not galaxy_state is None:
            self.galaxy = lib.model.Galaxy()
            self.galaxy.__setstate__(galaxy_state)
