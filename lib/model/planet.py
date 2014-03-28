import random
from time import time

from resources import THORIUM, METAL

from lib.namegen import NameGen
from lib.rst import indent
from lib.util import AttrDict
from resources import (update, ORE, METAL, THORIUM,
                       HYDROCARBON, DEUTERIUM, SUN,
                       ELECTRICITY, ALL_RESOURCES)

class Planet(object):
    #TODO: make max_resources a range per planet instance
    max_resources = AttrDict([(ORE, 15e6), (THORIUM, 1e6), (METAL, 10e6)],
                              (HYDROCARBON, 4e5), (DEUTERIUM, 2e5),
                              (SUN, None), (ELECTRICITY, None))

    def __init__(self):
        self.__resource_rates = []
        self.resources = AttrDict(
                [(res, random.randint(0, max_resources[res]))
                 for res in ALL_RESOURCES])

        self.name = self.__get_new_name()
        self.emperor = None
        self.last_update = time()
        self.buildings = []

    @property
    def ore(self):
        return self.resources[ORE]

    @property
    def thorium(self):
        return self.resources[THORIUM]

    @property
    def metal(self):
        return self.resources[METAL]

    @property
    def hydrocarbon(self):
        return self.resources[HYDROCARBON]

    @property
    def deuterium(self):
        return self.resources[DEUTERIUM]

    @property
    def sun(self):
        pass

    @property
    def electricity(self):
        pass

    @property
    def rates(self):
        rates = AttrDict(zip(ALL_RESOURCES,
                         [float()] * len(ALL_RESOURCES)))
        for res, modifier in self.__resource_rates:
            rates[res] = rates.get(res, float()) + modifier
        return rates

    def _modify_rate(self, resource, modifier):
        if resource not in ALL_RESOURCES:
            raise KeyError('Resource %s not found on planet %s.' %
                           (resource, self.name))
        self.__resource_rates.append((resource, float(modifier)))

    def update(self):
        new_t = time()
        num_secs = new_t - self.last_update
        update_resources(self.resources, self.rates, num_secs,
                         __cls__.max_resources)
        self.last_update = new_t

    def build_building(self, building_type):


    def __get_new_name(self, lang_file=None):
        if not lang_file:
            lang_file = 'lib/namegen_lang.txt'
        return NameGen(lang_file).gen_word()

    def __repr__(self):
        return ("Planet(name=%s, emperor=%s, resources=%s, rates=%s)" %
                (self.name, self.emperor, self.resources, self.rates))

    def show(self, rates=None):
        if rates is None:
            rates = True
        self.update()
        res = '\n'.join(['- %s: %d (%s)' % (name, amt, self.rates[name])
                         for name, amt in self.resources.iteritems()])
        res = indent(res, '  ')
        return "%s, owner %s\n%s" % (self.name, self.emperor, res)
