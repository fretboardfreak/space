from argparse import ArgumentParser
from cmd import Cmd
from functools import partial

import ui

class SpaceCmdInterpreter(Cmd):
    def __init__(self, engine):
        self.engine = engine
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

    def do_quit(self, line):
        self.engine.save()
        return True

    def help_quit(self):
        help = "Quit the program"
        print help

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

    def do_user(self, line):
        #TODO: implement change name
        print 'Not implemented yet'

    def help_user(self):
        print "Access to user admin tasks"

    def do_planet(self, line):
        show_planets = partial(ui.show_planets, self.engine)
        try:
            parser = ArgumentParser(prog='planet',
                                    description=self.help_show(True))
            parser.add_argument('-v', '--verbose', action='store_true',
                                dest='verbose', default=False)

            (args, params) = parser.parse_known_args(line.split(' '))
            if not hasattr(args, 'action'): # no arguments
                #args.action = show_planets
                show_planets(params, verbose=args.verbose)
            else:
                args.action(params, verbose=args.verbose)
        except SystemExit:
            pass
        return False

    def help_planet(self):
        print "Access to things on planets"


    # shortcuts
    do_sh = do_show
    do_q = do_quit
    do_EOF = do_quit
    #help_sh = help_show
    #help_q = help_quit
    #help_EOF = help_quit
