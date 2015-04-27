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

from lib.error import ObjectNotFound

from .resources import Resources


class BuildingRequirements(object):
    def __init__(self, resources=None, research=None, buildings=None):
        self.resources = resources
        if not self.resources:
            self.resources = Resources()

        # research dict: not defined yet
        self.research = research
        if self.research is None:
            self.research = dict()

        # buildings dict: key=str, building name; value=int, building level
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

    def __getstate__(self):
        return (self.resources, self.research, self.buildings)

    def __setstate__(self, state):
        (self.resources, self.research, self.buildings) = state


class Building(object):
    def __init__(self, level=None, sun_cb=None):
        if level is None:
            self.level = 1
        else:
            self.level = level
        self.sun_cb = sun_cb
        # requirements for construction
        self._requirements = BuildingRequirements()

        # per time unit production values
        self._modifier = Resources(ore=self.level)
        self._electricity = 0

    def __getstate__(self):
        return (self.level, self.sun_cb)

    def __setstate__(self, state):
        (self.level, self.sun_cb) = state

    @property
    def modifier(self):
        """The building's per time unit resource production."""
        return self._modifier

    @property
    def electricity(self):
        """The building's per time unit electricity production/consumption."""
        return self._electricity

    @property
    def requirements(self):
        return self._requirements

    def __repr__(self):
        return ("{}(level: {}, modifier: {}, electricity: {}, "
                "requirements: {})".format(
                    self.__class__.__name__, self.level, repr(self.modifier),
                    self.electricity, repr(self.requirements)))

    def __str__(self):
        return ("{}: level: {}\n  - electricity: {}\n  - modifier: {}\n"
                "  - requirements: {})".format(
                    self.__class__.__name__, self.level, self.electricity,
                    repr(self.modifier),
                    str(self.requirements).replace('\n', '\n' + ' ' * 8)))

    def __eq__(self, other):
        return (self.modifier == other.modifier and
                self.level == other.level and
                self.electricity == other.electricity)

    def __ne__(self, other):
        return not self.__eq__(other)

    def _compare(self, other):
        """Calculate an evenly weighted average of the atributes."""
        mod = self.modifier.trade_value - other.modifier.trade_value
        lev = self.level - other.level
        elec = self.electricity - other.electricity
        avg = (lev + elec + mod) / 3.0
        return avg

    def __lt__(self, other):
        return self._compare(other) < 0

    def __gt__(self, other):
        return self._compare(other) > 0

    def __le__(self, other):
        return self._compare(other) <= 0

    def __ge__(self, other):
        return self._compare(other) >= 0

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

    def __init__(self, level=None, sun_cb=None):
        super().__init__(level, sun_cb)
        self._modifier = Resources(ore=2*self.level,
                                   metal=0.25*self.level)
        self._electricity = -1 * pow(self.level, 2)
        self._requirements = BuildingRequirements(
            resources=Resources(ore=10+(2*(-1+self.level)),
                                metal=-10+(5*(1+self.level))))


class SolarPowerPlant(Building):
    name = 'Solar Power Plant'
    abbr = 'SPP'

    def __init__(self, level=None, sun_cb=None):
        super().__init__(level, sun_cb)
        self._modifier = Resources()
        if self.sun_cb:
            self._electricity = 10 * abs(log10(self.sun_cb())) * self.level
        self._requirements = BuildingRequirements(
            resources=Resources(ore=10+(5*self.level),
                                metal=50+(6*self.level)))


ALL_BUILDINGS = [Mine, SolarPowerPlant]


def get_all_building_names():
    return [cls.name for cls in ALL_BUILDINGS]


def get_all_building_abbr():
    return [cls.abbr for cls in ALL_BUILDINGS]


def get_building(building_name, level=None):
    if isinstance(building_name, type):
        building_name = building_name.__name__
    debug('getting building type %s, lvl %s' % (building_name, level))
    for building in ALL_BUILDINGS:
        if (building.__name__.lower() == building_name.lower() or
                building.name.lower() == building_name.lower() or
                building.abbr.lower() == building_name.lower()):
            if level is None:
                return building
            else:
                return building(level)
    else:
        raise ObjectNotFound(name=building_name)
