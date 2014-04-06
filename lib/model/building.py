from lib.util import AttrDict

from resources import (ORE, METAL, THORIUM, HYDROCARBON,
                       DEUTERIUM, SUN, ELECTRICITY)

class Building(object):
    def __init__(self):
        self.cost = AttrDict([
            (ORE, 1), (METAL, 1), (THORIUM, 0),
            (HYDROCARBON, 0), (DEUTERIUM, 0), (SUN, 0),
            (ELECTRICITY, 1)])
        self.modifier = AttrDict([
            (ORE, 0), (METAL, 0), (THORIUM, 0),
            (HYDROCARBON, 0), (DEUTERIUM, 0), (SUN, 0),
            (ELECTRICITY, 1)])
