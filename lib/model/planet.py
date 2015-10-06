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

from lib.error import ModelObjectError
from lib.namegen import NameGen

from .update import ResourceUpdater, delayed_event_trigger
from .resources import Resources
from .building import ALL_BUILDINGS, get_building


class Planet(object):

    # TODO: make max_resources a range per planet instance
    max_resources = Resources(ore=15e6, metal=10e6, thorium=1e6,
                              hydrocarbon=4e5, deuterium=2e5)

    def __init__(self, name=None, emperor=None, sun_brightness=None,
                 sun_distance=None, resources=None, buildings=None,
                 last_update=None):
        self.name = name
        if self.name is None:
            self.name = NameGen().gen_word(no_repeat=True)

        self.emperor = emperor

        self.resources = resources
        if self.resources is None:
            self.resources = Resources()
        elif not isinstance(self.resources, Resources):
            # state tuple not object
            tmp = Resources()
            tmp.__setstate__(self.resources)
            self.resources = tmp

        self.sun_brightness = sun_brightness
        if sun_distance is not None and sun_distance <= 0:
            raise ModelObjectError(
                'Planet: Sun Distance must be greater than 0.')
        self.sun_distance = sun_distance

        self.buildings = buildings
        if self.buildings is None:
            self.buildings = []
        elif (len(self.buildings) > 0 and
              not isinstance(self.buildings[0], tuple(ALL_BUILDINGS))):
            self.load_buildings(self.buildings)

        self.last_update = last_update
        if self.last_update is None:
            self.last_update = time()

        debug('Planet object initialized: name={}, sun_dist={}, '
              ' sun_brightness={}, resources={}'.format(
                  self.name, self.sun_distance, self.sun_brightness,
                  repr(self.resources)))

    def __getstate__(self):
        resources = self.resources.__getstate__()
        buildings = [(blding.abbr, blding.level)
                     for blding in self.buildings]
        return (self.name, self.emperor, self.sun_brightness,
                self.sun_distance, resources, buildings, self.last_update)

    def __setstate__(self, state):
        (self.name, self.emperor, self.sun_brightness,
         self.sun_distance, resources, buildings, self.last_update) = state
        self.resources = Resources().__setstate__(resources)
        self.load_buildings(buildings)

    def load_buildings(self, buildings):
        self.buildings = []
        for bld, level in buildings:
            self.buildings.append(get_building(bld)(level))

    @property
    def rates(self):
        rates = Resources()
        for bld in self.buildings:
            rates += bld.modifier
        return rates

    @delayed_event_trigger
    def update(self):
        updater = ResourceUpdater(self.last_update, self.resources,
                                  self.rates, self.max_resources)
        self.resources, self.last_update = updater.update()
        debug('Updated planet {} by {}'.format(self.name, updater.difference))

    def _build_building(self, building_name, level=None):
        self.update()
        building = get_building(building_name)
        if building.are_requirements_met(self, level):
            debug('Constructing {} level {} on planet {}'.format(
                building, level, self.name))
            new_blding = building(level)
            self.resources -= new_blding.requirements.resources
            # Remove existing building if exists
            self.buildings = [blding for blding in self.buildings
                              if not isinstance(blding, building)]
            self.buildings.append(new_blding)
            return True
        else:
            debug('Construction attempt failed on planet {}, not enough'
                  'resources.'.format(self.name))
            return False

    def build(self, building):
        existing = self.building(building)
        level = 1 if not existing else existing.level + 1
        return self._build_building(building, level)

    def get_available_buildings(self):
        debug('Retrieving buildings available for construction on planet '
              '{}'.format(self.name))
        avail = []
        for building in ALL_BUILDINGS:
            existing = self.building(building)
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
        resources = ['  {}: {:.2F} ({:.2F})\n'.format(name,
                                                      self.resources[name],
                                                      self.rates[name])
                     for name in self.resources]
        buildings = ['  {}\n'.format(bld) for bld in self.buildings]
        buildings = ''.join([text for text in buildings
                             if not text.isspace()])
        if not self.research:
            research = ""
        return ("{}: {}, Emperor: {},\nSun: {:.2F}, Electricity: {:.2F}\n"
                "Resources:\n{}Buildings:\n{}Research: {}".format(
                    self.__class__.__name__, self.name, self.emperor, self.sun,
                    self.electricity, ''.join(resources),
                    buildings, research))

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
        return sum(bld.electricity(self.sun) for bld in self.buildings)

    @property
    def research(self):
        return dict()

    # trigger delayed events to ensure any building construction is completed
    # the rest of the update process is not needed when looking at just a
    # building though.
    @delayed_event_trigger
    def building(self, building_type):
        bld_cls = get_building(building_type)
        for building in self.buildings:
            if isinstance(building, bld_cls):
                debug('found existing {} building'.format(building))
                return building
