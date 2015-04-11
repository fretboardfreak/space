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

__all__ = ['GameState']


class GameState(object):
    def __init__(self, save_file=None):
        self.save_file = save_file
        self.user = None
        self.galaxy = None

    def __repr__(self):
        return ("GameState(save_file=%s,%s,%s)" %
                (self.save_file, self.user, self.galaxy))

    def __getstate__(self):
        return (self.save_file, self.user, self.galaxy)

    def __setstate__(self, state):
        (self.save_file, self.user, self.galaxy) = state
