from __future__ import print_function
from drawille import Canvas, line
import math
from time import sleep
import curses
import locale

locale.setlocale(locale.LC_ALL,"")

stdscr = curses.initscr()
stdscr.refresh()


def __main__(stdscr):
    i = 0
    c = Canvas()
    height = 40
    while True:

        for x,y in line(0, height, 180, int(math.sin(math.radians(i)) * height + height)):
            c.set(x,y)

        for x in range(0, 360, 2):
            coords = (x/2, height + int(round(math.sin(math.radians(x+i)) * height)))
            c.set(*coords)

        f = c.frame()+'\n'
        stdscr.addstr(0, 0, f)
        stdscr.refresh()

        i += 2
        sleep(1.0/24)
        c.clear()


if __name__ == '__main__':
    curses.wrapper(__main__)
