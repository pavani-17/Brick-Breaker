import numpy as np

from object import Object

class Laser(Object):

    def __init__(self, pos):
        super().__init__(pos, np.array([1,1]))
        self._vel = np.array([-1, 0])
        self._rep = '|'
        self._isVisible = True

    def getVelocity(self):
        return self._vel

    def getType(self):
        return 'Laser'

    def hideVisibility(self):
        self._isVisible = False

    def isVisible(self):
        return self._isVisible

    def move(self):
        self._pos += self._vel
        if(self._pos[0] <= 1):
            self._isVisible = False