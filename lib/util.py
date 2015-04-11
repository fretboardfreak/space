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

from collections import defaultdict, UserDict

class AttrDict(UserDict):
    """ Dictionary who's keys become attributes.

        Causes memory leak on python < 2.7.3 and python < 3.2.3
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

class DefaultAttrDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DefaultAttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getattribute__(self, name):
        try:
            return super(DefaultAttrDict, self).__getattribute__(name)
        except AttributeError:
            return self[name]
