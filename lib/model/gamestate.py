__all__ = ['GameState']


class GameState(object):
    def __init__(self, save_file=None):
        self.save_file = save_file
        self.user = None
        self.galaxy = None

    def __repr__(self):
        return ("GameState(save_file=%s,%s,%s)" %
                (self.save_file, self.user, self.galaxy))

    def __getstate__(self):
        return (self.save_file, self.user, self.galaxy)

    def __setstate__(self, state):
        (self.save_file, self.user, self.galaxy) = state
