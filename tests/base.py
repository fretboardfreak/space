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

import unittest


class SpaceTest(unittest.TestCase):

    """Common base class for Space tests."""

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.warnings_to_errors = False

    def shortDescription(self):
        """
        Prevent nosetests from using test docstring instead of method and
        class names.
        """
        return None
