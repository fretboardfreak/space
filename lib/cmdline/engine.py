import sys, pickle
from logging import debug
from random import randint

from lib.model import GameState, User, Galaxy, Coord
from lib.namegen import NameGen

import ui

class SpaceEngine(object):
    def __init__(self, save_file):
        self.state = GameState(save_file)

    def load(self):
        '''Load game state directly. Useful when used on the interpreter'''
        debug('Loading saved game')
        with open(self.state.save_file, 'r') as sf:
            self.state = pickle.load(sf)

    def save(self):
        debug('Saving game')
        with open(self.state.save_file, 'w') as fd:
            pickle.dump(self.state, fd)

    def start_new_game(self):
        msg = 'Do you want to start a new game?'
        ui.input_bool(msg) or sys.exit(0)
        debug('Creating a new game')

        try:
            # create new galaxy
            self.state.galaxy = Galaxy()

            # create new user
            system_callback = lambda coords: self.state.galaxy.system(coords)
            user_info = ui.newgame_get_user_info(system_callback)
            self.state.user = User(*user_info)
        finally:
            self.save()
