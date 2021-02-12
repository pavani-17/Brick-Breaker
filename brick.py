from object import Object
import numpy as np

class Brick(Object):

    def __init__(self, pos):
        super().__init__(pos, np.array([3,10]))
        self._rep = np.array([
            [' ', '_', '_','_','_','_', '_','_','_', ' '],
            ['|', ' ', ' ',' ',' ',' ', ' ',' ',' ', '|'],
            ['|', '_', '_', '_','_','_', '_','_','_','|']
        ])
        self._isVisible = True

    def getRep(self):
        return self._rep
    
    def collideBall(self, ball, game):
        x1, y1 = ball.getPosition()
        vx, vy = ball.getVelocity()
        temp = ball.isThruBall()
        collide = False

        ## Right collision

        if (y1 >= self._pos[1] + self._size[1] and y1 + vy < self._pos[1] + self._size[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            if temp:
                self._isVisible = False
                collide = True
            else:
                ball.collideBrick(np.array([1,-1]))

        ## Left collision

        if (y1 < self._pos[1] and y1 + vy >= self._pos[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            if temp:
                self._isVisible = False
                collide = True
            else:
                ball.collideBrick(np.array([1,-1]))

        ## Vertical Collision
        if (x1 < self._pos[0] and x1 + vx >= self._pos[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            if temp:
                self._isVisible = False
                collide = True
            else:
                ball.collideBrick(np.array([-1,1]))

        if (x1 >= self._pos[0] + self._size[0] and x1 + vx < self._pos[0] + self._size[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            if temp:
                self._isVisible = False
                collide = True
            else:
                ball.collideBrick(np.array([-1,1]))

        if collide:
            game.incrementScore(5)

    def isVisible(self):
        return self._isVisible

class Breakable(Brick):
    def __init__(self, pos, strength):
        super().__init__(pos)
        self._strength = strength

    def collideBall(self, ball, game):

        if self._strength == 0:
            return
        x1, y1 = ball.getPosition()
        vx, vy = ball.getVelocity()

        temp = ball.isThruBall()
        collide = False
        val = self._strength

        ## Right collision

        if (y1 >= self._pos[1] + self._size[1] and y1 + vy < self._pos[1] + self._size[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if temp:
                self._strength = 0
            else:
                ball.collideBrick(np.array([1,-1]))

        ## Left collision

        if (y1 < self._pos[1] and y1 + vy >= self._pos[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if temp:
                self._strength = 0
            else:
                ball.collideBrick(np.array([1,-1]))

        ## Vertical Collision
        if (x1 < self._pos[0] and x1 + vx >= self._pos[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            if temp:
                self._strength = 0
            else:
                ball.collideBrick(np.array([-1,1]))

        if (x1 >= self._pos[0] + self._size[0] and x1 + vx < self._pos[0] + self._size[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            if temp:
                self._strength = 0
            else:
                ball.collideBrick(np.array([-1,1]))

        if collide == True:
            self._strength = self._strength - 1
        
        if collide:
            if temp:
                game.incrementScore(val*abs(vy+1))
            else:
                game.incrementScore(abs(vy+1))

        if self._strength <= 0:
            self._pos = np.array([0,0])
            self._size = np.array([0,0])
            self._isVisible = False
            return 1
        return 0

    

    

    
    