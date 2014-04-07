from resources import Resources

class Building(object):
    def __init__(self):
        self.cost = Resources(ore=1, metal=1, electricity=1)
        self.modifier = Resources(electricity=1)
