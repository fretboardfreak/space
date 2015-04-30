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

import os
import subprocess

from .base import SpaceTest


class TestPep8(SpaceTest):
    def setUp(self):
        self.errors = []
        self.file_filters = [lambda f: not f.startswith('.'),
                             lambda f: not f.endswith('.swp'),
                             lambda f: not f.endswith('.pyc'),
                             lambda f: '__pycache__' not in f]
        self.err_msg = 'Style errors were found:\n{}'

    def gather_filepaths(self, top):
        filepaths = []
        for path, dirs, files in os.walk(top):
            for filename in files:
                if all([test(filename) for test in self.file_filters]):
                    filepaths.append(os.path.join(path, filename))
        return filepaths

    def _run_cmd(self, cmd):
        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT,
                                    universal_newlines=True)
        except subprocess.CalledProcessError as err:
            self.errors.append(err.output.strip())

    def run_pep8(self, path):
        return self._run_cmd(['pep8', path])

    def run_pyflakes(self, path):
        return self._run_cmd(['pyflakes', path])

    def fail_on_errors(self):
        self.errors = [err for err in self.errors if err is not None]
        if self.errors:
            print(self.err_msg.format('\n'.join(self.errors)))
            self.fail()

    def tst_style(self, path, checker):
        for path in self.gather_filepaths(path):
            checker(path)
        self.fail_on_errors()

    def get_path(self, path):
        return os.path.join(os.getcwd(), path)

    def test_tests_pep8(self):
        self.tst_style(self.get_path('tests'), self.run_pep8)

    def test_lib_pep8(self):
        # TODO: Add the remainder of the lib package to this test as things get
        # refactored.
        self.tst_style(self.get_path('lib/model'), self.run_pep8)
        self.tst_style(self.get_path('lib/namegen.py'), self.run_pep8)

    def test_space_pep8(self):
        self.run_pep8(self.get_path('space'))
        self.fail_on_errors()

    def test_tests_pyflakes(self):
        self.tst_style(self.get_path('tests'), self.run_pyflakes)

    def test_lib_pyflakes(self):
        self.tst_style(self.get_path('lib'), self.run_pyflakes)

    def test_space_pyflakes(self):
        self.run_pyflakes(self.get_path('space'))
        self.fail_on_errors()
