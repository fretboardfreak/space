""" Space Object Model
"""

import random
from collections import defaultdict

from lib.rst import indent


from planet import Planet, METAL, THORIUM
from coord import Coord

class GameState(object):
    def __init__(self, save_file=None):
        self.save_file = save_file
        self.user = None
        self.galaxy = None

    def __repr__(self):
        return ("GameState(save_file=%s,%s,%s)" %
                (self.save_file, self.user, self.galaxy))

class User(object):
    def __init__(self, name, home_planet_coords, home_planet):
        self.name = name
        self.planets = {home_planet_coords: home_planet}
        home_planet.emperor = self.name

    def __repr__(self):
        return ("User(name=%s, planets=%s)" %
                (self.name, self.planets))

    def show_planets(self):
        planets = []
        for coord, planet in self.planets.iteritems():
            planets.append('%s: %s' % (coord, planet.show()))
        return '\n'.join(planets)

    def show(self):
        planets = indent(self.show_planets(), '    ')
        return ("User: %s\n  planets:\n%s" %
                (self.name, planets))

class Galaxy(object):
    def __init__(self):
        self.systems = defaultdict(System)

    def __repr__(self):
        return ("Galaxy(systems=[%s])" %
                ','.join([str(system) for system in self.systems.iteritems()]))

    def show(self):
        systems = []
        for c, s in self.systems.iteritems():
            sys = indent(s.show(), '  ')[2:]
            systems.append('%s %s' % (c, sys))
        return 'Galaxy:\n%s' % indent('\n'.join(systems), '  ')

class System(object):
    def __init__(self):
        self._size_range = (4, 20)
        self.planets = [Planet() for i in
                        range(random.randint(*self._size_range))]

    def __repr__(self):
        return ("System(size=%s, planets=%s)" %
                (self._size_range, self.planets))

    def show(self, coords=None):
        msg = "%s planet system"
        if coords is not None:
            msg += " at %s" % coords
        msg += "\n[%s]" % ', '.join([p.show() for p in self.planets])
        return msg
