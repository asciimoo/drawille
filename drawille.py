# -*- coding: utf-8 -*-

# drawille is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# drawille is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with drawille. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2014- by Adam Tauber, <asciimoo@gmail.com>

from collections import defaultdict
import math
from sys import version_info

IS_PY3 = version_info[0] == 3

if IS_PY3:
    unichr = chr

"""

http://www.alanwood.net/unicode/braille_patterns.html

dots:
   ,___,
   |1 4|
   |2 5|
   |3 6|
   |7 8|
   `````
"""

pixel_map = ((0x01, 0x08),
             (0x02, 0x10),
             (0x04, 0x20),
             (0x40, 0x80))

# braille unicode characters starts at 0x2800
braille_char_offset = 0x2800


# http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
def getTerminalSize():
    """Returns terminal width, height
    """
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass

    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

    return int(cr[1]), int(cr[0])


def normalize(coord):
    coord_type = type(coord)

    if coord_type == int:
        return coord

    elif coord_type == float:
        return int(round(coord))


def intdefaultdict():
    return defaultdict(int)


class Canvas(object):
    """This class implements the pixel surface """
    def __init__(self, line_ending='\n'):
        super(Canvas, self).__init__()
        self.clear()
        self.line_ending = line_ending

    def clear(self):
        """Remove all pixels from the :class:`Canvas` object."""
        self.chars = defaultdict(intdefaultdict)

    def _get_pos(self, x, y):
        """Convert x, y to cols, rows"""
        x = normalize(x)
        y = normalize(y)
        cols = x // 2
        rows = y // 4
        return x, y, cols, rows

    def set(self, x, y):
        """Set a pixel of the :class:`Canvas` object.

        :param x: x coordinate of the pixel
        :param y: y coordinate of the pixel
        """
        x, y, px, py = self._get_pos(x, y)
        if type(self.chars[py][px]) != int:
            return
        self.chars[py][px] |= pixel_map[y % 4][x % 2]

    def unset(self, x, y):
        """Unset a pixel of the :class:`Canvas` object.

        :param x: x coordinate of the pixel
        :param y: y coordinate of the pixel
        """
        x, y, px, py = self._get_pos(x, y)
        if type(self.chars[py][px]) == int:
            self.chars[py][px] &= ~pixel_map[y % 4][x % 2]
        if type(self.chars[py][px]) != int or self.chars[py][px] == 0:
            del(self.chars[py][px])
        if not self.chars.get(py):
            del(self.chars[py])

    def toggle(self, x, y):
        """Toggle a pixel of the :class:`Canvas` object.

        :param x: x coordinate of the pixel
        :param y: y coordinate of the pixel
        """
        x, y, px, py = self._get_pos(x, y)
        if type(self.chars[py][px]) != int or self.chars[py][px] & pixel_map[y % 4][x % 2]:
            self.unset(x, y)
        else:
            self.set(x, y)

    def set_text(self, x, y, text):
        """Set text to the given coords.

        :param x: x coordinate of the text start position
        :param y: y coordinate of the text start position
        """
        x = normalize(x / 2)
        y = normalize(y / 4)
        for i,c in enumerate(text):
            self.chars[y][x+i] = c

    def get(self, x, y):
        """Get the state of a pixel. Returns bool.

        :param x: x coordinate of the pixel
        :param y: y coordinate of the pixel
        """
        dot_index = pixel_map[y % 4][x % 2]
        x = normalize(x / 2)
        y = normalize(y / 4)
        char = self.chars.get(y, {}).get(x)

        if not char:
            return False

        if type(char) != int:
            return True

        return bool(char & dot_index)

    def rows(self, min_x=None, min_y=None, max_x=None, max_y=None):
        """Returns a list of the current :class:`Canvas` object lines.

        :param min_x: (optional) minimum x coordinate of the canvas
        :param min_y: (optional) minimum y coordinate of the canvas
        :param max_x: (optional) maximum x coordinate of the canvas
        :param max_y: (optional) maximum y coordinate of the canvas
        """

        if not self.chars.keys():
            return []

        minrow = min_y // 4 if min_y != None else min(self.chars.keys())
        maxrow = (max_y - 1) // 4 if max_y != None else max(self.chars.keys())
        mincol = min_x // 2 if min_x != None else min(min(x.keys()) for x in self.chars.values())
        maxcol = (max_x - 1) // 2 if max_x != None else max(max(x.keys()) for x in self.chars.values())
        ret = []

        for rownum in range(minrow, maxrow+1):
            if not rownum in self.chars:
                ret.append('')
                continue

            maxcol = (max_x - 1) // 2 if max_x != None else max(self.chars[rownum].keys())
            row = []

            for x in  range(mincol, maxcol+1):
                char = self.chars[rownum].get(x)

                if not char:
                    row.append(' ')
                elif type(char) != int:
                    row.append(char)
                else:
                    row.append(unichr(braille_char_offset+char))

            ret.append(''.join(row))

        return ret

    def frame(self, min_x=None, min_y=None, max_x=None, max_y=None):
        """String representation of the current :class:`Canvas` object pixels.

        :param min_x: (optional) minimum x coordinate of the canvas
        :param min_y: (optional) minimum y coordinate of the canvas
        :param max_x: (optional) maximum x coordinate of the canvas
        :param max_y: (optional) maximum y coordinate of the canvas
        """
        ret = self.line_ending.join(self.rows(min_x, min_y, max_x, max_y))

        if IS_PY3:
            return ret

        return ret.encode('utf-8')


def line(x1, y1, x2, y2):

    x1 = normalize(x1)
    y1 = normalize(y1)
    x2 = normalize(x2)
    y2 = normalize(y2)

    xdiff = max(x1, x2) - min(x1, x2)
    ydiff = max(y1, y2) - min(y1, y2)
    xdir = 1 if x1 <= x2 else -1
    ydir = 1 if y1 <= y2 else -1

    r = max(xdiff, ydiff)

    for i in range(r+1):
        x = x1
        y = y1

        if ydiff:
            y += (float(i)*ydiff)/r*ydir
        if xdiff:
            x += (float(i)*xdiff)/r*xdir

        yield (x, y)


def polygon(center_x=0, center_y=0, sides=4, radius=4):
    degree = float(360)/sides

    for n in range(sides):
        a = n*degree
        b = (n+1)*degree
        x1 = (center_x+math.cos(math.radians(a)))*(radius+1)/2
        y1 = (center_x+math.sin(math.radians(a)))*(radius+1)/2
        x2 = (center_x+math.cos(math.radians(b)))*(radius+1)/2
        y2 = (center_x+math.sin(math.radians(b)))*(radius+1)/2

        for x,y in line(x1,y1,x2,y2):
            yield x,y
