import numpy as np
from colorama import Fore, Back

def getGameOver(win):

    arr = []

    with open('gameover.txt','r') as f:
        for line in f:
            arr.append(list(line.strip('\n')))

    if win == True:
        with open('win.txt','r') as f:
            for line in f:
                arr.append(list(line.strip('\n')))

        color = Fore.GREEN

    else:
        with open('lose.txt','r') as f:
            for line in f:
                arr.append(list(line.strip('\n')))

        color = Fore.RED

    return np.array(arr, dtype=object), color

def getUfo():
    arr = []

    with open('ufo.txt','r') as f:
        for line in f:
            arr.append(list(line.strip('\n')))
    return np.array(arr,dtype=object)

