import sys
import numpy as np
from colorama import Fore, Back, Style, init
from art import *
import time

init()

import config

class Screen:

    def __init__(self):
        self._width  = config.WIDTH
        self._height = config.HEIGHT

    def clear(self):

        self.displayDynamic = np.full((self._height, self._width), '')
        self.displayStatic = np.full((self._height, self._width), ' ')
        self.displayColor = np.full((self._height, self._width), '', dtype=object)

    def drawBackGround(self):
        self.displayStatic[0,:] = np.full((1,self._width), "_")   
        self.displayStatic[:,0] = np.full((self._height), "|" )
        self.displayStatic[:,self._width-1] = np.full((self._height), "|")  
            
    def drawObject(self, obj):
        
        _x, _y = obj.getPosition()
        _h, _w = obj.getSize()
        _rep = obj.getRep()
        col = obj.getColor()

        _x = int(_x)
        _y = int(_y)
        _h = int(_h)
        _w = int(_w)

        self.displayDynamic[_x: _x + _h, _y: _y + _w] = _rep
        self.displayColor[_x: _x + _h, _y: _y + _w] = col
        self.displayStatic[_x: _x + _h, _y: _y + _w] = np.full((_h, _w), '')

    def gameOver(self, win):

        arr,col = getGameOver(win)

        print("\033[2J", end='')
        print(config.CURSOR_0, end='')

        for i in range(arr.shape[0]):
            for j in arr[i]:
                print(j+col, end='')
            print('')

        print(Style.RESET_ALL)
        time.sleep(1)

    def flash(self):

        out = ""
        print(config.CURSOR_0, end='')
        for _ in range(self._height):
            for _ in range(self._width):
                out += " "
            out += "\n"
        
        sys.stdout.write(out + Style.RESET_ALL)
        time.sleep(0.2)

    def printScreen(self):

        out = ""
        print(config.CURSOR_0, end='')
        for i in range(self._height):
            for j in range(self._width):
                out += (self.displayColor[i][j] +(self.displayStatic[i][j] + self.displayDynamic[i][j]) + Style.RESET_ALL)
            out += "\n"
        
        sys.stdout.write(out + Style.RESET_ALL)
