import numpy as np

from object import Object
import config

class Ball(Object):

    def __init__(self, pos, vel, stick):
        super().__init__(pos, np.array([1,1]))
        self._stickPaddle = stick
        self._paddleGrab = False
        self._thruBall = False
        self._vel = vel
        self._rep = 'O'
        self._fast = 1

    def getRep(self):
        return self._rep
    
    def getVelocity(self):
        return self._vel

    def release(self):
        if self._stickPaddle:
            self._pos[0] = self._pos[0] - self._size[0]
            self._stickPaddle = False

    def handleCollision(self):
        
        if self._pos[0] <= 1:
            self._vel[0] = - self._vel[0] 
        
        if self._pos[1] + self._vel[1]< 0 or self._pos[1] + self._vel[1] > config.WIDTH - 1:
            self._vel[1] = -self._vel[1]
        
        if self._pos[0] >= config.HEIGHT - 2:
            return 1
        
        return 0

    def move(self):
    
        if not self._stickPaddle:
            self._pos = self._pos + (self._vel)
            return self.handleCollision()
        return 0
        
    def moveWithPaddle(self, val):

        if self._stickPaddle and self._pos[0] >= (config.HEIGHT-3):
            self._pos[1] += val
            self.handle()

    def collidePaddle(self, speed):

        if not self._stickPaddle:
            self._vel[1] = speed*self._fast
            self._vel[0] = -self._vel[0]

            if self._paddleGrab:
                self._stickPaddle = True

    def isThruBall(self):
        return self._thruBall

    def makeThruBall(self):
        self._thruBall = True

    def makeNormal(self):
        self._thruBall = False
    
    def collideBrick(self, vel):
        self._vel = self._vel * vel

    def increaseSpeed(self):
        if not self._stickPaddle:
            self._vel[1] = self._vel[1]*2
        self._fast = self._fast * 2
    
    def decreaseSpeed(self):
        self._fast = self._fast/2
        self._vel[1] = self._vel[1]/2
    
    def stickPaddle(self):
        self._paddleGrab = True

    def releasePaddle(self):
        self._paddleGrab = False