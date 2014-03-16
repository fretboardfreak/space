#!/usr/bin/env python
"""
A space game where the player manages a space fairing civilization and
battles various challenges in growing their empire.
"""
# requires python 2.7

import sys, os, pickle, random, readline
from argparse import ArgumentParser
from collections import defaultdict
from cmd import Cmd
from functools import partial

from lib.namegen import NameGen
from lib.rst import indent, wrap

def main():
    args = parse_args()
    engine = SpaceEngine(args.save_file, SpaceUI)
    interpreter = SpaceCmd(engine)
    interpreter.start()

def parse_args():
    epilog = 'Stay awesome, spacelings!'
    parser = ArgumentParser(description=__doc__,
                            epilog=epilog)
    parser.add_argument('-s', '--save-file', default='space.sav', dest='save_file',
                        help='The persistant game save file.')
    return parser.parse_args()

class SpaceEngine(object):
    def __init__(self, save_file, user_interface):
        self.ui = user_interface
        self.state = GameState(save_file)

    def load(self):
        '''Load game state directly. Useful when used on the interpreter'''
        with open(self.state.save_file, 'r') as sf:
            self.state = pickle.load(sf)

    def start_new_game(self):
        msg = 'Do you want to start a new game?'
        self.ui.input_bool(msg) or sys.exit(0)

        self.state.galaxy = Galaxy()

        name = self.ui.input_text("Great another wanna be space emperor! "
                                  "What's your name then? ")

        home_coords = Coord()
        sec_x = self.ui.input_int('Ok, now we need to find your home planet. '
                                  'Enter the sector coords:\nx=')
        sec_y = self.ui.input_int('y=')
        home_coords.sector = (sec_x, sec_y)

        sys_x = self.ui.input_int('Now the system coords:\nx=')
        sys_y = self.ui.input_int('y=')
        home_coords.system = (sys_x, sys_y)

        system = self.state.galaxy.systems[home_coords]
        planet_num_qry = ('That system has %s planets. Which one did you say '
                          'was yours?\n%s\nplanet=' %
                          (len(system.planets),
                           '\n'.join([' %s. %s' % (i, p.name) for i,p in
                                      enumerate(system.planets)])))
        planet_num = self.ui.input_int(planet_num_qry, min=1,
                                       max=len(system.planets)-1)
        home_coords.planet = planet_num
        home_planet = system.planets[planet_num]

        self.state.user = User(name, home_coords, home_planet)
        self.save()

    def save(self):
        with open(self.state.save_file, 'w') as fd:
            pickle.dump(self.state, fd)

class SpaceUI(object):
    @staticmethod
    def input_bool(msg):
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

    @staticmethod
    def input_text(msg):
        while True:
            name = raw_input(msg)
            if name.isalpha():
                return name

    @staticmethod
    def input_int(msg, min=None, max=None):
        while True:
            while True:
                num = raw_input(msg)
                try:
                    num = int(num)
                    break
                except:
                    pass
            if min is not None and num < min:
                print "too small (minimum=%s)" % min
                continue
            if max is not None and num > max:
                print "too large (maximum=%s)" % max
                continue
            return num

    @staticmethod
    def dbg_print_state(engine):
        print engine.state

    @staticmethod
    def show_planets(engine, *args, **kwargs):
        print engine.state.user.show_planets()

class SpaceCmd(Cmd):
    def __init__(self, engine):
        self.engine = engine
        self.ui = self.engine.ui #convenient
        Cmd.__init__(self)
        self.prompt = 'space> '
        self.doc_header='Space Commands'
        self.undoc_header='Alias Commands'

    def start(self):
        try:
            self.engine.load()
        except IOError:
            self.engine.start_new_game()

        self.cmdloop()

    def do_show(self, line):
        show_planets = partial(self.ui.show_planets, self.engine)
        try:
            parser = ArgumentParser(prog='show',
                                    description=self.help_show(True))
            parser.add_argument('-p', '--planets', action='store_const',
                                dest='subject', const=show_planets)

            (args, params) = parser.parse_known_args(line.split(' '))
            if not args.subject: # no arguments
                args.subject = show_planets
            args.subject(params)
        except SystemExit:
            pass
        return False
    do_sh = do_show

    def help_show(self, no_print=None):
        msg = "Show various things. Use 'show --help' for more."
        if no_print:
            return msg
        print msg

    def do_quit(self, line):
        self.engine.save()
        return True
    do_q = do_quit

    def help_quit(self):
        help = "Quit the program"
        print help

    def do_dbg(self, line):
        print_state = partial(self.ui.dbg_print_state, self.engine)
        try:
            parser = ArgumentParser(prog='dbg',
                                    description=self.help_dbg(True))
            parser.add_argument(
                    '-ps', '--print-state', action='store_const',
                    dest='action', const=print_state,
                    help='print full game state')
            (args, unrecognized) = parser.parse_known_args(line.split(' '))
            if not args.action:
                args.action = print_state
            args.action()
        except SystemExit:
            pass
        return False

    def help_dbg(self, no_print=None):
        hlp = "Provides access to some debugging commands."
        if no_print:
            return hlp
        print hlp

    def do_user(self, line):
        #TODO: implement change name
        print 'Not implemented yet'

    def help_user(self):
        print "Access to user admin tasks"

    def do_planet(self, line):
        print 'Not implemented yet'

    def help_planet(self):
        print "Access to things on planets"

