from __future__ import print_function
from drawille import Canvas, line
import math
from time import sleep
c = Canvas()
i = 0
height = 40
while True:
    for x,y in line(0, height, 180, int(math.sin(math.radians(i))*height + height)):
        c.set(x,y)
    for x in range(0, 360, 2):
        coords = (x/2, height + int(round(math.sin(math.radians(x+i)) * height)))
        c.set(*coords)
    print("\x1b[2J\x1b[H" + c.frame())
    i += 2
    sleep(1.0/24)
    c.clear()
