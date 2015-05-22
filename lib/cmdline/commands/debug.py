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

from argparse import ArgumentParser

from .base import CommandMixin


class Debug(CommandMixin):
    def __print_state(self):
        print(self.engine.state)

    def do_debug(self, line):
        try:
            parser = ArgumentParser(
                prog='dbg', description=self.help_debug(True))
            parser.add_argument(
                '-ps', '--print-state', action='store_const',
                dest='action', const=self.print_state,
                help='print full game state')
            (args, unrecognized) = parser.parse_known_args(line.split(' '))
            if args.action is None:
                self.print_state()
            else:
                args.action()
        except SystemExit:
            pass
        return False

    def help_debug(self, no_print=None):
        hlp = "Provides access to some debugging commands."
        if no_print:
            return hlp
        print(hlp)
    do_dbg = do_debug
