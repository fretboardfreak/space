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


def print_object(fmt_func, *args, **kwargs):
    print(fmt_func(*args, **kwargs))


def galaxy(galaxy):
    systems = []
    debug('showing the galaxy...')
    for c, s in galaxy._systems.iteritems():
        sys = indent(system(s), '  ')[2:]
        systems.append('{} {}'.format(c, sys))
    return 'Galaxy:\n{}'.format(indent('\n'.join(systems), '  '))


def user(user, verbose=None):
    debug('showing user {}: verbose {}'.format(user.name, verbose))
    planets = indent(user_planets(user, verbose), '    ')
    return ("User: %s\n%s" % (user.name, planets))


def user_planets(user, verbose=None):
    debug("showing user {}'s planets: verbose={}".format(user.name, verbose))
    planets = ['Planets:']
    for coord, planet in user.planets.items():
            planets.append(' {}: {}'.format(coord, planet(planet, verbose)))
    return '\n'.join(planets)


def planet(planet, verbose=None, rates=None):
    if rates is None:
        rates = True
    details = []
    planet.update()
    if verbose:
        rates = True
        sun = 'Sun: dist: {}  brightness: {}'.format(planet.sun_distance,
                                                     planet.sun_brightness)
        details.append(sun)
    if rates:
        res = '\n'.join(['- {}: {} ({})'.format(
            name, planet.resources[name], planet.rates[name])
            for name in planet.resources])
    else:
        res = indent(str(planet.resources), '- ')
    details.append(indent(res, '  '))

    bldngs = '\n'.join(['- {}'.format(str(bld))
                        for bld in planet.buildings.values()])
    details.append(bldngs)
    return "Planet {}, owner {}\n{}".format(planet.name, planet.emperor,
                                            '\n'.join(details))


def system(system, coords=None):
    msg = "%s planet system"
    if coords is not None:
        msg += " at %s" % coords
    msg += "\n[%s]" % ', '.join([planet(p) for p in system.planets])
    return msg