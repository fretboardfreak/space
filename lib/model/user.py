from lib.rst import indent

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
        return '\n'.join(planets)

    def show(self):
        planets = indent(self.show_planets(), '    ')
        return ("User: %s\n  planets:\n%s" %
                (self.name, planets))
