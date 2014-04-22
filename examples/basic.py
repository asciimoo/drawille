from drawille import Canvas
import math
s = Canvas()
for x in range(1800):
    coords = (x/10, math.sin(math.radians(x)) * 10)
    s.set(*coords)
print s.frame()
s.clear()
for x in range(0, 1800, 10):
    coords = (x/10, 10 + math.sin(math.radians(x)) * 10)
    s.set(*coords)
    coords = (x/10, 10 + math.cos(math.radians(x)) * 10)
    s.set(*coords)
print s.frame()
s.clear()
for x in range(0, 3600, 20):
    coords = (x/20, 4 + math.sin(math.radians(x)) * 4)
    s.set(*coords)
print s.frame()
s.clear()
for x in range(0, 360, 4):
    coords = (x/4, 30 + math.sin(math.radians(x)) * 30)
    s.set(*coords)
for x in range(30):
    for y in range(30):
        s.set(x,y)
        s.toggle(x+30, y+30)
        s.toggle(x+60, y)
print s.frame()
