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

from logging import debug

from lib.error import UserInputError
from lib import model

RETRY_ATTEMPTS = 3


def input_bool(msg):
    debug('getting a boolean from the user')
    msg = str(msg) + ' (y|n) '
    for attempt in range(RETRY_ATTEMPTS):
        value = input(msg).strip().lower()
        if value.startswith('y'):
            return True
        elif value.startswith('n'):
            return False
        debug('  {} cannot be interpreted as a boolean, tries '
              'remaining {}'.format(value, RETRY_ATTEMPTS - attempt))
    else:
        raise UserInputError('Failed to receive a boolean from the user '
                             'after {} tries.'.format(RETRY_ATTEMPTS))


def input_text(msg):
    debug('getting some text from the user')
    for _ in range(RETRY_ATTEMPTS):
        name = input(msg)
        if hasattr(name, 'isprintable') and name.isprintable():
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


def get_new_game_info(system_query_cb):
    debug('Querying user for new game info...')
    name = input_text("Great another wanna be space emperor! "
                      "What's your name then? ")

    home_coords = model.Coord()
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
                       '\n'.join(' %s. %s' % (i, p.name) for i, p in
                                 enumerate(system.planets))))
    planet_num = input_int(planet_num_qry, minimum=0,
                           maximum=len(system.planets) - 1)
    home_coords.planet = planet_num
    print("Okay, here's some building materials to get you started. "
          "Use them wisely, that's all the new recruits get from us!")

    return (name, home_coords)
