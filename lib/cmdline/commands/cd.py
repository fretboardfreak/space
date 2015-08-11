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

from argparse import ArgumentParser

from .base import CommandMixin


class Cd(CommandMixin):
    """Change the focussed object."""
    def __change_focussed(self, opts):
        if not opts.object:
            print("No object ID: Showing available objects:\n")
            self.do_list("-a")
            return
        for obj_id, obj in self.engine.get_object_id_map().items():
            if obj_id.startswith(opts.object):
                print('Setting current object to %s' % obj[1].name)
                self.current_object = obj
                return
        else:
            print('Failed to find object {}'.format(opts.object))

    def __setup_parser(self):
        parser = ArgumentParser(prog='cd', description=Cd.__doc__)
        parser.add_argument(dest='object')
        parser.set_defaults(action=self.__change_focussed)
        return parser, self.__change_focussed

    def do_cd(self, line):
        super(Cd, self)._do(line, self.__setup_parser)

    def help_cd(self):
        print(Cd.__doc__)
