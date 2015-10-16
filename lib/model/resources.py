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


class NotSufficientResourcesError(ArithmeticError):
    """Thrown when an operation results in less than zero of some resource."""
    def __init__(self, defecit, *args, **kwargs):
        self.defecit = defecit


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

    @property
    def trade_value(self):
        value = 0
        for res in ALL_RESOURCES:
            value += float(TRADE_RATIO[res]) * self[res]
        return value

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
        return '({}, trade value: {:.2F})'.format(
            ', '.join("{res}: {amt:.2F}".format(res=res, amt=self[res])
                      for res in res_list),
            self.trade_value)

    def __str__(self):
        s = self.__repr__().replace('(', '').replace(')', '')
        s = s.replace(', ', '\n')
        return s

    def __eq__(self, other):
        return self.trade_value == other.trade_value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.trade_value < other.trade_value

    def __ge__(self, other):
        '''De Morgan's law'''
        return not self.__lt__(other)

    def __gt__(self, other):
        return self.trade_value > other.trade_value

    def __le__(self, other):
        '''De Morgan's law'''
        return not self.__gt__(other)

    def __add__(self, other):
        result = Resources()
        for res in ALL_RESOURCES:
            result[res] = self[res] + other[res]
        return result

    def __sub__(self, other):
        """Attempt to subtract the value of other from self.

        If the subtraction operation results in a negative value the
        NotSufficientResourcesError exception will be thrown. The
        NotSufficientResourcesError exception will include a "defecit"
        attribute which will be a Resources object with the values of resources
        that were missing for this subtraction operation.
        """
        result = Resources()
        nsr = {}
        for res in ALL_RESOURCES:
            temp = self[res] - other[res]
            if temp < 0:
                nsr[res] = abs(temp)
                continue
            result[res] = temp
        if nsr:
            raise NotSufficientResourcesError(defecit=Resources(**nsr))
        return result

    def copy(self):
        copy = self.__class__()
        for attr in self:
            copy[attr] = self[attr]
        return copy

    def __getstate__(self):
        return (dict((res, self[res]) for res in ALL_RESOURCES), )

    def __setstate__(self, state):
        res_dict = state[0]
        for res in res_dict:
            self[res] = res_dict[res]


# Add properties to the Resources class for each resource in ALL_RESOURCES
for res in ALL_RESOURCES:

    def getter(resource, self):
        return self[resource]

    def setter(resource, self, value):
        self.__setitem__(resource, value)

    setattr(Resources, res, property(fget=partial(getter, res),
                                     fset=partial(setter, res)))
