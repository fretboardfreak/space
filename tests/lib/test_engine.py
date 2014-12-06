#!/usr/bin/env python

import sys, os, unittest, pickle
from mock import patch, Mock, mock_open

# Add space root directory to import path
script_dir, _ = os.path.split(sys.argv[0])
space_dir = os.path.abspath(os.path.join(script_dir, '../..'))
sys.path.insert(1, space_dir)

import lib.engine as engine

class TestEngine(unittest.TestCase):

    save_file = 'blah'

    def setUp(self):
        engine.GameState = Mock()
        self.engine = engine.SpaceEngine(self.save_file)
        self.engine.state.save_file = self.save_file

    def test_load(self):
        #mopen = mock_open()

        string = 'foo'
        read_data = pickle.dumps(string)
        with patch('__main__.open',
                   mock_open(read_data=read_data),
                   create=True) as mopen:
            self.engine.load()

        self.assertTrue(engine.pickle.load.called)

        #open_args, _ = mopen.call_args
        #self.assertTrue(open_args[0], self.save_file)


if __name__ == "__main__":
    unittest.main()
