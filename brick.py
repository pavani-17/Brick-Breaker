from object import Object
import numpy as np
from colorama import Fore, Back, Style
import config

class Brick(Object):

    def __init__(self, pos):
        super().__init__(pos, np.array([3,10]))
        self._rep = np.array([
            [' ', '_', '_','_','_','_', '_','_','_', ' '],
            ['|', 'o', ' ','o',' ','o', ' ','o',' ', '|'],
            ['|', '_', '_', '_','_','_', '_','_','_','|']
        ])
        self._isVisible = True
        self._col = np.full(self._size, Fore.YELLOW)
        self._type =0
        
    
    def collideBall(self, ball, game):
        x1, y1 = ball.getPosition()
        vx, vy = ball.getVelocity()
        obj_type = ball.getType()
        if obj_type == 'Ball':
            temp = ball.isThruBall()
            temp1 = ball.isFireBall()
        else:
            temp = False
            temp1 = False
        collide = False

        ## Right collision

        if (y1 >= self._pos[1] + self._size[1] and y1 + vy < self._pos[1] + self._size[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            if temp:
                self._isVisible = False
                collide = True
            elif temp1: 
                self._isVisible = False
                collide = True
                ball.collideBrick(np.array([1,-1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([1,-1]))
            else:
                ball.hideVisibility()
                return

        ## Left collision

        if (y1 < self._pos[1] and y1 + vy >= self._pos[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            if temp:
                self._isVisible = False
                collide = True
            elif temp1:
                self._isVisible = False
                collide = True
                ball.collideBrick(np.array([1,-1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([1,-1]))
            else:
                ball.hideVisibility()
                return

        ## Vertical Collision
        if (x1 < self._pos[0] and x1 + vx >= self._pos[0]) and (y1+vy >= self._pos[1] and y1+vy < self._pos[1] + self._size[1]):
            if temp:
                self._isVisible = False
                collide = True
            elif temp1:
                self._isVisible = False
                collide = True
                ball.collideBrick(np.array([-1,1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([-1,1]))
            else:
                ball.hideVisibility()
                return

        if (x1 >= self._pos[0] + self._size[0] and x1 + vx < self._pos[0] + self._size[0]) and (y1+vy >= self._pos[1] and y1+vy < self._pos[1] + self._size[1]):
            if temp:
                self._isVisible = False
                collide = True
            elif temp1:
                self._isVisible = False
                collide = True
                ball.collideBrick(np.array([-1,1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([-1,1]))
            else:
                ball.hideVisibility()
                return

        if collide:
            game.incrementScore(5)
            if temp1:
                game.explodeBricks(self._pos, self._size)
                

    def moveDown(self):
        self._pos[0] += 1

        if self._pos[0] + self._size[0] >= config.HEIGHT-3:
            return True
        return False 

    def explodeBrick(self, game):
        self._isVisible = False
        game.incrementScore(5)

    def isVisible(self):
        return self._isVisible

    def getType(self):
        return self._type
    
    def isRainbow(self):
        return False

class Breakable(Brick):
    def __init__(self, pos, strength):
        super().__init__(pos)
        self._strength = strength
        self._type = 1

    def collideBall(self, ball, game):

        if self._strength == 0:
            return
        x1, y1 = ball.getPosition()
        vx, vy = ball.getVelocity()

        obj_type = ball.getType()
        if obj_type == 'Ball':
            temp = ball.isThruBall()
            temp1 = ball.isFireBall()
        else:
            temp = False
            temp1 = False
        collide = False
        val = self._strength

        ## Right collision

        if (y1 >= self._pos[1] + self._size[1] and y1 + vy < self._pos[1] + self._size[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if temp:
                self._strength = 0
            elif temp1:
                self._strength = 0
                ball.collideBrick(np.array([1,-1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([1,-1]))
            else:
                ball.hideVisibility()
            

        ## Left collision

        if (y1 < self._pos[1] and y1 + vy >= self._pos[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if temp:
                self._strength = 0
            elif temp1:
                self._strength = 0
                ball.collideBrick(np.array([1,-1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([1,-1]))
            else:
                ball.hideVisibility()

        ## Vertical Collision
        if (x1 < self._pos[0] and x1 + vx >= self._pos[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            if temp:
                self._strength = 0
            elif temp1:
                self._strength = 0
                ball.collideBrick(np.array([-1,1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([-1,1]))
            else:
                ball.hideVisibility()

        if (x1 >= self._pos[0] + self._size[0] and x1 + vx < self._pos[0] + self._size[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            if temp:
                self._strength = 0
            elif temp1:
                self._strength = 0
                ball.collideBrick(np.array([-1,1]))
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([-1,1]))
            else:
                ball.hideVisibility()

        if collide == True:
            self._strength = self._strength - 1
        
        if collide:
            if temp:
                game.incrementScore(val*abs(vy+1))
            elif temp1:
                game.explodeBricks(self._pos, self._size)
                game.incrementScore(abs(vy+1))
            else:
                game.incrementScore(abs(vy+1))

        if self._strength <= 0:
            self._pos = np.array([0,0])
            self._size = np.array([0,0])
            self._isVisible = False
            return 1
        return 0

    def explodeBrick(self, game):
        self._isVisible = False
        game.incrementScore(self._strength)
        self._strength = 0

    def getColor(self):

        if self._strength == 1:
            return (np.full(self._size, Fore.GREEN, dtype=object))

        elif self._strength == 2:
            return (np.full(self._size, Fore.CYAN, dtype=object))

        else:
            return (np.full(self._size, Fore.RED, dtype=object))

class RainbowBrick(Breakable):

    def __init__(self, pos):
        super().__init__( pos, np.random.randint(1, 4))
        self._touched = False
        self._type = 4    

    def collideBall(self, ball, game):

        if self._strength == 0:
            return
        x1, y1 = ball.getPosition()
        vx, vy = ball.getVelocity()

        obj_type = ball.getType()
        if obj_type == 'Ball':
            temp = ball.isThruBall()
            temp1 = ball.isFireBall()
        else:
            temp = False
            temp1 = False
        collide = False
        val = self._strength

        ## Right collision

        if (y1 >= self._pos[1] + self._size[1] and y1 + vy < self._pos[1] + self._size[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if temp:
                self._strength = 0
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([1,-1]))
            else:
                ball.hideVisibility()

        ## Left collision

        if (y1 < self._pos[1] and y1 + vy >= self._pos[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if temp:
                self._strength = 0
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([1,-1]))
            else:
                ball.hideVisibility()

        ## Vertical Collision
        if (x1 < self._pos[0] and x1 + vx >= self._pos[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            if temp:
                self._strength = 0
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([-1,1]))
            else:
                ball.hideVisibility()

        if (x1 >= self._pos[0] + self._size[0] and x1 + vx < self._pos[0] + self._size[0]) and (y1+vy >= self._pos[1] and y1+vy <= self._pos[1] + self._size[1]):
            collide = True
            if temp:
                self._strength = 0
            elif obj_type == 'Ball':
                ball.collideBrick(np.array([-1,1]))
            else:
                ball.hideVisibility()

        if collide == True:
            self._strength = self._strength - 1
        
        if collide:
            self._touched = True
            if temp:
                game.incrementScore(val*abs(vy+1))
            elif temp1:
                game.explodeBricks(self._pos, self._size)
                game.incrementScore(abs(vy+1))
            else:
                game.incrementScore(abs(vy+1))

        if self._strength <= 0:
            self._pos = np.array([0,0])
            self._size = np.array([0,0])
            self._isVisible = False
            return 1
        return 0

    def changeStrength(self):
        if not self._touched:
            self._strength = (self._strength + 1)%3 + 1 
    
    def isRainbow(self):
        return True

class ExplodingBrick(Brick):

    def __init__(self, pos):
        super().__init__(pos)
        self._strength = 1
        self._col = np.full(self._size, Fore.MAGENTA, dtype=object)
        self._type = 4
    
    def collideBall(self, ball, game):

        x1, y1 = ball.getPosition()
        vx, vy = ball.getVelocity()

        collide = False
        temp = ball.isThruBall()        

        ## Right collision

        if (y1 >= self._pos[1] + self._size[1] and y1 + vy < self._pos[1] + self._size[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if not temp:
                ball.collideBrick(np.array([1, -1]))

        ## Left collision

        if (y1 < self._pos[1] and y1 + vy >= self._pos[1]) and (x1 + vx >= self._pos[0] and x1+vx <= self._pos[0]+self._size[0]):
            collide = True
            if not temp:
                ball.collideBrick(np.array([1, -1]))

        ## Vertical Collision
        if (x1 < self._pos[0] and x1 + vx >= self._pos[0]) and (y1+vy >= self._pos[1] and y1+vy < self._pos[1] + self._size[1]):
            collide = True
            if not temp:
                ball.collideBrick(np.array([-1,1]))

        if (x1 >= self._pos[0] + self._size[0] and x1 + vx < self._pos[0] + self._size[0]) and (y1+vy >= self._pos[1] and y1+vy < self._pos[1] + self._size[1]):
            collide = True
            if not temp:
                ball.collideBrick(np.array([-1,1]))

        if collide:
            game.explodeBricks(self._pos, self._size)
            return True
        
        return False

    def explodeBrick(self, game):
        self._isVisible = False
        game.incrementScore(5)
        game.explodeBricks(self._pos, self._size)





    

    
    