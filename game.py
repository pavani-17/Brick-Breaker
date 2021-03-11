import os
import sys
import numpy as np
import time

import config
from screen import Screen
from paddle import Paddle
from input import input_to, Get
from ball import Ball
from brick import Breakable, Brick, ExplodingBrick
from powerup import FastBall, LongPaddlePowerup, ShortPaddlePowerup, StickBall, ThruBall, MultiplyBall

class Game:

    def start(self):
        if config.HEIGHT < 41 or config.WIDTH < 168:
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
        self._start_time = time.time()
        self._printscore = 0
        get = Get()
        self.bricks_pos = np.array([
           [21, 66, 2, 2, 0], [21, 75,3, 1, 1], [21, 84, 1, 3, 2], 
           [19,70,2,4,3], [19,79,2,5,4],[19,88,3,6,5], [19, 61,3,2,6],
           [17,75,-1, 0,0], [17,84,-1, 0,0], [17,66,-1, 0,0], [17, 93, -1, 0 ,0], [17, 57, -1, 0, 0], [17,48,-1,0,0], [17,102,-1,0,0],
           [15, 79, 1, 1, 7], [15, 70, 1, 3, 8], [15,88,0,2,9], [15, 61,0,6,10],
           [13, 75, 1, 4, 11], [13, 66, 2, 5, 12], [13, 84, 3, 6, 13], 
           [8,14,0,0,0], [8,23,1,1,14], [8, 32, 0, 0,0], [6, 23, 2, 4,15], [4,14,0,0,0], [4,23,1,2,16], [4, 32, 0, 0,0],
           [8,127,0,0,0], [8,136,1,3,17], [8,145,0,0,0],[6,136,2,5,18],[4,127,0,0,0], [4,136,1,6,19], [4,145,0,0,0], 
           
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
            time_temp = int(time.time() - self._start_time)
            self._printscore = int(self._score + max(0, (1000 - time_temp)/100))
            print("Lives ", self._lives, "   Score ", self._printscore, "   Time ", time_temp)

    def moveBalls(self):
        for i in self._ball:
            if i.move():
                self._ball.remove(i)
                self._balls = self._balls - 1

        if self._balls == 0:
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
                    
            self._balls = 1
            x, y = self._paddle.getPosition()
            _, w = self._paddle.getSize()
            self._ball.append(Ball(np.array([x-1, y + w/2]), np.array([-1, 0]), True))

    def drawBalls(self):
        for i in self._ball:
            self._screen.drawObject(i)

    def createBricks(self):
        self._brick = []
        for i in self.bricks_pos:
            if(i[2] == 0):
                temp = Brick(np.array([i[0], i[1]]))
                self._brick.append(temp)

            elif i[2] == -1:
                temp = ExplodingBrick(np.array([i[0], i[1]]))
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
        
        gameOver = True
        for i in self._brick:
            if i.isVisible():
                self._screen.drawObject(i)
                if i.getType() != 0:
                    gameOver = False

        if gameOver == True:
            time_temp = int(time.time() - self._start_time)
            self._screen.gameOver(win=True, score=(self._score + max(0, (1000 - time_temp)/100)))
            quit()

        for i in self.powerup:
            if i.isVisible():
                i.move(self._paddle)
                p = i.getType()
                if p == 'F' or p == 'B' or p == 'T':
                    i.activate(self._ball)
                    i.setTime(time.time() + 50)
                elif p == 'L' or p == 'S':
                    i.activate(self)
                    i.setTime(time.time() + 50)
                elif p == 'M':
                    i.activate(self, len(self._ball))
                    i.setTime(time.time() + 50)

                self._screen.drawObject(i)
            if i.isActivated() and i.getTime() < time.time():
                p = i.getType()
                if p == 'F' or p == 'B' or p == 'T':
                    i.deactivate(self._ball)
                elif p == 'L' or p == 'S' or p == 'M':
                    i.deactivate(self)


    def changeLongPaddle(self):
        x, y = self._paddle.getPosition()
        _, w = self._paddle.getSize()
        
        self._paddle = Paddle(np.array([x,y]), np.array([1, w+3]))

    def changeShortPaddle(self):
        x, y = self._paddle.getPosition()
        _, w = self._paddle.getSize()
        
        if (w>8):
            self._paddle = Paddle(np.array([x,y]), np.array([1, w-3]))

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
                        self.powerup[self.bricks_pos[j][4]].release()

    def explodeBricks(self, pos, size):
        for j in range(self._len):
            i = self._brick[j]
            if i.isVisible():
                x2, y2 = i.getPosition()

                if ((x2 == pos[0] or x2 == pos[0] + size[0] - 1 or x2 + size[0] - 1 == pos[0]) and (pos[1] <= y2 <= pos[1] + size[1] or pos[1] <= y2 + size[1] - 1 <= pos[1] + size[1])) or ((y2 == pos[1] or y2 == pos[1] + size[1] - 1 or y2 + size[1] - 1 == pos[1]) and (pos[0] <= x2 <= pos[0] + size[0] or pos[0] <= x2 + size[0] - 1 <= pos[0] + size[0])):
                    i.explodeBrick(self)     
                    if self.bricks_pos[j][3]!=0:
                        self.powerup[self.bricks_pos[j][4]].release() 
                          


                

    def handleCollisionBallPaddle(self):

        for i in self._ball:
            x1, y1 = i.getPosition()
            x2, y2 = self._paddle.getPosition()
            _, w = self._paddle.getSize()

            if x1==x2-1 and y2 <= y1 <= y2+w:
                speed = y1 - y2 - w/2
                i.collidePaddle(speed/2)

    def handleInput(self, ch):
        if ch == 'q':
            raise SystemExit
        if ch == 's':
            for i in self._ball:
                i.release()    
        self._paddle.move(ch, self._ball)
