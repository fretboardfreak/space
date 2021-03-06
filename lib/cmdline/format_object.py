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

"""format_object: Format game model objects for the cmdline UI."""

from logging import debug
from textwrap import indent

from lib.error import ObjectNotFound


def print_object(fmt_func, *args, **kwargs):
    print(fmt_func(*args, **kwargs))


def galaxy(_galaxy):
    systems = []
    debug('showing the galaxy...')
    for c, s in _galaxy._systems.items():
        sys = indent(system(s), '  ')[2:]
        systems.append('{} {}'.format(c, sys))
    return 'Galaxy:\n{}'.format(indent('\n'.join(systems), '  '))


def user(_user, verbose=None):
    debug('showing user {}: verbose {}'.format(_user.name, verbose))
    planets = indent(user_planets(_user, verbose), '    ')
    return ("User: %s\n%s" % (_user.name, planets))


def user_planets(_user, verbose=None):
    debug("showing user {}'s planets: verbose={}".format(_user.name, verbose))
    planets = ['Planets:']
    planets.extend(' {}'.format(_coord) for _coord in _user.planets)
    return '\n'.join(planets)


def _planet_available_buildings(_engine, _planet, verbose=None):
    try:
        _coord, _planet = _engine.user.get_planet(_planet)
    except ObjectNotFound as e:
        print("Could not find that planet")
        if verbose:
            print(e)
        return
    avail = _planet.get_available_buildings()
    msg = "%s: %s\n" % (_coord, _planet.name)
    msg += ''.join('\n  - %s: %s\n%s' %
                   (bld.name, lvl,
                    indent(str(bld(lvl).requirements.resources), '    - '))
                   for bld, lvl in avail)
    return msg


def planet_available_buildings(_engine, _planet, verbose=None):
    # TODO: refactor this so that the planet object is passed in rather than
    # the planet name and the whole engine
    if _planet is None:
        msg = [_planet_available_buildings(_engine, plnt.name, verbose)
               for plnt in _engine.user.planets.values()]
        return '\n'.join(msg)
    return _planet_available_buildings(_engine, _planet, verbose)


def system(_system, _coord=None):
    msg = "%s planet system"
    if _coord is not None:
        msg += " at %s" % _coord
    msg += "\n[%s]" % ', '.join(str(p) for p in _system.planets)
    return msg


def planet_summary(planet_map):
    """Summarize a list of planets and their coordinates.

    To preserve order planet_map can be a list of 2 item tuples instead of a
    dict.
    """
    line = "[{}]: {}: {}\n"
    ret_val = ""
    iterable = planet_map
    if isinstance(planet_map, dict):
        iterable = list(planet_map.items())
    for num, (coord, planet) in enumerate(iterable):
        ret_val += line.format(num, coord, planet.name)
    return ret_val
