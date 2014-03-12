#!/usr/bin/env python
"""
A space game where the player manages a space fairing civilization and
battles various challenges in growing their empire.
"""
# requires python 2.7

import sys, os, argparse, pickle

STATE = None


def load(save_file):
    '''Load game state directly. Useful when used on the interpreter'''
    global STATE
    STATE = pickle.load(save_file)

def main():
    args = parse_cmd_line()
    load_save_or_start_new_game(args.save)

    print STATE

    return 0

def parse_cmd_line():
    epilog = 'Stay awesome, spacelings!'
    parser = argparse.ArgumentParser(description=__doc__,
                                     epilog=epilog)
    parser.add_argument('-s', '--save-file', default='space.sav', dest='save',
                        help='The persistant game save file.')
    return parser.parse_args()

def load_save_or_start_new_game(save_file):
    if os.path.exists(save_file):
        global STATE
        with open(save_file, 'r') as sf:
            STATE = pickle.load(sf)
    else:
        start_new_game(save_file)

def start_new_game(save_file):
    msg = 'Do you want to start a new game?'
    user_input_bool(msg) or sys.exit(0)
    global STATE
    STATE = GameState(save_file)
    save()

def user_input_bool(msg):
    msg = str(msg) + ' (y|n) '
    for attempt in range(3):
        x = raw_input(msg).strip().lower()
        if x.startswith('y'):
            return True
        elif x.startswith('n'):
            break
        if attempt == 1:
            print "(>'-')>"
    print "<('-'<)"
    return False

def user_input_text(msg):
    msg = str(msg) + ' '
    while True:
        name = raw_input(msg)
        if name.isalpha():
            return name

def save():
    with open(STATE.save_file, 'w') as fd:
        pickle.dump(STATE, fd)

class GameState:
    def __init__(self, save_file):
        self.save_file = save_file
        self.user = User()
        self.galaxy = Galaxy()

    def __str__(self):
        return ("Game State[save_file=%s,%s,%s]" %
                (self.save_file, self.user, self.galaxy))

class User:
    def __init__(self, name=None):
        msg = 'what do you want your username to be? '
        self.name = user_input_text(msg)
        self.planets = {}

    def __str__(self):
        return ("User[name=%s, planets=%s]" %
                (self.name, str(self.planets)))

class SectorGrid:
    def __init__(self):
        self.x = {}
        self.y = {}

    def __str__(self):
        return "SectorGrid[%s, %s]" % (self.x, self.y)

class Galaxy:
    def __init__(self):
       self.sector_grid = SectorGrid()

    def __str__(self):
        return "Galaxy[%s]" % self.sector_grid

if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        pass
