from lib.rst import indent

class User(object):
    def __init__(self, name, home_planet_coords, home_planet):
        self.name = name
        self.planets = {home_planet_coords: home_planet}
        home_planet.emperor = self.name

    def __repr__(self):
        return ("User(name=%s, planets=%s)" %
                (self.name, self.planets))

    def show_planets(self, verbose=None):
        planets = ['Planets:']
        for coord, planet in self.planets.iteritems():
            if verbose:
                planets.append(' %s: %s' % (coord, planet.show()))
            else:
                planets.append(' %s: %s' % (coord, planet.name))
        return '\n'.join(planets)

    def show(self):
        planets = indent(self.show_planets(), '    ')
        return ("User: %s\n%s" %
                (self.name, planets))

    def __getstate__(self):
        return (self.name, self.planets)

    def __setstate__(self, state):
        (self.name, self.planets) = state
