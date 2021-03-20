from art import *
from object import Object
import config
import threading
from playsound import playsound

class Ufo(Object):

    def __init__(self, pos):
        pos[1] = pos[1] - 20
        if(pos[1] <= 1):
            pos[1] = 1
        if(pos[1] + 41 >= config.WIDTH):
            pos[1] = config.WIDTH - 41

        super().__init__(pos,np.array([8,41]))
        self._rep = getUfo()
        self._strength = 20
        self._isVisible = True

    def setPosition(self, pos):
        self._pos[1] = pos[1] - 20
        if(self._pos[1] <= 1):
            self._pos[1] = 1
        if(self._pos[1] + 41 >= config.WIDTH-1):
            self._pos[1] = config.WIDTH - 42

    def getStrength(self):
        return self._strength

    def collideBall(self, ball, game):

        x1, y1 = ball.getPosition()
        vx, vy = ball.getVelocity()

        collide = False

        if (y1 >= self._pos[1] + self._size[1] and y1 + vy < self._pos[1] + self._size[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            ball.collideBrick(np.array([1,-1]))
            

        if (y1 < self._pos[1] and y1 + vy >= self._pos[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            ball.collideBrick(np.array([1,-1]))

        if (x1 < self._pos[0] and x1 + vx >= self._pos[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            ball.collideBrick(np.array([-1,1]))

        if (x1 >= self._pos[0] + self._size[0] and x1 + vx < self._pos[0] + self._size[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            ball.collideBrick(np.array([-1,1]))

        if collide:
            threading.Thread(target=playsound, args=('ball_wall.wav',), daemon=True).start()
            self._strength = self._strength - 1
            if(self._strength <= 0):
                self._isVisible = False
                game.removeUfo()
    
    def isVisible(self):
        return self._isVisible


class Bomb(Object):

    def __init__(self,pos):
        super().__init__(pos, np.array([1,1]))
        self._rep = '*'
        self._vel = [1,0]
        self._isVisible = True

    def isVisible(self):
        return self._isVisible

    def move(self):
        self._pos = self._pos + self._vel
        if(self._pos[0] >= config.HEIGHT):
            self._isVisible = False

    def makeInvisible(self):
        self._isVisible = False