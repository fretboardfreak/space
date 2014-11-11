from math import log10

from lib.util import AttrDict, DefaultAttrDict
from resources import Resources

class Building(object):
    def __init__(self, level=None):
        if level is None:
            self.level = 1
        else:
            self.level = level

    def __getstate__(self):
        return (self.level,)

    def __setstate__(self, state):
        (self.level,) = state

    @property
    def modifier(self):
        return Resources()

    @property
    def electricity(self):
        return 0

    @property
    def requirements(self):
        return AttrDict([('resources', Resources()),
                         ('research', set()),
                         ('buildings', set()),
                        ])

    def __repr__(self):
        return ("%s(level=%s, mod=%s, reqs=%s)" %
               ((self.__class__.__name__, self.level, repr(self.modifier),
                 repr(self.requirements))))

    def __str__(self):
        return ("%s : level=%s\n  - modfier=%s)" %
                (self.__class__.__name__, self.level, repr(self.modifier)))

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.level == other.level)

    def __hash__(self):
        return hash("%s%s" % (self.__class__, self.level))

    @classmethod
    def are_requirements_met(cls, build_site, level=None):
        reqs = cls(level).requirements
        if reqs.resources > build_site.resources:
            return False
        for bldng in reqs.buildings:
            if bldng not in build_site.buildings:
                return False
            elif reqs.buildings[bldng] > build_site.buildings[bldng]:
                return False
        #TODO: implement research requirements here
        return True

class Mine(Building):
    name = 'Mine'
    def __init__(self, level=None):
        super(Mine, self).__init__(level)

    @property
    def modifier(self):
        return Resources(ore=2*self.level,
                         metal=0.25*self.level)

    @property
    def electricity(self):
        return -1 * pow(self.level, 2)

    @property
    def requirements(self):
        return AttrDict([
            ('resources', Resources(
                ore=10+(2*(-1+self.level)),
                metal=-10+(5*(1+self.level)),
                electricity=3)),
            ('research', DefaultAttrDict(lambda: 0)),
            ('buildings', DefaultAttrDict(lambda: 0)),
            ])


class SolarPowerPlant(Building):
    name = 'Solar Power Plant'
    def __init__(self, level=None, sun_cb=None):
        self.sun_cb = sun_cb
        super(SolarPowerPlant, self).__init__(level)

    @property
    def modifier(self):
        return Resources()

    @property
    def electricity(self):
        if not self.sun_cb: return 0
        return 10 * abs(log10(self.sun_cb())) * self.level

    @property
    def requirements(self):
        return AttrDict([
            ('resources', Resources(
                ore=10+(5*self.level),
                metal=50+(6*self.level))),
            ('research', DefaultAttrDict(lambda: 0)),
            ('buildings', DefaultAttrDict(lambda: 0)),
            ])

ALL_BUILDINGS = [Mine, SolarPowerPlant]
