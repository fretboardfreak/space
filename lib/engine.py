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
import os
from logging import debug

from .model import GameState, Galaxy, User, Coord


class SpaceEngine(object):
    def __init__(self, save_file):
        self.state = GameState(save_file)

    def load(self):
        '''Load game state directly. Useful when used on the interpreter'''
        debug('Loading saved game')
        if not os.path.exists(self.state.save_file):
            debug('No save file to load.')
            raise FileNotFoundError('No save file to load.')
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
            system = self.state.galaxy.system(self.state.user.planets[0])
            planet = system.planets[int(self.state.user.planets[0].planet)]
            planet.resources.ore = 25
            planet.resources.metal = 60
            planet.emperor = self.state.user.name
        finally:
            self.save()

    def mock_new_game_info_cb(self, system_callback):
        """Mock callback for creating test gamestates"""
        coord, name = Coord(), "emperor nim"
        # the callback side effect creates a system object
        self._system_callback(coord)
        return (name, coord)
