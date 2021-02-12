import os
import sys
import numpy as np
import time

import config
from screen import Screen
from paddle import Paddle, LongPaddle, ShortPaddle
from input import input_to, Get
from ball import Ball
from brick import Breakable, Brick
from powerup import FastBall, LongPaddlePowerup, ShortPaddlePowerup, StickBall, ThruBall, MultiplyBall

class Game:

    def start(self):
        print("\033[?25l\033[2J", end='')
        self._screen = Screen()        
        self._paddle = Paddle(np.array([config.HEIGHT-3, config.WIDTH/2 - 7]))
        self._ball = []
        self._ball.append(Ball(np.array([config.HEIGHT-3, config.WIDTH/2]), np.array([-1, 0]), True))
        self._lives = 5
        self._balls = 1
        self._score = 0
        self._start_time = time.time()
        get = Get()
        self.bricks_pos = np.array([
           [17,75,1, 6,0], [15, 79, 0, 0, 0], [15, 70, 3, 0, 0], [13, 75, 2, 0, 0], [13, 66, 1, 0, 0], [13, 84, 1, 0, 0], [11, 79, 2, 0, 0], [11, 70, 2, 0, 0], [11, 61, 3, 0, 0], [11, 88, 3, 0, 0], 
        ])
        self.powerup = []
        self._len = self.bricks_pos.shape[0]
        self.createBricks()
        
        while True:
            self._screen.clear()
            self._screen.drawBackGround()
            inchar = input_to(get.__call__)
            self.handleInput(inchar)
            self.moveBalls()
            self._screen.drawObject(self._paddle)
            self.drawBricks()
            self.handleCollisionBallPaddle() 
            self.handleCollisionBallBrick()     
            self.drawBalls()
            self._screen.printScreen()
            print("Lives ", self._lives, "   Score ", self._score, "   Time ", time.time() - self._start_time)

    def moveBalls(self):
        for i in self._ball:
            if i.move():
                self._ball.remove(i)
                self._balls = self._balls - 1

        if self._balls == 0:
            self._lives = self._lives - 1
            self._balls = 1
            x, y = self._paddle.getPosition()
            _, w = self._paddle.getSize()
            self._ball.append(Ball(np.array([x, y + w/2]), np.array([-1, 0]), True))

    def drawBalls(self):
        for i in self._ball:
            self._screen.drawObject(i)

    def createBricks(self):
        self._brick = []
        for i in self.bricks_pos:
            if(i[2] == 0):
                temp = Brick(np.array([i[0], i[1]]))
                self._brick.append(temp)
            
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
                    
                    self.powerup.append(temp1)


        self._brick = np.array(self._brick)

    def drawBricks(self):
        
        for i in self._brick:
            if i.isVisible():
                self._screen.drawObject(i)

        for i in self.powerup:
            if i.isVisible():
                i.move(self._paddle)
                p = i.getType()
                if p == 'F' or p == 'B' or p == 'T':
                    i.activate(self._ball)
                    i.setTime(time.time() + 10)
                elif p == 'L' or p == 'S':
                    i.activate(self)
                    i.setTime(time.time() + 10)
                elif p == 'M':
                    i.activate(self, len(self._ball))
                    i.setTime(time.time() + 5)

                self._screen.drawObject(i)
            if i.isActivated() and i.getTime() < time.time():
                p = i.getType()
                if p == 'F' or p == 'B' or p == 'T':
                    i.deactivate(self._ball)
                elif p == 'L' or p == 'S' or p == 'M':
                    i.deactivate(self)


    def changeLongPaddle(self):
        x, y = self._paddle.getPosition()
        self._paddle = LongPaddle(np.array([x,y]))

    def changeShortPaddle(self):
        x, y = self._paddle.getPosition()
        self._paddle = ShortPaddle(np.array([x,y]))

    def changeNormalPaddle(self):
        x, y = self._paddle.getPosition()
        self._paddle = Paddle(np.array([x,y]))

    def multiplyBalls(self):
        length = len(self._ball)
        for j in range(length):
            i = self._ball[j]
            vx, vy = i.getVelocity()
            x, y = i.getPosition()
            self._balls += 1
            self._ball.append(Ball(np.array([x, y+10]), np.array([vx, -vy]), False))   

    def decreaseBalls(self, balls):
        length = len(self._ball)

        while(length > balls):
            self._ball.pop()
            length = length - 1
            self._balls = self._balls - 1


    def incrementScore(self,val):
        self._score = self._score + val         

    def handleCollisionBallBrick(self):

        for ball in self._ball:
            for j in range(self._len):
                i = self._brick[j]
                if i.isVisible():
                    if i.collideBall(ball, self) and self.bricks_pos[j][3] != 0:
                        self.powerup[self.bricks_pos[j][4]].release()

    def handleCollisionBallPaddle(self):

        for i in self._ball:
            x1, y1 = i.getPosition()
            x2, y2 = self._paddle.getPosition()
            _, w = self._paddle.getSize()

            if x1==x2 and y2 <= y1 <= y2+w:
                speed = y1 - y2 - w/2
                i.collidePaddle(speed/2)

    def handleInput(self, ch):
        if ch == 'q':
            raise SystemExit
        if ch == 's':
            for i in self._ball:
                i.release()    
        self._paddle.move(ch, self._ball)

Game().start()

    


    