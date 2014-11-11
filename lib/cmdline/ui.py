from logging import debug

from lib.model import Coord

def input_bool(msg):
    debug('getting a boolean from the user')
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

def input_text(msg):
    debug('getting some text from the user')
    while True:
        name = raw_input(msg)
        if name.isalpha():
            return name

def input_int(msg, min=None, max=None):
    debug('getting an int from the user')
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

def dbg_print_state(engine):
    debug('dbg: printing the game state')
    print engine.state

def show_planets(engine, *args, **kwargs):
    verbose = kwargs['verbose'] if kwargs.has_key('verbose') else False
    debug('showing planets')
    print engine.state.user.show_planets(verbose)

def show_user(engine, *args, **kwargs):
    debug('showing user')
    print engine.state.user.show(kwargs.get('verbose', False))

def newgame_get_user_info(system_query_cb):
    debug('Querying user for new game info...')
    name = input_text("Great another wanna be space emperor! "
                              "What's your name then? ")

    home_coords = Coord()
    sec_x = input_int('Ok, now we need to find your home planet. '
                              'Enter the sector coords:\nx=')
    sec_y = input_int('y=')
    home_coords.sector = (sec_x, sec_y)

    sys_x = input_int('Now the system coords:\nx=')
    sys_y = input_int('y=')
    home_coords.system = (sys_x, sys_y)

    system = system_query_cb(home_coords)
    #TODO: replace this ugliness with a System.show_planets method
    planet_num_qry = ('That system has %s planets. Which one did you say '
                      'was yours?\n%s\nplanet=' %
                      (len(system.planets),
                       '\n'.join([' %s. %s' % (i, p.name) for i, p in
                                  enumerate(system.planets)])))
    planet_num = input_int(planet_num_qry, min=0,
                                   max=len(system.planets)-1)
    home_coords.planet = planet_num
    home_planet = system.planets[planet_num]
    home_planet.resources.ore = 25
    home_planet.resources.metal = 60
    print ("We've given you some building materials to get you started. "
           "Use them wisely, that's all the new recruits get from us!")

    return (name, home_coords, home_planet)
