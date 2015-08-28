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


class Build(CommandMixin):
    """Construct or interact with building objects."""
    def __build(self, opts):
        if not self.current_object:
            print('No focussed planet to build on.')
            return
        if not opts.building_type:
            print('No building type provided. Listing buildings that can '
                  'be constructed.\n')
            buildings = []
            for bld, level in self.current_object[1].get_available_buildings():
                buildings.append("- {}: lvl {}".format(bld.name, level))
            print('  ' + '\n  '.join(buildings))
        else:
            result = self.current_object[1].build(opts.building_type)
            if result:
                print('{} has been constructed.'.format(opts.building_type))
            else:
                print('Could not construct a {}. Make sure you have enough '
                      'resources.'.format(opts.building_type))

    def __setup_parser(self):
        parser = ArgumentParser(prog='build', description=Build.__doc__)
        parser.add_argument(dest='building_type')
        parser.set_defaults(action=self.__build)
        return parser, self.__build

    def do_build(self, line):
        super(Build, self)._do(line, self.__setup_parser)

    def help_build(self):
        print(Build.__doc__)
