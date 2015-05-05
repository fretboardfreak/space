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

import sys
from unittest.mock import patch
from itertools import product

from .base import SpaceTest

import space


class TestSpace(SpaceTest):
    def setUp(self):
        self.save_file_opt = 'save_file'
        self.log_file_opt = 'log_file'
        self.defaults = {self.save_file_opt: 'save.space',
                         self.log_file_opt: 'runlog'}
        self.save_flags = ['-s', '--save-file']
        self.log_flags = ['-l', '--log-file']
        self.orig_argv = sys.argv

        # prevent parser.error output on tests, nose buffers stdout not stderr
        self.orig_stderr = sys.stderr
        sys.stderr = sys.stdout

    def tearDown(self):
        sys.argv = self.orig_argv
        sys.stderr = self.orig_stderr

    def get_option_key(self, flag):
        if flag in self.save_flags:
            return self.save_file_opt
        elif flag in self.log_flags:
            return self.log_file_opt
        else:
            raise Exception('{} is not a valid flag for space.py'.format(flag))

    def test_parse_args_default(self):
        sys.argv = ['prog']
        args = space.parse_args()
        for default in self.defaults:
            self.assertTrue(hasattr(args, default))
            self.assertEqual(getattr(args, default), self.defaults[default])

    def test_parse_args_flag_present_no_argument(self):
        for flag in self.save_flags + self.log_flags:
            sys.argv = ['prog', flag]
            self.assertRaises(SystemExit, space.parse_args)

    def test_parse_args_one_flag_present(self):
        fname = 'filename'
        for flag in self.save_flags + self.log_flags:
            sys.argv = ['prog', flag, fname]
            args = space.parse_args()
            option = self.get_option_key(flag)
            self.assertEqual(getattr(args, option), fname)

    def test_parse_args_all_flags(self):
        save_file = 'some_save_file',
        log_file = 'a_log_file'
        expected = {self.save_file_opt: save_file,
                    self.log_file_opt: log_file}
        test_iterator = product([(flag, save_file)
                                 for flag in self.save_flags],
                                [(flag, log_file)
                                 for flag in self.log_flags])
        for ((one, two), (three, four)) in test_iterator:
            sys.argv = ['prog', one, two, three, four]
            args = space.parse_args()
            for key in expected:
                self.assertEquals(getattr(args, key), expected[key])

    def test_parse_args_extra_args(self):
        fname = 'filename'
        extra = 'something_extra'
        for flag in self.save_flags + self.log_flags:
            sys.argv = ['prog', flag, fname, extra]
            self.assertRaises(SystemExit, space.parse_args)

    @patch('space.parse_args', autospec=True)
    @patch('space.logging.basicConfig', autospec=True)
    @patch('space.SpaceCmdInterpreter', autospec=True)
    @patch('space.SpaceEngine', autospec=True)
    def test_main(self, mock_engine, mock_interpreter, mock_log_config,
                  mock_parse_args):
        space.main()
        self.assertTrue(mock_engine.called)
        self.assertTrue(mock_interpreter.called)
        self.assertTrue(any([True for call in mock_interpreter.mock_calls
                             if 'start' in call[0]]))
