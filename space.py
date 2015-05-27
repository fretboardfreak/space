#!/usr/bin/env python3

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

"""
A space game where the player manages a space fairing civilization and
battles various challenges in growing their empire.
"""
# requires python 3

import sys
import logging
from argparse import ArgumentParser

from lib.engine import SpaceEngine
from lib.cmdline.interpreter import SpaceCmdInterpreter


def main():
    args = parse_args()
    logging.basicConfig(
        filename=args.log_file, level=logging.DEBUG, filemode='a',
        format='%(levelname)s [%(module)s|%(funcName)s] %(message)s')
    print('logging to %s started' % args.log_file)
    logging.debug('logging to %s started' % args.log_file)
    engine = SpaceEngine(args.save_file)
    SpaceCmdInterpreter(engine, args.debug).start()


def parse_args():
    epilog = 'Stay awesome, spacelings!'
    parser = ArgumentParser(description=__doc__,
                            epilog=epilog)
    parser.add_argument(
        '-s', '--save-file', default='save.space', dest='save_file',
        help='The persistant game save file.')
    parser.add_argument(
        '-l', '--log-file', default='runlog', dest='log_file',
        help='The filename to store game logs.')
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False, dest='debug',
        help='Enable debugging features.')
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
