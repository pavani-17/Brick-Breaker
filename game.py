import os
import sys
import numpy as np
import time

import config
from screen import Screen
from paddle import Paddle
from input import input_to, Get
from ball import Ball
from brick import Breakable, Brick, ExplodingBrick, RainbowBrick
from powerup import FastBall, LongPaddlePowerup, ShortPaddlePowerup, StickBall, ThruBall, MultiplyBall,ShootLaser, FireBall
from laser import Laser
from ufo import Ufo, Bomb
import threading
from playsound import playsound

class Game:

    def start(self):
        if config.HEIGHT < 38 or config.WIDTH < 168:
            print("Please play on full screen")
            quit()
        print("\033[?25l\033[2J", end='')
        self._screen = Screen()        
        self._paddle = Paddle(np.array([config.HEIGHT-3, config.WIDTH/2 - 7]), np.array([1,16]))
        self._ball = []
        self._ball.append(Ball(np.array([config.HEIGHT-4, config.WIDTH/2]), np.array([-1, 0]), True))
        self._lives = 5
        self._balls = 1
        self._score = 0
        self._level = 1
        self._start_time = time.time()
        self._printscore = 0
        self._move = False
        self._laser = False
        self._lasertime = self._start_time
        self._ufo = None
        self._isUfo = False
        get = Get()
        self.bricks_pos_l2 = np.array([
           [18, 66, 2, 2, 0], [18, 75,3, 1, 1], [18, 84, 1, 3, 2], 
           [16,70,2,4,3], [16,79,2,5,4],[16,88,3,6,5], [16, 61,3,2,6],
           [14,75,-1, 0,0], [14,84,-1, 0,0], [14,66,-1, 0,0], [14, 93, -1, 0 ,0], [14, 57, -1, 0, 0], [14,48,-1,0,0], [14,102,-1,0,0],
           [12, 79, 1, 1, 7], [12, 70, 1, 3, 8], [12,88,0,2,9], [12, 61,0,6,10],
           [10, 75, 1, 4, 11], [10, 66, 2, 5, 12], [10, 84, 3, 6, 13], 
        ])
        self.bricks_pos_l1 = np.array([
            [8,14,0,0,0], [8,23,1,1,0], [8, 32, 0, 0,0], [6, 23, 2, 4,1], [4,14,0,0,0], [4,23,1,2,2], [4, 32, 0, 0,0],
           [8,127,0,0,0], [8,136,1,3,3], [8,145,0,0,0],[6,136,2,5,4],[4,127,0,0,0], [4,136,1,6,5], [4,145,0,0,0], 
           [14,75,4,7,6], [14, 84, 4, 8, 7],
           [12, 75, 4,0,0], [12, 84, 4,0,0],
           [10,75,4,0,0], [10,84,4,0,0],
        ])
        self.bricks_pos_l3 = np.array([
            [15,5,0,0,0], [15,150,0,0,0]
        ])
        self.ufo_layer1 = np.array([
            [15,5,0,0,0],[15,150,0,0,0],
            [10,3,1,0,0], [10,12,2,0,0], [10,21,3,0,0], [10,30,2,0,0], [10,39,1,0,0],[10,48,2,0,0], [10,57,3,0,0], [10,66,2,0,0], [10,75,1,0,0], [10,84,2,0,0],
            [10, 93, 3, 0, 0], [10,102,2,0,0], [10,111,1,0,0], [10,120,2,0,0], [10,129,3,0,0],[10,138,2,0,0], [10,147,1,0,0], [10,156,2,0,0]
        ])
        self.ufo_layer2 = np.array([
            [15,5,0,0,0],[15,150,0,0,0],
            [10,3,1,0,0], [10,12,2,0,0], [10,21,3,0,0], [10,30,2,0,0], [10,39,1,0,0],[10,48,2,0,0], [10,57,3,0,0], [10,66,2,0,0], [10,75,1,0,0], [10,84,2,0,0],
            [10, 93, 3, 0, 0], [10,102,2,0,0], [10,111,1,0,0], [10,120,2,0,0], [10,129,3,0,0],[10,138,2,0,0], [10,147,1,0,0], [10,156,2,0,0],
            [13,3,1,0,0], [13,12,2,0,0], [13,21,3,0,0], [13,30,2,0,0], [13,39,1,0,0],[13,48,2,0,0], [13,57,3,0,0], [13,66,2,0,0], [13,75,1,0,0], [13,84,2,0,0],
            [13, 93, 3, 0, 0], [13,102,2,0,0], [13,111,1,0,0], [13,120,2,0,0], [13,129,3,0,0],[13,138,2,0,0], [13,147,1,0,0], [13,156,2,0,0]
        ])
        self.bricks_pos = self.bricks_pos_l1
        self.powerup = []
        self._len = self.bricks_pos.shape[0]
        self.createBricks()
        self.laserbeams = []
        self.lastlaser = self._start_time
        self.bombtime = self._start_time
        self._bombs = []
        self._spawn1 = False
        self._spawn2 = False

        self.lastMove = self._start_time
        while True:
            self._screen.clear()
            self._screen.drawBackGround()
            inchar = input_to(get.__call__)
            self.handleInput(inchar)
            self.createLaser()
            self.moveBalls()
            self._screen.drawObject(self._paddle)
            self.spawnBricks()
            self.drawBricks()
            self.handleCollisionBallPaddle() 
            self.handleCollisionBallBrick() 
            self.drawUfo()    
            self.drawBalls()
            self._screen.printScreen()
            time_temp = int(time.time() - self._start_time)
            self._printscore = int(self._score + max(0, (1000 - time_temp)/100))
            print("\r Lives ", self._lives, "   Score ", self._printscore, "   Time ", time_temp, "   Level ",self._level, "    ")
            if(self._laser):
                print("Remaining Time ",-int(time.time() - self._lasertime))
            elif self._isUfo:
                print("Boss Strenth: ",end="")
                strength = self._ufo.getStrength()
                for i in range(0,strength):
                    print('o',end="")
                for i in range(strength,20):
                    print(' ',end="")
                print()
            else:
                for i in range(0,30):
                    print(' ',end="")
                print()

    def drawUfo(self):
        if self._isUfo and self.bombtime + 5 < time.time():
            pos = self._ufo.getPosition()
            size = self._ufo.getSize()
            temp = Bomb(np.array([pos[0] + size[0], pos[1] + size[1]/2]))
            self._bombs.append(temp)
            self.bombtime = time.time()
            threading.Thread(target=playsound, args=('laser.wav',), daemon=True).start()

        if self._isUfo:
            if self._ufo.isVisible:
                self._screen.drawObject(self._ufo)
        
            for i in self._bombs:
                if i.isVisible():
                    self._screen.drawObject(i)

    def spawnBricks(self):
        if self._isUfo:
            if self._ufo.getStrength() <= 10 and self._spawn1 is False:
                self._spawn1 = True
                self.bricks_pos = self.ufo_layer1

                for j in range(self._len, len(self.ufo_layer1)):
                    i = self.ufo_layer1[j]
                    temp = Breakable(np.array([i[0], i[1]]),i[2])
                    self._brick.append(temp)
                self._len = len(self._brick)
            
            if self._ufo.getStrength() <= 5 and self._spawn2 is False:
                self._spawn2 = True
                self.bricks_pos = self.ufo_layer2

                for j in range(self._len, len(self.ufo_layer2)):
                    i = self.ufo_layer2[j]
                    temp = Breakable(np.array([i[0], i[1]]), i[2])
                    self._brick.append(temp)
                self._len = len(self._brick)

    def removeUfo(self):
        self._isUfo = False

    def createLaser(self):
        if(self.lastlaser + 1 < time.time() and self._laser):
            threading.Thread(target=playsound, args=('laser.wav',), daemon=True).start()
            pos = self._paddle.getPosition()
            size = self._paddle.getSize()
            temp = Laser(np.array([pos[0], pos[1]+1]))
            self.laserbeams.append(temp)
            temp = Laser(np.array([pos[0], pos[1] + size[1]-1]))
            self.laserbeams.append(temp)
            self.lastlaser = time.time()

    def decreaseLives(self):
        threading.Thread(target=playsound, args=('life.wav',), daemon=True).start()
        self._lives = self._lives - 1
        self._screen.flash()
        if self._lives == 0:
            self._screen.gameOver(win=False, score=0)
            quit()
        for i in self.powerup:
            if i.isActivated():
                p = i.getType()
                if p == 'F' or p == 'B' or p == 'T':
                    i.deactivate(self._ball)
                elif p == 'L' or p == 'S' or p == 'M':
                    i.deactivate(self)
                elif p == '|':
                    i.deactivate(self._paddle, self)
                    
        self._balls = 1
        x, y = self._paddle.getPosition()
        _, w = self._paddle.getSize()
        self._ball = []
        self._ball.append(Ball(np.array([x-1, y + w/2]), np.array([-1, 0]), True))

    def moveBalls(self):
        for i in self._ball:
            if i.move():
                self._ball.remove(i)
                self._balls = self._balls - 1

        if self._balls == 0:
            self.decreaseLives()

        for i in self.laserbeams:
            if i.isVisible():
                i.move()

        for i in self._bombs:
            if i.isVisible():
                i.move()

    def moveBricks(self):
        for i in self._brick:
            if(i.moveDown()):
                self._screen.flash()
                self._screen.gameOver(win=False, score=0)
                quit()
            
        
        for i in self.powerup:
            i.moveDown()

    def drawBalls(self):
        if(self.lastMove + 100 <= time.time() and not self._move):
            self._move = True
        for i in self._ball:
            self._screen.drawObject(i)
        for i in self.laserbeams:
            if i._isVisible:
                self._screen.drawObject(i)

    def createBricks(self):
        self._brick = []
        for i in self.bricks_pos:
            if(i[2] == 0):
                temp = Brick(np.array([i[0], i[1]]))

            elif i[2] == -1:
                temp = ExplodingBrick(np.array([i[0], i[1]]))
                
            elif i[2] == 4:
                temp = RainbowBrick(np.array([i[0], i[1]]))
                
            else:
                temp = Breakable(np.array([i[0], i[1]]),i[2])

            self._brick.append(temp)

            if (i[3] != 0):
                if(i[3] == 1):
                    temp1 = FastBall(np.array([i[0], i[1]])) 
                elif(i[3] == 2):
                    temp1 = LongPaddlePowerup(np.array([i[0], i[1]]))   
                elif (i[3] == 3):
                    temp1 = ShortPaddlePowerup(np.array([i[0], i[1]]))
                elif (i[3] == 4):
                    temp1 = StickBall(np.array([i[0], i[1]]))
                elif (i[3] == 5):
                    temp1 = ThruBall(np.array([i[0], i[1]]))
                elif (i[3] == 6):
                    temp1 = MultiplyBall(np.array([i[0], i[1]]))
                elif(i[3] == 7):
                    temp1 = ShootLaser(np.array([i[0], i[1]])) 
                elif(i[3] == 8):
                    temp1 = FireBall(np.array([i[0], i[1]]))
                
                self.powerup.append(temp1)



    def nextLevel(self):
        self._level += 1
        self._screen.flash()
        if(self._level == 2):
            self.bricks_pos = self.bricks_pos_l2
        elif (self._level == 3):
            threading.Thread(target=playsound, args=('boss.wav',), daemon=True).start()
            self.bricks_pos = self.bricks_pos_l3
            pos = self._paddle.getPosition()
            size = self._paddle.getSize()
            self._isUfo = True
            self._ufo = Ufo(np.array([2, pos[1] + size[1]/2]))
        else:
            time_temp = int(time.time() - self._start_time)
            self._screen.gameOver(win=True, score=(self._score + max(0, (1000 - time_temp)/100)))
            quit()

        self._move = False
        self._len = self.bricks_pos.shape[0]
        self.powerup = []
        self._laser = False
        self.laserbeams = []
        self.createBricks()
        self._paddle = Paddle(np.array([config.HEIGHT-3, config.WIDTH/2 - 7]), np.array([1,16]))
        self._ball = []
        self._ball.append(Ball(np.array([config.HEIGHT-4, config.WIDTH/2]), np.array([-1, 0]), True))
        self._balls = 1
        self.lastMove = time.time()

    def drawBricks(self):
        
        levelDone = True
        for i in self._brick:
            if i.isRainbow():
                i.changeStrength()
            if i.isVisible():
                self._screen.drawObject(i)
                if i.getType() != 0:
                    levelDone = False

        if self._isUfo and self._ufo.isVisible():
            levelDone = False

        if levelDone == True:
            self.nextLevel()

        for i in self.powerup:
            if i.isVisible():
                i.move(self._paddle)
                p = i.getType()
                if p == 'F' or p == 'B' or p == 'T' or p == '!':
                    i.activate(self._ball)
                    i.setTime(time.time() + 50)
                elif p == 'L' or p == 'S':
                    i.activate(self)
                    i.setTime(time.time() + 50)
                elif p == 'M':
                    i.activate(self, len(self._ball))
                    i.setTime(time.time() + 50)
                elif p == '|':
                    i.activate(self._paddle, self)
                    self._lasertime = time.time()+50
                    i.setTime(self._lasertime)

                self._screen.drawObject(i)
            if i.isActivated() and i.getTime() < time.time():
                p = i.getType()
                if p == 'F' or p == 'B' or p == 'T' or p == '!':
                    i.deactivate(self._ball)
                elif p == 'L' or p == 'S' or p == 'M':
                    i.deactivate(self)
                elif p == '|':
                    i.deactivate(self._paddle, self)

    def changeLaserStatus(self, val):
        self._laser = val
        if val == False:
            if self._lasertime < time.time():
                self._laser = True

    def changeLongPaddle(self):
        x, y = self._paddle.getPosition()
        _, w = self._paddle.getSize()
        
        self._paddle = Paddle(np.array([x,y]), np.array([1, w+3]), self._paddle.isShoots())

    def changeShortPaddle(self):
        x, y = self._paddle.getPosition()
        _, w = self._paddle.getSize()
        
        if (w>8):
            self._paddle = Paddle(np.array([x,y]), np.array([1, w-3]), self._paddle.isShoots())

    def multiplyBalls(self):
        length = len(self._ball)
        for j in range(length):
            i = self._ball[j]
            vx, vy = i.getVelocity()
            x, y = i.getPosition()
            self._balls += 1
            self._ball.append(Ball(np.array([x, y]), np.array([-vx, -vy]), False))   

    def decreaseBalls(self, balls):
        length = len(self._ball)
        if length > balls:
            while(balls > 0):
                self._ball.pop()
                balls = balls - 1
                self._balls = self._balls - 1


    def incrementScore(self,val):
        self._score = self._score + val         

    def handleCollisionBallBrick(self):

        for ball in self._ball:
            for j in range(self._len):
                i = self._brick[j]
                if i.isVisible():
                    if i.collideBall(ball, self) and self.bricks_pos[j][3] != 0:
                        ball_vel = ball.getVelocity()
                        self.powerup[self.bricks_pos[j][4]].release(np.array([ball_vel[0], ball_vel[1]], dtype='float'))
        
        for beam in self.laserbeams:
            for j in range(self._len):
                i = self._brick[j]
                
                if i.isVisible() and beam.isVisible():
                    if i.collideBall(beam, self) and self.bricks_pos[j][3] != 0:
                        self.powerup[self.bricks_pos[j][4]].release(np.array([1,0], dtype='float'))
        
        if self._isUfo:
            self._ufo.collideBall(ball, self)

    def explodeBricks(self, pos, size):
        threading.Thread(target=playsound, args=('explosion.wav',), daemon=True).start()
        for j in range(self._len):
            i = self._brick[j]
            if i.isVisible():
                x2, y2 = i.getPosition()

                if ((x2 == pos[0] or x2 == pos[0] + size[0] - 1 or x2 + size[0] - 1 == pos[0]) and (pos[1] <= y2 <= pos[1] + size[1] or pos[1] <= y2 + size[1] - 1 <= pos[1] + size[1])) or ((y2 == pos[1] or y2 == pos[1] + size[1] - 1 or y2 + size[1] - 1 == pos[1]) and (pos[0] <= x2 <= pos[0] + size[0] or pos[0] <= x2 + size[0] - 1 <= pos[0] + size[0])):
                    i.explodeBrick(self)     
                    if self.bricks_pos[j][3]!=0:
                        self.powerup[self.bricks_pos[j][4]].release(np.array([1, 1], dtype='float')) 
                

    def handleCollisionBallPaddle(self):

        collide = False
        
                    
        for i in self._ball:
            x1, y1 = i.getPosition()
            x2, y2 = self._paddle.getPosition()
            _, w = self._paddle.getSize()

            if x1==x2-1 and y2 <= y1 <= y2+w:
                speed = y1 - y2 - w/2
                if not i.isStuckPaddle():
                    collide = True
                    threading.Thread(target=playsound, args=('ball.wav',), daemon=True).start()
                    
                i.collidePaddle(speed/2)
        
        for i in self._bombs:
            if i.isVisible():
                x1, y1 = i.getPosition()
                x2,y2 = self._paddle.getPosition()
                _, w = self._paddle.getSize()

                if x1 == x2 and y2 <= y1 <= y2+w:
                    i.makeInvisible()
                    self.decreaseLives()
                

        if(collide and self._move):
            self.moveBricks()

    def handleInput(self, ch):
        if ch == 'q':
            raise SystemExit
        if ch == 's':
            for i in self._ball:
                i.release()    
        if ch == 'l':
            self.nextLevel()
        self._paddle.move(ch, self._ball)
        if self._isUfo:
            pos = self._paddle.getPosition()
            size = self._paddle.getSize()
            self._ufo.setPosition(np.array([2, pos[1] + (size[1]/2)]))
