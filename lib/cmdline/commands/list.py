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

from .. import format_object
from .base import CommandMixin


class List(CommandMixin):
    """List the objects that can be focussed on."""
    def __list_planets(self, opts):
        planets = self.engine.get_focusable_objects()
        format_object.print_object(format_object.planet_summary, planets)

    def __show_focussed(self, opts):
        if not self.current_object:
            print('No focussed object, listing all available...\n')
            self.__list_planets(opts)
            return
        print(self.current_object[1])

    def __setup_parser(self):
        parser = ArgumentParser(prog='list', description=List.__doc__)
        self._add_argument(parser, '-a', '--available',
                           const=self.__list_planets,
                           help="Print list of available objects.")
        parser.add_argument('-v', '--verbose', action='store_true',
                            dest='verbose', default=False)
        parser.set_defaults(action=self.__show_focussed)

        return parser, self.__list_planets

    def do_list(self, line):
        super(List, self)._do(line, self.__setup_parser)

    def help_list(self):
        print(List.__doc__)

    do_ls = do_list
