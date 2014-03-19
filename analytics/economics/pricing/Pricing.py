__author__ = 'Ronaldo'

class Pricing():
    def __init__(self):
        self._data = []

    @property
    def data(self):
        return self._data


p = Pricing()
p._data = 1


print p._data