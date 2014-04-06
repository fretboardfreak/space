import copy

ORE = 'ore'
METAL = 'metal'
THORIUM = 'thorium'
HYDROCARBON = 'hydrocarbon'
DEUTERIUM = 'deuterium'
SUN = 'sun'
ELECTRICITY = 'electricity'

ALL_RESOURCES = [ORE, METAL, THORIUM, HYDROCARBON,
                 DEUTERIUM, SUN, ELECTRICITY]


class Resources(object):
    def __init__(self, **kwargs):
        if any([res not in ALL_RESOURCES
                for res in kwargs.keys()]):
            raise KeyError('Resources must be one of %s' % ALL_RESOURCES)
        self.__dict__ = copy.deepcopy(kwargs)
        self.__init_dict()
        for res in ALL_RESOURCES:
            self.__dict__.setdefault(res, 0)

class ResourceError(Exception):
    pass

def update(resources, rates, num_secs, maxes=None):
    for res in ALL_RESOURCES:
        update = num_secs * rates[res]
        new_val = resources[res] + update
        if maxes and new_val > maxes[res]:
            new_val = maxes[res]
        resources[res] = new_val
