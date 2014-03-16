class Coord(object):
    def __init__(self, x=None, y=None, planet=None):
        if x is None: x = 0
        if y is None: y = 0
        if planet is None: planet = 0
        self.x = float(x)
        self.y = float(y)
        self.planet = int(planet)

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

    def __eq__(self, other):
        return (other.x == self.x and
                other.y == self.y and
                other.planet == self.planet)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.planet))

    def __repr__(self):
        return "Coord(%s, %s, %s)" % (self.x, self.y, self.planet)

    def __str__(self):
        return str((self.x, self.y, self.planet))