class AttrDict(dict):
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

### Object Model

# resources
METALS = 'metals'
THORIUM = 'thorium'

class Coord(object):
    def __init__(self, x=None, y=None, planet=None):
        if x is None: x = 0
        if y is None: y = 0
        if planet is None: planet = 0
        self.x = float(x)
        self.y = float(y)
        self.planet = int(0)

    @property
    def sector(self):
        return (int(str(self.x).split('.')[0]),
                int(str(self.y).split('.')[0]))

    @sector.setter
    def sector(self, value):
        sec_x = str(int(value[0]))
        sec_y = str(int(value[1]))
        self.x = float('.'.join([sec_x, str(self.x).split('.')[1]]))
        self.y = float('.'.join([sec_y, str(self.y).split('.')[1]]))

    @property
    def system(self):
        return (int(str(self.x).split('.')[1]),
                int(str(self.y).split('.')[1]))

    @system.setter
    def system(self, value):
        sys_x = str(int(value[0]))
        sys_y = str(int(value[1]))
        self.x = float('.'.join([sys_x, str(self.x).split('.')[0]]))
        self.y = float('.'.join([sys_y, str(self.y).split('.')[0]]))

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "Coord(%s, %s, %s)" % (self.x, self.y, self.planet)

    def __str__(self):
        return str((self.x, self.y, self.planet))

class GameState(object):
    def __init__(self, save_file=None):
        self.save_file = save_file
        self.user = None
        self.galaxy = None

    def __repr__(self):
        return ("GameState(save_file=%s,%s,%s)" %
                (self.save_file, self.user, self.galaxy))

class User(object):
    def __init__(self, name, home_planet_coords, home_planet):
        self.name = name
        self.planets = {home_planet_coords: home_planet}
        home_planet.emperor = self.name

    def __repr__(self):
        return ("User(name=%s, planets=%s)" %
                (self.name, self.planets))

    def show_planets(self):
        planets = []
        for coord, planet in self.planets.iteritems():
            planets.append('%s: %s' % (coord, planet.show()))
        planets = indent('\n'.join(planets), '    ')
        return planets

    def show(self):
        return ("User: %s\n  planets:\n%s" %
                (self.name, self.show_planets()))


class Galaxy(object):
    def __init__(self):
        self.systems = defaultdict(System)

    def __repr__(self):
        return ("Galaxy(systems=[%s])" %
                ','.join([str(system) for system in self.systems.iteritems()]))

    def show(self):
        systems = []
        for c, s in self.systems.iteritems():
            sys = indent(s.show(), '  ')[2:]
            systems.append('%s %s' % (c, sys))
        return 'Galaxy:\n%s' % indent('\n'.join(systems), '  ')

class System(object):
    def __init__(self):
        self._size_range = (4, 20)
        self.planets = [Planet() for i in
                        range(random.randint(*self._size_range))]

    def __repr__(self):
        return ("System(size=%s, planets=%s)" %
                (self._size_range, self.planets))

    def show(self, coords=None):
        msg = "%s planet system"
        if coords is not None:
            msg += " at %s" % coords
        msg += "\n[%s]" % ', '.join([p.show() for p in self.planets])
        return msg

class Planet(object):
    def __init__(self):
        self._max_resources = AttrDict([(THORIUM, 1e6),
                                        (METALS, 10e6)])
        self.resources = AttrDict([(THORIUM, 0),
                                   (METALS, 0)])
        self.name = self.__get_new_name()
        self.emperor = None

    def __get_new_name(self, lang_file=None):
        if not lang_file:
            lang_file = 'lib/namegen_lang.txt'
        return NameGen(lang_file).gen_word()

    def __repr__(self):
        return ("Planet(name=%s, resources=%s, emperor=%s)" %
                (self.name, self.resources, self.emperor))

    def show(self):
        res = '\n'.join(['- %s: %s' % (name, amt)
                         for name, amt in self.resources.iteritems()])
        res = indent(res, '  ')
        return "%s, owner %s\n%s" % (self.name, self.emperor, res)


if __name__ == "__main__":
    sys.exit(main())
