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

from time import time
from math import pi
from logging import debug

from lib.namegen import NameGen
from lib.rst import indent

from .resources import Resources
from .building import ALL_BUILDINGS, get_building


class Planet(object):

    # TODO: make max_resources a range per planet instance
    max_resources = Resources(ore=15e6, metal=10e6, thorium=1e6,
                              hydrocarbon=4e5, deuterium=2e5)

    def __init__(self, sun_brightness=None, sun_distance=None):
        self.name = NameGen().gen_word()
        self.emperor = None
        self.resources = Resources()
        self.last_update = time()
        self.sun_brightness = sun_brightness
        self.sun_distance = sun_distance

        # keys will be the building classname
        self.buildings = dict()
        debug('Constructing new Planet: sun_dist={}, sun_brightness={},'
              'resources={}'.format(self.sun_distance, self.sun_brightness,
                                    self.resources))

    def __getstate__(self):
        return (self.name, self.emperor, self.resources, self.last_update,
                self.buildings, self.sun_brightness, self.sun_distance)

    def __setstate__(self, state):
        (self.name, self.emperor, self.resources, self.last_update,
         self.buildings, self.sun_brightness, self.sun_distance) = state

    @property
    def rates(self):
        rates = Resources()
        for bld in self.buildings.values():
            rates += bld.modifier
        return rates

    def update(self):
        new_t = time()
        num_secs = new_t - self.last_update
        debug('Updating planet {} by {}'.format(self.name, num_secs))
        for res in self.rates:
            difference = self.rates[res] * num_secs
            self.resources[res] = min(self.resources[res] + difference,
                                      self.max_resources[res])
        self.last_update = new_t

    def _build_building(self, building, level=None):
        self.update()
        building = get_building(building)
        if building.are_requirements_met(self, level):
            debug('Constructing {} level {} on planet {}'.format(
                building, level, self.name))
            new_blding = building(level)
            self.resources -= new_blding.requirements.resources
            self.buildings[building] = new_blding
            return True
        else:
            debug('Construction attempt failed on planet {}, not enough'
                  'resources.'.format(self.name))
            return False

    def build(self, building):
        existing = self.buildings.get(building, None)
        level = 1 if not existing else existing.level + 1
        return self._build_building(building, level)

    def get_available_buildings(self):
        debug('Retrieving buildings available for construction on planet '
              '{}'.format(self.name))
        avail = []
        for building in ALL_BUILDINGS:
            existing = self.buildings.get(building, None)
            level = 1 if not existing else existing.level + 1
            if building.are_requirements_met(self, level):
                avail.append((building, level))
        return avail

    def __repr__(self):
        return ("{}(name: {}, emperor: {}, sun: {}, buildings: {}, "
                "electricity: {}, resources: {}, rates: {}, research: {}, "
                "last update: {})".format(
                    self.__class__.__name__, self.name, self.emperor,
                    self.sun, self.buildings, self.electricity,
                    repr(self.resources), repr(self.rates), self.research,
                    self.last_update))

    def __str__(self):
        resources = ['  {}: {} ({})'.format(name, self.resources[name],
                                            self.rates[name])
                     for name in self.resources]
        buildings = ['  {}'.format(bld) for bld in self.buildings.values()]
        return ("{}: {}, Emperor: {},\nSun: {}, Electricity: {}\n"
                "Resources:\n{}\nBuildings:\n{}\nResearch: {}\n"
                "Last Update: {}".format(
                    self.__class__.__name__, self.name, self.emperor, self.sun,
                    self.electricity, '\n'.join(resources),
                    '\n'.join(buildings), self.research, self.last_update))

    def show(self, verbose=None, rates=None):
        if rates is None:
            rates = True
        details = []
        self.update()
        if verbose:
            rates = True
            sun = 'Sun: dist: {}  brightness: {}'.format(self.sun_distance,
                                                         self.sun_brightness)
            details.append(sun)
        if rates:
            res = '\n'.join(['- {}: {} ({})'.format(
                                name, self.resources[name], self.rates[name])
                             for name in self.resources])
        else:
            res = indent(str(self.resources), '- ')
        details.append(indent(res, '  '))

        bldngs = '\n'.join(['- {}'.format(str(bld))
                            for bld in self.buildings.values()])
        details.append(bldngs)
        return "Planet {}, owner {}\n{}".format(self.name, self.emperor,
                                                '\n'.join(details))

    @property
    def ore(self):
        return self.resources.ore

    @property
    def thorium(self):
        return self.resources.thorium

    @property
    def metal(self):
        return self.resources.metal

    @property
    def hydrocarbon(self):
        return self.resources.hydrocarbon

    @property
    def deuterium(self):
        return self.resources.deuterium

    @property
    def sun(self):
        """
        Sun energy is calculated by the planet so that different effects
        like polution/atmosphere blocking transmission can be implemented.
        """
        return 1 + (self.sun_brightness / (4 * pi * pow(self.sun_distance, 2)))

    @property
    def electricity(self):
        return sum([bld.electricity for bld in self.buildings.values()])

    @property
    def research(self):
        return dict()
