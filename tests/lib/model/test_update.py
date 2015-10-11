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

from unittest.mock import patch, Mock

from tests.base import SpaceTest

from lib import model
from lib.model import update


class TestUpdate(SpaceTest):
    @patch('time.time')
    def test_calculate_update_increments(self, mock_time):
        last_update = 0
        mock_time.return_value = 1
        self.assertEqual(1, update.calculate_update_increments(last_update))
        self.assertEqual(3, update.calculate_update_increments(last_update,
                                                               new_time=3))

    def test_update_trigger_decorator(self):
        # cannot use update.update_trigger because within the test_class scope
        # the "update" portion resolves to the test_class method rather than
        # the module.
        decorator = update.update_trigger

        class test_class(object):
            def __init__(self):
                self.update_called = False
                self.func_called = False

            def update(self):
                self.update_called = True

            @decorator
            def func(self, *args):
                self.func_called = True
                self.func_args = args

        test_obj = test_class()
        args = (1, 2, 'foo', 5)
        test_obj.func(*args)

        self.assertTrue(test_obj.func_called)
        self.assertTrue(test_obj.update_called)
        self.assertEqual(test_obj.func_args, args)

    def test_delayed_event_trigger_decorator(self):

        def do_delayed_actions():
            do_delayed_actions.called = True

        @update.delayed_event_trigger
        def test_method(*args):
            test_method.args = args

        update.delayed_event_trigger.CALLABLE = do_delayed_actions
        args = (9, 'bar', 4)
        test_method(*args)
        self.assertTrue(getattr(do_delayed_actions, 'called', False))
        self.assertEqual(getattr(test_method, 'args', tuple()), args)


class TestResourceUpdater(SpaceTest):
    def setUp(self):
        self.time_patch = patch('time.time')
        self.resources = model.Resources()
        self.rates = model.Resources(ore=1)
        self.last_update = 100
        self.ru = update.ResourceUpdater(self.last_update, self.resources,
                                         self.rates)

    def tearDown(self):
        self.time_patch.stop()

    def test_update(self):
        mock_time = self.time_patch.start()
        new_time = 101
        mock_time.return_value = new_time
        self.assertIsNone(self.ru.difference)
        self.assertIsNone(self.ru.resources)
        self.assertIsNone(self.ru.new_time)
        self.ru.update()
        self.assertIsNotNone(self.ru.difference)
        self.assertIsNotNone(self.ru.resources)
        self.assertIsNotNone(self.ru.new_time)
        self.assertEqual(self.ru.resources.ore,
                         (new_time - self.last_update) * self.rates.ore)

    def test_max_resources(self):
        mock_time = self.time_patch.start()
        new_time = 110
        mock_time.return_value = new_time
        max_resources = model.Resources(ore=5)
        self.ru.max_resources = max_resources
        self.ru.update()
        # check the validity of this test
        self.assertGreater((new_time - self.last_update) * self.rates.ore,
                           max_resources.ore)
        self.assertEqual(self.ru.resources.ore, max_resources.ore)
