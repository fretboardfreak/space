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

import time

from .resources import Resources


def calculate_update_increments(last_update, new_time=None):
    """Determine the number of updated increments between last_update and now.
    """
    if not new_time:
        new_t = time.time()
    else:
        new_t = new_time
    return new_t - last_update


class ResourceUpdater(object):

    """Helper class to handle updating resources based on income.

    Attributes "new_time", "difference", "resources" will be unset until the
    update() method is called.
    """

    def __init__(self, last_update, resources, rates, max_resources=None):
        self.last_update = last_update
        self.original_resources = resources
        self.rates = rates
        self.max_resources = max_resources
        self.new_time, self.difference, self.resources = [None, None, None]

    def update(self):
        self.new_time = time.time()
        increments = calculate_update_increments(self.last_update,
                                                 new_time=self.new_time)
        self.difference = Resources()
        self.resources = self.original_resources.copy()
        for res in self.original_resources:
            self.difference[res] = self.rates[res] * increments
            if self.max_resources:
                new_val = min(self.resources[res] + self.difference[res],
                              self.max_resources[res])
            else:
                new_val = self.resources[res] + self.difference[res]
            self.resources[res] = new_val
        return self.resources, self.new_time
