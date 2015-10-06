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
import os
from logging import debug

from .cmdline.interpreter import SpaceCmdInterpreter
from . import model


class SpaceEngine(model.ModelQueryMixin):
    def __init__(self, save_file, opts=None):
        self.save_file = save_file
        self.opts = opts
        self.user = None
        self.galaxy = None
        model.update.delayed_event_trigger.CALLABLE = (
            self.execute_delayed_events)

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
        if user_state is not None:
            self.user = model.User(name='')
            self.user.__setstate__(user_state)
        if galaxy_state is not None:
            self.galaxy = model.Galaxy()
            self.galaxy.__setstate__(galaxy_state)

    def load(self):
        '''Load game state directly. Useful when used on the interpreter'''
        debug('Loading saved game')
        if not os.path.exists(self.save_file):
            debug('No save file to load.')
            raise FileNotFoundError('No save file to load.')
        with open(self.save_file, 'r') as sf:
            state = json.load(sf)
            self.__setstate__(state[1])
            return state[0]

    def save(self, current_object=None):
        debug('Saving game')
        with open(self.save_file, 'w') as fd:
            current_obj_state = None
            if current_object:
                current_obj_state = current_object[1].name
            state = (current_obj_state, self.__getstate__())
            json.dump(state, fd)

    def _system_callback(self, coords):
        return self.galaxy.system(coords)

    def new_game(self, new_game_info_cb):
        """Set up a new game.

        :param new_game_info_cb: UI callable that will retrieve info from the
            user and return a tuple of (username, home_planet_coords,
            home_planet)
        """
        try:
            self.galaxy = model.Galaxy()
            self.user = model.User(*new_game_info_cb(self._system_callback))
            system = self.galaxy.system(self.user.planets[0])
            planet = system.planets[int(self.user.planets[0].planet)]
            planet.resources.ore = 25
            planet.resources.metal = 60
            planet.emperor = self.user.name
        finally:
            self.save()

    def mock_new_game_info_cb(self, system_callback):
        """Mock callback for creating test gamestates"""
        coord, name = model.Coord(), "emperor nim"
        return (name, coord)

    def run(self):
        SpaceCmdInterpreter(self, self.opts.debug).start()

    def execute_delayed_events(self):
        debug('delayed actions happening')
