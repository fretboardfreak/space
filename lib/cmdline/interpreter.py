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

import sys
from cmd import Cmd
from logging import debug

from . import ui
from .commands import Quit, Debug, List


class SpaceCmdInterpreter(Cmd, Quit, Debug, List):
    def __init__(self, engine, debug=None):
        super(SpaceCmdInterpreter, self).__init__()
        self.engine = engine
        self.prompt = 'space> '
        self.doc_header = 'Space Commands'
        self.undoc_header = 'Alias Commands'
        self.debug = False if debug is None else debug

    def start(self):
        try:
            try:
                debug('Trying to load the saved game...')
                self.engine.load()
            except FileNotFoundError:
                debug('No save game, starting new game...')
                self.start_new_game()
            debug('Starting interpreter...')
            self.cmdloop()
        except (KeyboardInterrupt, SystemExit):
            debug('Recieved Interrupt.')
        except Exception:
            debug('Received Unknown Exception, exiting...',
                  exc_info=True, stack_info=True)
            self.debug_post_mortem()
        finally:
            try:
                self.engine.save()
            except:
                self.debug_post_mortem()

    def start_new_game(self):
        if self.debug and ui.input_bool('Create test game state?'):
            self.engine.new_game(self.engine.mock_new_game_info_cb)
            return
        msg = 'Do you want to start a new game?'
        ui.input_bool(msg) or sys.exit(0)
        debug('Creating a new game')
        self.engine.new_game(ui.get_new_game_info)

    def debug_post_mortem(self):
        if self.debug:
            import pdb
            pdb.post_mortem()
