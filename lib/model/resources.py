from copy import deepcopy
from logging import debug
from functools import partial
from collections import UserDict

ORE = 'ore'
METAL = 'metal'
THORIUM = 'thorium'
HYDROCARBON = 'hydrocarbon'
DEUTERIUM = 'deuterium'
SUN = 'sun'
ELECTRICITY = 'electricity'

ALL_RESOURCES = [ORE, METAL, THORIUM, HYDROCARBON,
                 DEUTERIUM]

TRADE_RATIO = {ORE: 1.0, METAL: 2.0, THORIUM: 4.0, HYDROCARBON: 3.0,
               DEUTERIUM: 5.0, }


class Resources(UserDict):
    def __init__(self, *args, **kwargs):
        items = dict(zip(ALL_RESOURCES, [0] * len(ALL_RESOURCES)))
        for res in kwargs:
            if res not in ALL_RESOURCES:
                msg = ('Resource %s is invalid. Resources must be one of %s'
                       % (res, ALL_RESOURCES))
                debug(msg)
                raise KeyError(msg)
            items[res] = float(kwargs[res])
        super(Resources, self).__init__(items)

    def __getattribute__(self, item):
        val = None
        try:
            val = super(Resources, self).__getattribute__(item)
        except AttributeError:
            val = self[item]
        if item in ALL_RESOURCES:
            if val < 0:
                val = abs(val)
                self.__setattr__(item, val)
        return val

    def __getitem__(self, item):
        val = super(Resources, self).__getitem__(item)
        if item in ALL_RESOURCES:
            if val < 0:
                val = abs(val)
                self.__setitem__(item, val)
        return val

    def __repr__(self):
        res_list = deepcopy(ALL_RESOURCES)
        return '(%s)' % ', '.join(["%s: %s" % (res, self[res])
                                   for res in res_list])

    def __str__(self):
        s = self.__repr__().replace('(', '').replace(')', '')
        s = s.replace(', ', '\n')
        return s

    def _tally_value_difference(self, other):
        '''Use the trade ratio to tally the relative values of each resource'''
        tally = 0
        for res in ALL_RESOURCES:
            diff = float(self[res]) - float(other[res])
            tally += float(TRADE_RATIO[res]) * diff
        return tally

    def __eq__(self, other):
        return self._tally_value_difference(other) == 0

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self._tally_value_difference(other) < 0

    def __ge__(self, other):
        '''De Morgan's law'''
        return not self.__lt__(other)

    def __gt__(self, other):
        return self._tally_value_difference(other) > 0

    def __le__(self, other):
        '''De Morgan's law'''
        return not self.__gt__(other)

    def __add__(self, other):
        result = Resources()
        for res in ALL_RESOURCES:
            result[res] = self[res] + other[res]
        return result

    def __sub__(self, other):
        result = Resources()
        for res in ALL_RESOURCES:
            result[res] = self[res] - other[res]
        return result

# Add properties to the Resources class for each resource in ALL_RESOURCES
for res in ALL_RESOURCES:

    def getter(resource, self):
        return self[resource]

    def setter(resource, self, value):
        self.__setitem__(resource, value)

    setattr(Resources, res, property(fget=partial(getter, res),
                                     fset=partial(setter, res)))
