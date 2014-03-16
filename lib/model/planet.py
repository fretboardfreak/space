import random
from time import time

from lib.namegen import NameGen
from lib.rst import indent
from lib.util import AttrDict

# resources
METAL = 'metal'
THORIUM = 'thorium'

class Planet(object):
    def __init__(self):
        self.__resource_names = [THORIUM, METAL]
        self.__max_resources = AttrDict([(THORIUM, 1e6),
                                        (METAL, 10e6)])
        self.__resource_rates = []
        self.resources = AttrDict(
                [(res, random.randint(0, self.__max_resources[res]))
                 for res in self.__resource_names])

        self.name = self.__get_new_name()
        self.emperor = None
        self.__last_update = time()

    @property
    def thorium(self):
        return self.resources[THORIUM]

    @property
    def metal(self):
        return self.resources[METAL]

    @property
    def rates(self):
        rates = AttrDict(zip(self.__resource_names,
                         [float()] * len(self.__resource_names)))
        for res, modifier in self.__resource_rates:
            rates[res] = rates.get(res, float()) + modifier
        return rates

    def __modify_rate(self, resource, modifier):
        if resource not in self.__resource_names:
            raise KeyError('Resource %s not found on planet %s.' %
                           (resource, self.name))
        self.__resource_rates.append((resource, float(modifier)))

    def update(self):
        """ update things that change over time on planets

            Resources: When something is constructed that modifies the income
                rate of a resource, a rate modifier is added to
                self.__resource_rates of the form (resource, float) where the
                float is the per second rate modifier.  All the rate modifiers
                for each resource type are accumulated together before the
                update amount is calculated.
        """
        no_secs = time() - self.__last_update
        for res in self.__resource_names:
            update = no_secs * self.rates[res]
            new_val = self.resources[res] + update
            if new_val > self.__max_resources[res]:
                new_val = self.__max_resources[res]
            self.resources[res] = new_val
        self.__last_update = time()

    def __get_new_name(self, lang_file=None):
        if not lang_file:
            lang_file = 'lib/namegen_lang.txt'
        return NameGen(lang_file).gen_word()

    def __repr__(self):
        return ("Planet(name=%s, emperor=%s, resources=%s, rates=%s)" %
                (self.name, self.emperor, self.resources, self.rates))

    def show(self):
        self.update()
        res = '\n'.join(['- %s: %d' % (name, amt)
                         for name, amt in self.resources.iteritems()])
        res = indent(res, '  ')
        return "%s, owner %s\n%s" % (self.name, self.emperor, res)
