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

from math import log10
from logging import debug

from .resources import Resources


class BuildingRequirements(object):
    def __init__(self, resources=None, research=None, buildings=None):
        self.resources = resources
        if not self.resources:
            self.resources = Resources()

        self.research = research
        if self.research is None:
            self.research = dict()

        self.buildings = buildings
        if self.buildings is None:
            self.buildings = dict()

    def __repr__(self):
        return ("{}(Resources: {}, Research: {}, Buildings: {})".format(
            self.__class__.__name__, repr(self.resources), repr(self.research),
            repr(self.buildings)))

    def __str__(self):
        return "Resources: {}\nResearch: {}\nBuildings: {}".format(
                str(self.resources).replace('\n', ', '), self.research,
                self.buildings)


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
        return BuildingRequirements()

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
            if (bldng not in build_site.buildings or
                    reqs.buildings[bldng] > build_site.buildings[bldng]):
                return False
        # TODO: implement research requirements here
        return True


class Mine(Building):
    name = 'Mine'
    abbr = 'Mn'

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
        return BuildingRequirements(resources=Resources(
            ore=10+(2*(-1+self.level)), metal=-10+(5*(1+self.level)),))


class SolarPowerPlant(Building):
    name = 'Solar Power Plant'
    abbr = 'SPP'

    def __init__(self, level=None, sun_cb=None):
        self.sun_cb = sun_cb
        super(SolarPowerPlant, self).__init__(level)

    @property
    def modifier(self):
        return Resources()

    @property
    def electricity(self):
        if not self.sun_cb:
            return 0
        return 10 * abs(log10(self.sun_cb())) * self.level

    @property
    def requirements(self):
        return BuildingRequirements(resources=Resources(
            ore=10+(5*self.level), metal=50+(6*self.level)))


ALL_BUILDINGS = [Mine, SolarPowerPlant]


def get_all_buildings():
    return [cls.name for cls in ALL_BUILDINGS]


def get_all_abbr():
    return [cls.abbr for cls in ALL_BUILDINGS]


def get_building(building_name, level=None):
    debug('getting building type %s, lvl %s' % (building_name, level))
    bld = None
    for building in ALL_BUILDINGS:
        if (building.name.lower() == building_name.lower() or
                building.abbr.lower() == building_name.lower()):
            bld = building
    else:
        debug('')
    if level is None:
        return bld
    else:
        return bld(level)
