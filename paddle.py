import numpy as np
import config
from colorama import Fore, Back, Style

from object import Object   

class Paddle(Object):

    def __init__(self, pos, size, shoots=False):
        super().__init__(pos, size)
        self._vel = np.array([0,0])
        self._shoots = shoots

        list = []
        
        for i in range(self._size[1]):
            if i==0:
                list.append('(')
            elif i == (self._size[1]-1):
                list.append(')')
            else:
                list.append('I')
        
        self._rep = np.array([])

        self._rep = np.append(self._rep, np.array(list), axis=0)
        
        self.addShoots()

    def in_child(self, pos, size):
        super().__init__(pos, size)
        self._vel = np.array([0,0])

    def move(self,key, ball):
        if key == 'a':
            self._pos[1] = self._pos[1] - 2
            for i in ball:
                i.moveWithPaddle(-2)
            self.handle()
        
        elif key == 'd':
            self._pos[1] = self._pos[1] + 2
            for i in ball:
                i.moveWithPaddle(+2)
            self.handle()

    def addShoots(self):

        if self._shoots:
            list = []
        
            for i in range(self._size[1]):
                if i==0:
                    list.append('(')
                elif i == 1:
                    list.append('V')
                elif i == (self._size[1]-1):
                    list.append(')')
                elif i == (self._size[1]-2):
                    list.append('V')
                else:
                    list.append('I')
            
            self._rep = np.array([])

            self._rep = np.append(self._rep, np.array(list), axis=0)

    def activateShoots(self):
        self._shoots = True
        self.addShoots()

    def deactivateShoots(self):
        self._shoots = False
        list = []
        
        for i in range(self._size[1]):
            if i==0:
                list.append('(')
            elif i == (self._size[1]-1):
                list.append(')')
            else:
                list.append('I')
        
        self._rep = np.array([])

        self._rep = np.append(self._rep, np.array(list), axis=0)

    def isShoots(self):
        return self._shoots






        
