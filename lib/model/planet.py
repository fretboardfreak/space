from time import time

from lib.util import AttrDict
from lib.namegen import NameGen
from lib.rst import indent
from resources import Resources
from building import ALL_BUILDINGS

class Planet(object):
    #TODO: make max_resources a range per planet instance
    max_resources = Resources(ore=15e6, metal=10e6, thorium=1e6,
                              hydrocarbon=4e5, deuterium=2e5)

    def __init__(self):
        self.rate_modifiers = []
        self.resources = Resources()
        self.name = self.__get_new_name()
        self.emperor = None
        self.last_update = time()

        # keys will be the building classname
        self.buildings = AttrDict()

    @property
    def rates(self):
        rates = Resources()
        for reason, modifier in self.rate_modifiers:
            rates += modifier
        return rates

    def modify_rate(self, reason, modifier):
        self.rate_modifiers.append((reason, modifier))

    def update(self):
        new_t = time()
        num_secs = new_t - self.last_update
        for res, val in self.rates:
            difference = val * num_secs
            self.resources[res] = min(self.resources[res] + difference,
                                      self.max_resources[res])
        self.last_update = new_t

    def _build_building(self, building, level=None):
        self.update()
        if building.are_requirements_met(self, level):
            new_blding = building(level)
            self.resources -= new_blding.requirements.resources
            self.modify_rate(reason=str((type(building).__name__, level)),
                             modifier=new_blding.modifier)
            self.buildings[building] = new_blding
            return True
        else:
            return False

    def build(self, building):
        existing = self.buildings.get(building, None)
        level = None if not existing else existing.level + 1
        return self._build_building(building, level)

    def get_available_buildings(self):
        avail = []
        for building in ALL_BUILDINGS:
            existing = self.buildings.get(building, None)
            level = None if not existing else existing.level + 1
            if building.are_requirements_met(self, level):
                avail.append((building, level))
        return avail

    def __get_new_name(self, lang_file=None):
        if not lang_file:
            lang_file = 'lib/namegen_lang.txt'
        return NameGen(lang_file).gen_word()

    def __repr__(self):
        return ("%s(name=%s, emperor=%s, buildings=%s, resources=%s, "
                "rates=%s)" % (self.__class__.__name__, self.name,
                self.emperor, self.buildings, self.resources, self.rates))

    def show(self, rates=None):
        if rates is None:
            rates = True
        else:
            rates = rates
        self.update()
        if rates:
            res = '\n'.join(['- %s: %d (%s)' % (name, amt, self.rates[name])
                             for name, amt in self.resources])
        else:
            res = indent(self.resources, '- ')
        res = indent(res, '  ')
        bldngs = '\n'.join(['- %s' % str(bld) for bld in self.buildings])
        return ("%s, owner %s\n%s\n%s" %
                (self.name, self.emperor, bldngs, res))

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
        pass

    @property
    def electricity(self):
        return self.rates.electricity
