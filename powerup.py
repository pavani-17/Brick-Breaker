import numpy as np
import time

from object import Object

class Powerup(Object):

    def __init__(self,pos):
        super().__init__(pos, np.array([1,1]))
        self._isVisible = False
        self._isActivated = False
        self._deactivateTime = 0
    
    def release(self):
        self._isVisible = True
        self._vel = [1, 0]

    def move(self, paddle):
        if self._isVisible:
            self._pos = self._pos + self._vel
            x1, y1 = paddle.getPosition()
            _, w = paddle.getSize()
            if x1 == self._pos[0] and y1 <= self._pos[1] <= y1 + w:
                self._isVisible = False
                self._isActivated = True
            
            elif x1 == self._pos[0]:
                self._isVisible = False

    def isVisible(self):
        return self._isVisible

    def setTime(self, val):
        if self._isActivated:
            self._deactivateTime = val

    def isActivated(self):
        return self._isActivated
    
    def getTime(self):
        return self._deactivateTime
        
class FastBall(Powerup):

    def __init__(self, pos):
        super().__init__(pos)
        self._rep = np.array(['F'])
        self._type = 'F'

    def activate(self, ball):
        
        if self._isActivated:
            for i in ball:
                i.increaseSpeed()

    def deactivate(self, ball):

        self._isActivated = False
        for i in ball:
            i.decreaseSpeed()

    def getRep(self):
        return self._rep

    def getType(self):
        return self._type


class LongPaddlePowerup(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
        self._rep = np.array(['L'])
        self._type = 'L'

    def activate(self, game):
        if self._isActivated:
            game.changeLongPaddle()
    
    def deactivate(self, game):
        game.changeNormalPaddle()
        self._isActivated = False
    
    def getRep(self):
        return self._rep
    
    def getType(self):
        return self._type

class ShortPaddlePowerup(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
        self._rep = np.array(['S'])
        self._type = 'S'

    def activate(self, game):
        if self._isActivated:
            game.changeShortPaddle()

    def deactivate(self, game):
        game.changeNormalPaddle()
        self._isActivated = False
    
    def getRep(self):
        return self._rep
    
    def getType(self):
        return self._type

class StickBall(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
        self._rep = np.array(['B'])
        self._type = 'B'

    def activate(self, ball):
        
        if self._isActivated:
            for i in ball:
                i.stickPaddle()
    
    def deactivate(self, ball):
        for i in ball:
            i.releasePaddle()
        self._isActivated = False

    def getRep(self):
        return self._rep

    def getType(self):
        return self._type

class ThruBall(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
        self._rep = np.array(['T'])
        self._type = 'T'

    def activate(self, ball):
        if self._isActivated:
            for i in ball:
                i.makeThruBall()

    def deactivate(self, ball):
        for i in ball:
            i.makeNormal()
        self._isActivated = False

    def getRep(self):
        return self._rep

    def getType(self):
        return self._type

class MultiplyBall(Powerup):
    def __init__(self, pos):
        super().__init__(pos)
        self._rep = np.array(['M'])
        self._type = 'M'
        self._numBalls = 0

    def activate(self, game, balls):
        if self._isActivated:
            game.multiplyBalls()
            self._numBalls = balls
    
    def deactivate(self, game):
        game.decreaseBalls(self._numBalls)
        self._isActivated = False

    def getRep(self):
        return self._rep

    def getType(self):
        return self._type
    

