from collections import defaultdict

from lib.rst import indent

from system import System
from coord import Coord

class Galaxy(object):
    def __init__(self):
        self.__systems = defaultdict(System)

    @property
    def system(self, coord):
        system_coord = Coord(coord.x, coord.y)
        system_coord.planet = None
        return self.__systems[system_coord]

    @property
    def planet(self, coord):
        system = self.system(coord)
        return system.planets[coord.planet]

    def __repr__(self):
        return ("Galaxy(systems=[%s])" %
                ','.join([str(system)
                          for system in self.__systems.iteritems()]))

    def show(self):
        systems = []
        for c, s in self.__systems.iteritems():
            sys = indent(s.show(), '  ')[2:]
            systems.append('%s %s' % (c, sys))
        return 'Galaxy:\n%s' % indent('\n'.join(systems), '  ')
