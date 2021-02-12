import numpy as np
import config

from object import Object   

class Paddle(Object):

    def __init__(self, pos):
        super().__init__(pos, np.array([2,14]))
        self._vel = np.array([0,0])
        self._repr = np.array([
                    [' ', '_', '_', '_', '_', '_','_','_','_','_', '_', '_', '_',' '],
                    ['(', '_','_','_','_','_','_', '_','_','_', '_', '_', '_',')']], dtype='object')

    def in_child(self, pos, size):
        super().__init__(pos, size)
        self._vel = np.array([0,0])

    def getRep(self):
        return self._repr
        
    def move(self,key, ball):
        if key == 'a':
            self._pos[1] = self._pos[1] - 2
            for i in ball:
                i.moveWithPaddle(-2)
            self.handle()
        
        elif key == 'd':
            self._pos[1] = self._pos[1] + 2
            for i in ball:
                i.moveWithPaddle(+2)
            self.handle()

class LongPaddle(Paddle):

    def __init__(self, pos):
        super().in_child(pos, np.array([2,20]))
        self._vel = np.array([0,0])
        self._repr =  np.array([
                    [' ', '_', '_', '_', '_', '_','_','_','_','_', '_', '_', '_','_', '_','_','_','_','_',' '],
                    ['(', '_','_','_','_','_','_', '_','_','_', '_', '_', '_','_', '_','_','_','_','_',')']], dtype='object')

class ShortPaddle(Paddle):

    def __init__(self, pos):
        super().in_child(pos, np.array([2,10]))
        self._vel = np.array([0,0])
        self._repr = np.array([
                    [' ', '_', '_', '_', '_', '_','_','_', '_',' '],
                    ['(', '_','_','_','_','_','_', '_', '_',')']], dtype='object')




        
