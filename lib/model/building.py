from lib.util import AttrDict
from resources import Resources


class Building(object):
    def __init__(self, level=None):
        if level is None:
            self.level = 1
        else:
            self.level = level

    @property
    def modifier(self):
        return Resources()

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
        return ((reqs.resources == build_site.resources) and
                (len(reqs.research) == \
                    len(reqs.research.intersection(build_site.research))) and
                (len(reqs.buildings) == \
                    len(reqs.buildings.intersection(build_site.buildings))))


class Mine(Building):
    def __init__(self, level=None):
        super(Mine, self).__init__(level)

    @property
    def modifier(self):
        return Resources(ore=2*self.level)

    @property
    def requirements(self):
        return AttrDict([
            ('resources', Resources(
                ore=10+(2*(-1+self.level)),
                metal=-10+(5*(1+self.level)),
                electricity=3)),
            ('research', set()),
            ('buildings', set()),
            ])


class SolarPowerPlant(Building):
    def __init__(self, level=None):
        super(SolarPowerPlant, self).__init__(level)

    @property
    def modifier(self):
        return Resources(electricity=10+2*self.level)

    @property
    def requirements(self):
        return AttrDict([
            ('resources', Resources(
                ore=10+(5*self.level),
                metal=100+(6*self.level))),
            ('research', set()),
            ('buildings', set()),
            ])


ALL_BUILDINGS = [Mine, SolarPowerPlant]
