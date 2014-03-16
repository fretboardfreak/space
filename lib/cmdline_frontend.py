import sys, pickle, readline
from argparse import ArgumentParser
from cmd import Cmd
from functools import partial

from lib.model import GameState, User, Galaxy, Coord

class SpaceEngine(object):
    def __init__(self, save_file, user_interface):
        self.ui = user_interface
        self.state = GameState(save_file)

    def load(self):
        '''Load game state directly. Useful when used on the interpreter'''
        with open(self.state.save_file, 'r') as sf:
            self.state = pickle.load(sf)

    def start_new_game(self):
        #TODO farm most/some of this to a ui method
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
        planet_num = self.ui.input_int(planet_num_qry, min=0,
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
