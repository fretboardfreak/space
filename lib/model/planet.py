from time import time

from lib.namegen import NameGen
from lib.rst import indent
from resources import ResourceError, Resources

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
        self.buildings = []

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
        pass

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

    def build_building(self, building):
        self.update()
        if self.resources < building.cost:
            raise ResourceError("Not enough resources.")
        self.resources -= building.cost
        self.buildings.append(building)

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
