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

from ..ui import input_bool

from .base import CommandMixin


class User(CommandMixin):
    """Interact with your profile and check your stats."""
    def __print_stats(self, opts):
        building_count = 0
        per_second_income = 0
        for coord, planet in self.engine.user_planets(self.engine.user):
            building_count += len(planet.buildings)
            per_second_income += planet.rates.trade_value

        print("{}:\n  {} planets\n  {} buildings\n"
              "  {} per second income trade value".format(
                  self.engine.user.name, len(self.engine.user.planets),
                  building_count, per_second_income))

    def __change_name(self, opts):
        try:
            new_name = opts.args.pop(0)
        except IndexError:
            print("You can't change your name to nothing. Give us "
                  "a new name for the records if you want a new one.")
            return
        prompt = ("Are you sure you want to change your name from "
                  "'{}' to '{}'".format(self.engine.user.name, new_name))
        if not input_bool(prompt):
            print('Okay, see you next time.')
            return
        print("Okay, just let me change your name on our records...")
        # loop through user's planets and change emperor name
        for coord, planet in self.engine.user_planets(self.engine.user):
            planet.emperor = new_name

        # change user's name last
        self.engine.user.name = new_name
        print("Alright, er, {}, you should be good to go "
              "now.".format(new_name))

    def __setup_parser(self):
        parser = ArgumentParser(prog='user', description=User.__doc__)
        parser.set_defaults(action=self.__print_stats)
        self._add_argument(parser, '--change-name', const=self.__change_name,
                           help="Change your username.")
        return parser, self.__print_stats

    def do_user(self, line):
        super(User, self)._do(line, self.__setup_parser)

    def help_user(self):
        print(User.__doc__)
