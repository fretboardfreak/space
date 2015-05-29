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
    def __list_planets(self, args):
        format_object.print_object(format_object.user_planets,
                                   self.engine.state.user)

    def __setup_parser(self):
        parser = ArgumentParser(prog='list', description=List.__doc__)
        self._add_argument(parser, '-p', '--planets',
                           const=self.__list_planets,
                           help="[DEFAULT] List focussable planets.")
        parser.add_argument('-v', '--verbose', action='store_true',
                            dest='verbose', default=False)

        return parser, self.__list_planets

    def do_list(self, line):
        super(List, self)._do(line, self.__setup_parser)

    def help_list(self):
        print(List.__doc__)

    do_ls = do_list
