import os
import colorama

CURSOR_0 = "\033[0;0H"

SCREEN_HEIGHT, SCREEN_WIDTH = os.popen("stty size", "r").read().split()

HEIGHT = int(SCREEN_HEIGHT) - 2
WIDTH  = int(SCREEN_WIDTH) - 5

DELAY = 0.05