import sys
import os
import unittest
import pickle
import tempfile
from mock import Mock

#import lib.engine as engine


class MockGameState(object):
    def __init__(self, *args, **kwargs):
        self.save_file = None


@unittest.skip('lib.model is in the process of being refactored')
class TestEngine(unittest.TestCase):

    def setUp(self):
        self.save_file = tempfile.NamedTemporaryFile()
        engine.GameState = MockGameState
        self.engine = engine.SpaceEngine(self.save_file)
        self.engine.state.save_file = self.save_file.name

    def test_load(self):
        orig_state = hash(self.engine.state)
        pickle.dump(self.engine.state, self.save_file.file)
        self.save_file.file.seek(0)

        self.engine.load()

        self.assertTrue(orig_state, hash(self.engine.state))
