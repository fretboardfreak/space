from argparse import ArgumentParser
from cmd import Cmd
from functools import partial
from logging import debug

import ui

class CommandMixin(object):
    def __init__(self, engine):
        self.engine = engine

class Quit(CommandMixin):
    def do_quit(self, line):
        self.engine.save()
        return True

    def help_quit(self):
        print "Quit the program"
    do_q = do_quit
    do_EOF = do_quit

class Show(CommandMixin):
    def do_show(self, line):
        show_planets = partial(ui.show_planets, self.engine)
        show_user = partial(ui.show_user, self.engine)
        try:
            parser = ArgumentParser(prog='show',
                                    description=self.help_show(True))
            parser.add_argument('-p', '--planets', action='store_const',
                                dest='subject', const=show_planets)
            parser.add_argument('-u', '--user', action='store_const',
                                dest='subject', const=show_user)
            parser.add_argument('-v', '--verbose', action='store_true',
                                dest='verbose', default=False)

            (args, params) = parser.parse_known_args(line.split(' '))
            if args.subject is None: # no arguments
                args.subject = show_planets
            args.subject(params, verbose=args.verbose)
        except SystemExit:
            pass
        return False

    def help_show(self, no_print=None):
        msg = "Show various things. Use 'show --help' for more."
        if no_print:
            return msg
        print msg
    do_sh = do_show
    do_s = do_show

class Debug(CommandMixin):
    def do_dbg(self, line):
        print_state = partial(ui.dbg_print_state, self.engine)
        try:
            parser = ArgumentParser(prog='dbg',
                                    description=self.help_dbg(True))
            parser.add_argument(
                    '-ps', '--print-state', action='store_const',
                    dest='action', const=print_state,
                    help='print full game state')
            (args, unrecognized) = parser.parse_known_args(line.split(' '))
            if args.action is None:
                print_state()
            else:
                args.action()
        except SystemExit:
            pass
        return False

    def help_dbg(self, no_print=None):
        hlp = "Provides access to some debugging commands."
        if no_print:
            return hlp
        print hlp

class Planet(CommandMixin):
    def _building(self, *args, **kwargs):
        args = kwargs['args']
        if args.building is None:
            ui.show_available_buildings(engine=self.engine,
                                        planet=args.planet,
                                        verbose=args.verbose)
            return
        print "not implemented yet :("

    def do_planet(self, line):
        show_planets = partial(ui.show_planets, self.engine)
        try:
            parser = ArgumentParser(prog='planet',
                                    description=self.help_show(True))
            parser.add_argument('-v', '--verbose', action='store_true',
                                dest='verbose', default=False)
            parser.add_argument('-b', '--building', action='store_const',
                                dest='action', const=self._building)
            parser.add_argument('planet', help='Limit the effect of the '
                                'command to this planet (if supported)',
                                default=None, nargs='?')
            parser.add_argument('building', help='Name of building type to '
                                'pass to the command (if supported, '
                                'PLANET must be supplied first)',
                                default=None, nargs='?')

            (args, params) = parser.parse_known_args(line.split(' '))
            setattr(args, 'params', params)
            if args.action is None:
                args.action = show_planets
            args.action(args=args, verbose=args.verbose)
        except SystemExit:
            pass
        return False

    def help_planet(self):
        print "Access to things on planets"
    do_p = do_planet
    do_pl = do_planet

class User(CommandMixin):
    def do_user(self, line):
        #TODO: implement change name
        print 'Not implemented yet'

    def help_user(self):
        print "Access to user admin tasks"
    do_u = do_user

class SpaceCmdInterpreter(Cmd, Quit, Debug, Show, Planet, User):
    def __init__(self, engine):
        super(SpaceCmdInterpreter, self).__init__()
        self.engine = engine
        self.prompt = 'space> '
        self.doc_header='Space Commands'
        self.undoc_header='Alias Commands'

    def start(self):
        try:
            try:
                debug('Trying to load the saved game...')
                self.engine.load()
            except IOError:
                debug('No save game, starting new game...')
                ui.start_new_game(self.engine)
            debug('Starting interpreter...')
            self.cmdloop()
        except KeyboardInterrupt, SystemExit:
            debug('Recieved Interrupt.')
        finally:
            self.engine.save()
