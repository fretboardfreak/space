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
from logging import debug
from textwrap import indent

from lib.model import User, Galaxy, Coord
from lib.error import ObjectNotFound, UserInputError

RETRY_ATTEMPTS = 3


def input_bool(msg):
    debug('getting a boolean from the user')
    msg = str(msg) + ' (y|n) '
    for attempt in range(RETRY_ATTEMPTS):
        x = input(msg).strip().lower()
        if x.startswith('y'):
            return True
        elif x.startswith('n'):
            return False
        debug('  {} cannot be interpreted as a boolean, tries '
              'remaining {}'.format(RETRY_ATTEMPTS - attempt))
    else:
        raise UserInputError('Failed to receive a boolean from the user '
                             'after {} tries.'.format(RETRY_ATTEMPTS))


def input_text(msg):
    debug('getting some text from the user')
    for _ in range(RETRY_ATTEMPTS):
        name = input(msg)
        if name.isalpha():
            return name
    else:
        raise UserInputError('Failed to receive a string from the user '
                             'after {} tries.'.format(RETRY_ATTEMPTS))


def input_int(msg, minimum=None, maximum=None):
    debug('getting an int from the user')
    for _ in range(RETRY_ATTEMPTS):
        num = input(msg)
        try:
            num = int(num)
            break
        except:
            debug('  {} is not a number.'.format(num))
            continue
        if minimum is not None and num < minimum:
            debug("too small (minimum=%s)" % minimum)
            continue
        if maximum is not None and num > maximum:
            debug("too large (maximum=%s)" % maximum)
            continue
    else:
        raise UserInputError('Failed to receive an int from the user '
                             'after {} tries.'.format(RETRY_ATTEMPTS))
    return num


def _show_available_buildings(engine, planet, verbose=None):
    try:
        coord, planet = engine.state.user.get_planet(planet)
    except ObjectNotFound as e:
        print("Could not find that planet")
        if verbose:
            print(e)
        return
    avail = planet.get_available_buildings()
    msg = "%s: %s\n" % (coord, planet.name)
    msg += ''.join(['\n  - %s: %s\n%s' %
                    (bld.name, lvl,
                     indent(str(bld(lvl).requirements.resources), '    - '))
                    for bld, lvl in avail])
    return msg


def show_available_buildings(engine, planet, verbose=None):
    if planet is None:
        msg = [_show_available_buildings(engine, plnt.name, verbose)
               for plnt in engine.state.user.planets.itervalues()]
        print('\n'.join(msg))
        return
    print(_show_available_buildings(engine, planet, verbose))


def start_new_game(engine):
    msg = 'Do you want to start a new game?'
    input_bool(msg) or sys.exit(0)
    debug('Creating a new game')

    try:
        # create new galaxy
        engine.state.galaxy = Galaxy()

        # create new user
        def system_callback(coords):
            engine.state.galaxy.system(coords)

        user_info = newgame_get_user_info(system_callback)
        engine.state.user = User(*user_info)
    finally:
        engine.save()


def newgame_get_user_info(system_query_cb):
    debug('Querying user for new game info...')
    name = input_text("Great another wanna be space emperor! "
                      "What's your name then? ")

    home_coords = Coord()
    sec_x = input_int('Ok, now we need to find your home planet. '
                      'Enter the sector coords:\nx=')
    sec_y = input_int('y=')
    home_coords.sector = (sec_x, sec_y)

    sys_x = input_int('Now the system coords:\nx=')
    sys_y = input_int('y=')
    home_coords.system = (sys_x, sys_y)

    system = system_query_cb(home_coords)
    planet_num_qry = ('That system has %s planets. Which one did you say '
                      'was yours?\n%s\nplanet=' %
                      (len(system.planets),
                       '\n'.join([' %s. %s' % (i, p.name) for i, p in
                                  enumerate(system.planets)])))
    planet_num = input_int(planet_num_qry, min=0,
                           max=len(system.planets) - 1)
    home_coords.planet = planet_num
    home_planet = system.planets[planet_num]
    home_planet.resources.ore = 25
    home_planet.resources.metal = 60
    print("We've given you some building materials to get you started. "
          "Use them wisely, that's all the new recruits get from us!")

    return (name, home_coords, home_planet)
