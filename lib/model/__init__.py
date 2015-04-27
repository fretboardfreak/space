"""Space Object Model"""

# order imports by least dependent to most dependent

from .coord import Coord, SystemCoord
from .resources import (Resources, ALL_RESOURCES, ORE, METAL, THORIUM,
                        HYDROCARBON, DEUTERIUM, SUN, ELECTRICITY, TRADE_RATIO)
from .building import (Mine, SolarPowerPlant, ALL_BUILDINGS, get_building,
                       get_all_building_names, get_all_building_abbr)
from .planet import Planet
from .system import System
from .galaxy import Galaxy
from .user import User


__all__ = [Coord, SystemCoord, ]

__all__.extend([Resources, ALL_RESOURCES, ORE, METAL, THORIUM,
                HYDROCARBON, DEUTERIUM, SUN, ELECTRICITY,
                TRADE_RATIO])

__all__.extend([Mine, SolarPowerPlant, ALL_BUILDINGS, get_building,
                get_all_building_names, get_all_building_abbr])

__all__.append(Planet)
__all__.append(System)
__all__.append(Galaxy)
__all__.append(User)
