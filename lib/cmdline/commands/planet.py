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
from .. import format_object
from lib import model


class Planet(CommandMixin):
    def __build(self, args):
        if args.building is None:
            format_object.print_object(
                format_object.planet_available_buildings, self.engine,
                args.planet, args.verbose)
            return
        coord, planet = self.engine.state.user.get_planet(args.planet)
        if planet.build(args.building):
            print("Congrats, you just built a %s" % args.building)
        else:
            print("Construction Failed! Make sure you have enough "
                  "resources and try again.")

    def __show_planets(self, args):
        if args.planet in [None, '']:
            format_object.print_object(format_object.user_planets,
                                       self.engine.state.user, args.verbose)
            return
        coord, planet = self.engine.state.user.get_planet(args.planet)
        print(planet.show(verbose=args.verbose))

    def do_planet(self, line):
        try:
            parser = ArgumentParser(prog='planet',
                                    description=self.help_show(True))
            parser.add_argument('-v', '--verbose', action='store_true',
                                dest='verbose', default=False)
            parser.add_argument('-b', '--build', action='store_const',
                                dest='action', const=self.__build)
            parser.add_argument('planet', help='Limit the effect of the '
                                'command to this planet (if supported)',
                                default=None, nargs='?')
            parser.add_argument('building', help='Name of building type to '
                                'pass to the command %s (if supported, '
                                'PLANET must be supplied first)'
                                % str(model.get_all_building_abbr()),
                                default=None, nargs='?')

            (args, params) = parser.parse_known_args(line.split(' '))
            setattr(args, 'params', params)
            if args.action is None:
                args.action = self.__show_planets
            args.action(args=args)
        except SystemExit:
            pass
        return False

    def help_planet(self):
        print("Access to things on planets")
    do_p = do_planet
    do_pl = do_planet
