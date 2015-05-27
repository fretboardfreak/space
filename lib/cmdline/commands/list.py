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
from functools import partial

from .. import format_object
from .base import CommandMixin


class List(CommandMixin):
    def do_list(self, line):
        list_planets = partial(format_object.print_object,
                               format_object.user_planets,
                               self.engine.state.user)
        list_user = partial(format_object.print_object, format_object.user,
                            self.engine.state.user)
        try:
            parser = ArgumentParser(prog='list',
                                    description=self.help_list(True))
            parser.add_argument('-p', '--planets', action='store_const',
                                dest='subject', const=list_planets)
            parser.add_argument('-u', '--user', action='store_const',
                                dest='subject', const=list_user)
            parser.add_argument('-v', '--verbose', action='store_true',
                                dest='verbose', default=False)

            (args, params) = parser.parse_known_args(line.split(' '))
            setattr(args, 'params', params)
            if args.subject is None:  # no arguments
                args.subject = list_planets
            args.subject(verbose=args.verbose)
        except SystemExit:
            pass
        return False

    def help_list(self, no_print=None):
        msg = "Show various things. Use 'list --help' for more."
        if no_print:
            return msg
        print(msg)
    do_ls = do_list
