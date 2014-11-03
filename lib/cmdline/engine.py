import sys, pickle
from logging import debug
from random import randint

from lib.model import GameState, User, Galaxy, Coord
from lib.namegen import NameGen

import ui

DEBUG = True

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

        if DEBUG and ui.input_bool('create test state?'):
            self.create_test_state()
            return

        try:
            # create new galaxy
            self.state.galaxy = Galaxy()

            # create new user
            system_callback = lambda coords: self.state.galaxy.system(coords)
            user_info = ui.newgame_get_user_info(system_callback)
            self.state.user = User(*user_info)
        finally:
            self.save()

    def create_test_state(self):
        debug('Creating a canned state for testing...')
        self.state.galaxy = Galaxy()
        name = NameGen('lib/namegen_lang.txt').gen_word()
        home_coords = Coord(float('%d.%d' % (randint(0, 100), randint(0, 100))),
                            float('%d.%d' % (randint(0, 100), randint(0, 100))),
                            randint(0, 2))
        system = self.state.galaxy.system(home_coords)
        home_planet = system.planets[home_coords.planet]
        self.state.user = User(name, home_coords, home_planet)
        self.save()
