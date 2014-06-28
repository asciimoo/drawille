from __future__ import print_function
from drawille import Canvas, line, animate
import math

def __main__():
    i = 0
    height = 40

    while True:
        frame = []
        for x,y in line(0, height, 180, math.sin(math.radians(i)) * height + height):
            frame.append((x,y))

        for x in range(0, 360, 2):
            coords = (x/2, height + math.sin(math.radians(x+i)) * height)
            frame.append((coords[0], coords[1]))

        yield frame

        i += 2



if __name__ == '__main__':
    c = Canvas()
    animate(c, __main__, 1./60)
