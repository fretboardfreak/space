import sys, pickle
from logging import debug
from random import randint

from lib.model import GameState

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
