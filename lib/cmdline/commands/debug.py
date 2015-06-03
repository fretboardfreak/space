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

from logging import info
from argparse import ArgumentParser
import code

from lib.engine import SpaceEngine
from .base import CommandMixin


class Debug(CommandMixin):
    """Provides access to some debugging features."""

    def __print_state(self, args):
        print(self.engine.state)

    def __interactive(self, args):
        local = {"__name__": "__debug_console__", "__doc__": None,
                 "engine": self.engine}
        code.interact(local=local)

    def __new_state(self, args):
        info('Creating new test state...')
        self.engine = SpaceEngine(self.engine.state.save_file)
        self.engine.new_game(self.engine.mock_new_game_info_cb)

    def __setup_parser(self):
        parser = ArgumentParser(prog='debug', description=Debug.__doc__)
        self._add_argument(parser, '-ps', '--print-state',
                           const=self.__print_state,
                           help='[Default] print full game state.')
        self._add_argument(parser, '-i', '--interactive',
                           const=self.__interactive,
                           help='Start interactive python session.')
        self._add_argument(parser, '-n', '--new-state',
                           const=self.__new_state,
                           help='Create a new test state. Note: A new'
                           ' state will override the existing one.')
        return parser, self.__print_state

    def do_debug(self, line):
        super(Debug, self)._do(line, self.__setup_parser)

    def help_debug(self):
        print(Debug.__doc__)

    do_dbg = do_debug
