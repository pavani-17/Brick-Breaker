import numpy as np
import config

class Object:

    def __init__(self, pos=np.array([0,0]), size = np.array([1,1])):

        self._pos = pos
        self._size = size
        self._vel = np.array([0,0])

    def handle(self):
        if self._pos[0]  < 0:
            self._pos[0] = 0
        
        if self._pos[0] + self._size[0] > config.HEIGHT - 1:
            self._pos[0] = config.HEIGHT - 1 - self._size[0]
        
        if self._pos[1] < 0:
            self._pos[1] = 0
        
        if self._pos[1] + self._size[1] > config.WIDTH -1:
            self._pos[1] = config.WIDTH - 1 - self._size[1]

    def getPosition(self):
        return self._pos

    def getSize(self):
        return self._size