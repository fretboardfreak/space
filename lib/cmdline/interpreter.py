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
from argparse import ArgumentParser
from cmd import Cmd
from logging import debug

from . import ui
from . import format_object
from lib import model

from . import commands


class Planet(commands.CommandMixin):
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


class User(commands.CommandMixin):
    def do_user(self, line):
        # TODO: implement change name
        print('Not implemented yet')

    def help_user(self):
        print("Access to user admin tasks")
    do_u = do_user


class SpaceCmdInterpreter(Cmd, commands.Quit, commands.Debug, commands.Show,
                          Planet, User):
    def __init__(self, engine):
        super(SpaceCmdInterpreter, self).__init__()
        self.engine = engine
        self.prompt = 'space> '
        self.doc_header = 'Space Commands'
        self.undoc_header = 'Alias Commands'

    def start(self):
        try:
            try:
                debug('Trying to load the saved game...')
                self.engine.load()
            except FileNotFoundError:
                debug('No save game, starting new game...')
                self.start_new_game()
            debug('Starting interpreter...')
            self.cmdloop()
        except (KeyboardInterrupt, SystemExit):
            debug('Recieved Interrupt.')
        except Exception:
            debug('Received Unknown Exception, exiting...',
                  exc_info=True, stack_info=True)
        finally:
            self.engine.save()

    def start_new_game(self):
        msg = 'Do you want to start a new game?'
        ui.input_bool(msg) or sys.exit(0)
        debug('Creating a new game')
        self.engine.new_game(ui.get_new_game_info)
