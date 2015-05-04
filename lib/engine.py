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

import pickle
from logging import debug

from .model import GameState, Galaxy, User


class SpaceEngine(object):
    def __init__(self, save_file):
        self.state = GameState(save_file)

    def load(self):
        '''Load game state directly. Useful when used on the interpreter'''
        debug('Loading saved game')
        with open(self.state.save_file, 'rb') as sf:
            self.state = pickle.load(sf)

    def save(self):
        debug('Saving game')
        with open(self.state.save_file, 'wb') as fd:
            pickle.dump(self.state, fd)

    def _system_callback(self, coords):
        return self.state.galaxy.system(coords)

    def new_game(self, new_game_info_cb):
        """Set up a new game.

        :param new_game_info_cb: UI callable that will retrieve info from the
            user and return a tuple of (username, home_planet_coords,
            home_planet)
        """
        try:
            self.state.galaxy = Galaxy()
            self.state.user = User(*new_game_info_cb(self._system_callback))
        finally:
            self.save()
