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
import functools
from logging import debug

from .resources import Resources

# Using a global to hold the delayed events for now.
# Also, delayed events are currently executed through the delayed_event_trigger
# rather than a separate event thread.
DELAYED_EVENTS = []
# TODO:
# - make engine queries threadsafe
# - ensure that only queries are used to interact with the model
# - write a class that will run its own thread for managing
# - Move event handling from engine into the event manager class
# - remove all uses of delayed_event_trigger


def update_trigger(func):
    """Decorator to trigger an update before given method is called."""

    @functools.wraps(func)
    def new_function(*args, **kwargs):
        if len(args) > 0 and hasattr(args[0], 'update'):
            args[0].update()
        return func(*args, **kwargs)

    return new_function


def delayed_event_trigger(func):
    """Decorator to trigger delayed events before calling a method."""

    @functools.wraps(func)
    def new_function(*args, **kwargs):
        if hasattr(delayed_event_trigger, 'CALLABLE'):
            debug('Performing Delayed Actions...')
            delayed_event_trigger.CALLABLE()
        return func(*args, **kwargs)

    return new_function


def calculate_update_increments(last_update, new_time=None):
    """Determine the number of updated increments between last_update and now.
    """
    if not new_time:
        new_t = time.time()
    else:
        new_t = new_time
    return new_t - last_update


class ResourceUpdater(object):

    """Helper class to handle updating a Planet's resources based on income.

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
        """Calculate the new value of resources for planet."""
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


class DelayedEvent(object):

    """Perform an action after some delay.

    :descriptor: A string describing the event.
    :delay: A number representing the number of seconds to delay.
    :action: A callable to be executed after the delay.

    When triggered, if the period of delay has passed, the provided action
    callable will be executed.  If the event triggered it will return True
    otherwise it will return None.  When triggered the attribute "triggered"
    will change from False to True unless an exception was thrown by the action
    callable.  Once the "triggered" attribute is set to True the event cannot
    be re-triggered.

    When triggering events, the trigger time can be passed in as the keyword
    "_time" otherwise time.time() will be used.
    """

    def __init__(self, descriptor, delay, action, *args, **kwargs):
        self.descriptor = descriptor
        self.delay = delay
        self.action = action
        self.args = args
        self.kwargs = kwargs
        self.trigger_time = time.time() + delay
        self.triggered = False

    def is_delay_over(self, _time=None):
        if not _time:
            _time = time.time()
        return _time >= self.trigger_time

    def __call__(self, _time=None):
        if not self.is_delay_over(_time):
            return
        if not self.triggered:
            debug('Triggering event "{}"...'.format(self.descriptor))
            self.action(*self.args, **self.kwargs)
            self.triggered = True
        return True
