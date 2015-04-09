import sys, pickle
from logging import debug
from random import randint

from .model import GameState
from .cmdline import ui

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
