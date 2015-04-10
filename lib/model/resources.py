from math import ceil, floor
from copy import deepcopy
from logging import debug

from lib.util import AttrDict, DefaultAttrDict

__all__ = ['Resources', 'ALL_RESOURCES', 'ORE', 'METAL', 'THORIUM',
           'HYDROCARBON', 'DEUTERIUM', 'SUN', 'ELECTRICITY']

ORE = 'ore'
METAL = 'metal'
THORIUM = 'thorium'
HYDROCARBON = 'hydrocarbon'
DEUTERIUM = 'deuterium'
SUN = 'sun'
ELECTRICITY = 'electricity'

ALL_RESOURCES = [ORE, METAL, THORIUM, HYDROCARBON,
                 DEUTERIUM]

# Trade Value: defined in terms of 1 ORE as unit value
TRADE_MODIFIER = DefaultAttrDict(lambda: 0.0,
                                 {ORE: 1.0,
                                  METAL: 2.0,
                                  THORIUM: 4.0,
                                  HYDROCARBON: 3.0,
                                  DEUTERIUM: 5.0, })

class Resources(DefaultAttrDict):
    def __init__(self, *args, **kwargs):
        for res in kwargs:
            if res not in ALL_RESOURCES:
                msg = ('Resource %s is invalid. Resources must be one of %s'
                       % (res, ALL_RESOURCES))
                debug(msg)
                raise KeyError(msg)
            kwargs[res] = float(kwargs[res])
        super(Resources, self).__init__(lambda: 0.0, *args, **kwargs)

    def __getattribute__(self, item):
        try:
            val = super(Resources, self).__getattribute__(item)
        except AttributeError:
            val = self[val]
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

    def __cmp__(self, other):
        tally = 0
        for res in ALL_RESOURCES:
            diff = float(self[res]) - float(other[res])
            tally += float(TRADE_MODIFIER[res]) * diff
        if tally > 0:
            return ceil(tally)
        else:
            return floor(tally)

    def __eq__(self, other):
        return self.__cmp__(other) == 0

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

    def __iter__(self):
        for res in ALL_RESOURCES:
            yield (res, self[res])
