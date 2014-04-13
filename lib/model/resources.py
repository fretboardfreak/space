from math import ceil, floor
from copy import deepcopy

from lib.util import AttrDict

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
TRADE_MODIFIER = AttrDict([
    (ORE, 1.0),
    (METAL, 2.0),
    (THORIUM, 4.0),
    (HYDROCARBON, 3.0),
    (DEUTERIUM, 5.0),
    ])

class Resources(AttrDict):
    def __init__(self, *args, **kwargs):
        for res, amt in kwargs.iteritems():
            if res not in ALL_RESOURCES:
                raise KeyError('Resources must be one of %s' % ALL_RESOURCES)
            kwargs[res] = float(amt)
        super(Resources, self).__init__(*args, **kwargs)
        for res in set(ALL_RESOURCES).difference(set(kwargs.keys())):
            self.setdefault(res, 0)

        # force print of sun and electricity even if val is 0
        self.force_print_all = kwargs.get('force_print_all', False)

    def __repr__(self):
        res_list = deepcopy(ALL_RESOURCES)
        if not self.force_print_all:
            if self.sun == 0:
                res_list.remove(SUN)
            if self.electricity == 0:
                res_list.remove(ELECTRICITY)
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

class ResourceError(Exception):
    pass
