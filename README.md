DRAWILLE
========


Drawing in terminal with unicode braille characters

![Drawille](https://raw.github.com/asciimoo/drawille/master/docs/drawille_01.png)


### USAGE

```python
from drawille import Canvas
from math import sin, radians

c = Canvas()

for x in range(0, 1800, 10):
    c.set(x / 10, 10 + sin(radians(x)) * 10)

print s.frame()
```


### Bugs

Bugs or suggestions? Visit the [issue tracker](https://github.com/asciimoo/drawille/issues).

(Tested only with `urxvt` terminal and `fixed` font.)
