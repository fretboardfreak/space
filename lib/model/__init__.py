"""Space Object Model"""

from .coord import Coord, SystemCoord
__all__ = ['Coord', 'SystemCoord', ]


from .resources import (Resources, ALL_RESOURCES, ORE, METAL, THORIUM,
                        HYDROCARBON, DEUTERIUM, SUN, ELECTRICITY, TRADE_RATIO)
__all__.extend(['Resources', 'ALL_RESOURCES', 'ORE', 'METAL', 'THORIUM',
                'HYDROCARBON', 'DEUTERIUM', 'SUN', 'ELECTRICITY',
                'TRADE_RATIO'])
