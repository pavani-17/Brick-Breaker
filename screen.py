import sys
import numpy as np
import colorama as col

import config

class Screen:

    def __init__(self):
        self._width  = config.WIDTH
        self._height = config.HEIGHT

    def clear(self):

        self.displayDynamic = np.full((self._height, self._width), '')
        self.displayStatic = np.full((self._height, self._width), ' ')

    def drawBackGround(self):
        self.displayStatic[0,:] = np.full((1,self._width), "_")   
        self.displayStatic[:,0] = np.full((self._height), "|")
        self.displayStatic[:,self._width-1] = np.full((self._height), "|")  
            
    def drawObject(self, obj):
        
        _x, _y = obj.getPosition()
        _h, _w = obj.getSize()
        _rep = obj.getRep()

        _x = int(_x)
        _y = int(_y)
        _h = int(_h)
        _w = int(_w)

        self.displayDynamic[_x: _x + _h, _y: _y + _w] = _rep
        self.displayStatic[_x: _x + _h, _y: _y + _w] = np.full((_h, _w), '')

    def printScreen(self):

        out = ""
        print(config.CURSOR_0, end='')
        for i in range(self._height):
            for j in range(self._width):
                out += (self.displayStatic[i][j] + self.displayDynamic[i][j])
            out += "\n"
        
        sys.stdout.write(out)
