from time import time
from math import pi
from logging import debug

from lib.util import AttrDict
from lib.namegen import NameGen
from lib.rst import indent
from resources import Resources
from building import ALL_BUILDINGS, get_building

class Planet(object):
    #TODO: make max_resources a range per planet instance
    max_resources = Resources(ore=15e6, metal=10e6, thorium=1e6,
                              hydrocarbon=4e5, deuterium=2e5)

    def __init__(self, sun_brightness=None, sun_distance=None):
        self.name = self.__get_new_name()
        self.emperor = None
        self.resources = Resources()
        self.last_update = time()
        self.sun_brightness = sun_brightness
        self.sun_distance = sun_distance

        # keys will be the building classname
        self.buildings = AttrDict()
        debug('Constructing new Planet: sun_dist=%s, sun_brightness=%s,'
              'resources=%s' % (self.sun_distance, self.sun_brightness,
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
        for bld in self.buildings.itervalues():
            rates += bld.modifier
        return rates

    def update(self):
        new_t = time()
        num_secs = new_t - self.last_update
        debug('Updating planet %s by %s' % (self.name, num_secs))
        for res, val in self.rates:
            difference = val * num_secs
            self.resources[res] = min(self.resources[res] + difference,
                                      self.max_resources[res])
        self.last_update = new_t

    def _build_building(self, building, level=None):
        self.update()
        building = get_building(building)
        if building.are_requirements_met(self, level):
            debug('Constructing %s level %s on planet %s' %
                  (building, level, self.name))
            new_blding = building(level)
            self.resources -= new_blding.requirements.resources
            #self.modify_rate(reason=str((type(building).__name__, level)),
            #                 modifier=new_blding.modifier)
            self.buildings[building] = new_blding
            return True
        else:
            debug('Construction attempt failed on planet %s, not enough'
                  'resources.' % self.name)
            return False

    def build(self, building):
        existing = self.buildings.get(building, None)
        level = 1 if not existing else existing.level + 1
        return self._build_building(building, level)

    def get_available_buildings(self):
        debug('Retrieving buildings available for construction on planet '
              '%s' % self.name)
        avail = []
        for building in ALL_BUILDINGS:
            existing = self.buildings.get(building, None)
            level = 1 if not existing else existing.level + 1
            if building.are_requirements_met(self, level):
                avail.append((building, level))
        return avail

    def __get_new_name(self):
        return NameGen().gen_word()

    def __repr__(self):
        return ("%s(name=%s, emperor=%s, sun_dist=%s, sun_brightness=%s, "
                "buildings=%s, electricity=%s, resources=%s, rates=%s)" %
                (self.__class__.__name__, self.name, self.emperor,
                 self.sun_distance, self.sun_brightness, self.buildings,
                 self.electricity, self.resources, self.rates))

    def show(self, verbose=None, rates=None):
        if rates is None:
            rates = True
        details = []
        self.update()
        if verbose:
            rates = True
            sun = ('Sun: dist: %s  brightness: %s' %
                   (self.sun_distance, self.sun_brightness))
            details.append(sun)
        if rates:
            res = '\n'.join(['- %s: %d (%s)' % (name, amt, self.rates[name])
                             for name, amt in self.resources])
        else:
            res = indent(str(self.resources), '- ')
        details.append(indent(res, '  '))

        bldngs = '\n'.join(['- %s' % str(bld)
                            for bld in self.buildings.itervalues()])
        details.append(bldngs)
        return ("%s, owner %s\n%s" %
                (self.name, self.emperor, '\n'.join(details)))

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
        if not self.sun_data_cb: return 0
        sun_brightness, sun_distance = self.sun_data_cb()
        return 1 + (sun_brightness / (4 * pi * pow(sun_distance, 2)))

    @property
    def electricity(self):
        return sum([bld.electricity for bld in self.buildings.itervalues()])

    @property
    def research(self):
        return AttrDict()
