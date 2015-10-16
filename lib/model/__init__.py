# Copyright 2015 Curtis Sand
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Space Object Model"""

# order imports by least dependent to most dependent

from .coord import Coord, SystemCoord
from .resources import (Resources, ALL_RESOURCES, ORE, METAL, THORIUM,
                        HYDROCARBON, DEUTERIUM, SUN, ELECTRICITY, TRADE_RATIO,
                        NotSufficientResourcesError)
from .building import (Mine, SolarPowerPlant, ALL_BUILDINGS, get_building,
                       get_all_building_names, get_all_building_abbr)
from .planet import Planet
from .system import System
from .galaxy import Galaxy
from .user import User
from .query import ModelQueryMixin


__all__ = [Coord, SystemCoord, ]

__all__.extend([Resources, ALL_RESOURCES, ORE, METAL, THORIUM,
                HYDROCARBON, DEUTERIUM, SUN, ELECTRICITY,
                TRADE_RATIO, NotSufficientResourcesError])

__all__.extend([Mine, SolarPowerPlant, ALL_BUILDINGS, get_building,
                get_all_building_names, get_all_building_abbr])

__all__.append(Planet)
__all__.append(System)
__all__.append(Galaxy)
__all__.append(User)
__all__.append(ModelQueryMixin)
