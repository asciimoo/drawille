DRAWILLE
========


Drawing in terminal with Unicode [Braille][] characters

[Braille]: http://en.wikipedia.org/wiki/Braille

![Drawille](docs/images/drawille_01.png)

![Drawille](docs/images/xkcd.png)

![Drawille](docs/images/sine_tracking.gif)

![Drawille](docs/images/rotating_cube.gif)


### USAGE

```python
from __future__ import print_function
from drawille import Canvas
from math import sin, radians

c = Canvas()

for x in range(0, 1800, 10):
    c.set(x / 10, 10 + sin(radians(x)) * 10)

print(c.frame())
```

![Usage](docs/images/usage.png)


### Bugs

Bugs or suggestions? Visit the [issue tracker](https://github.com/asciimoo/drawille/issues).

(Tested only with `urxvt` terminal and `fixed` font.)

### LICENSE

```
drawille is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

drawille is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with drawille. If not, see < http://www.gnu.org/licenses/ >.

(C) 2014- by Adam Tauber, <asciimoo@gmail.com>
```
