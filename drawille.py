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
from operator import or_
import math
from sys import version_info
IS_PY3 = version_info[0] == 3

if IS_PY3:
    from functools import reduce

"""

source: http://www.alanwood.net/unicode/braille_patterns.html

dots:
   ,___,
   |1 4|
   |2 5|
   |3 6|
   |7 8|
   `````
"""

pixel_map = ((0b00000001, 0b00001000),
             (0b00000010, 0b00010000),
             (0b00000100, 0b00100000),
             (0b01000000, 0b10000000))

braille_map = {
    0b00000000 : '⠀',
    0b00000001 : '⠁',
    0b00000010 : '⠂',
    0b00000011 : '⠃',
    0b00000100 : '⠄',
    0b00000101 : '⠅',
    0b00000110 : '⠆',
    0b00000111 : '⠇',
    0b00001000 : '⠈',
    0b00001001 : '⠉',
    0b00001010 : '⠊',
    0b00001011 : '⠋',
    0b00001100 : '⠌',
    0b00001101 : '⠍',
    0b00001110 : '⠎',
    0b00001111 : '⠏',
    0b00010000 : '⠐',
    0b00010001 : '⠑',
    0b00010010 : '⠒',
    0b00010011 : '⠓',
    0b00010100 : '⠔',
    0b00010101 : '⠕',
    0b00010110 : '⠖',
    0b00010111 : '⠗',
    0b00011000 : '⠘',
    0b00011001 : '⠙',
    0b00011010 : '⠚',
    0b00011011 : '⠛',
    0b00011100 : '⠜',
    0b00011101 : '⠝',
    0b00011110 : '⠞',
    0b00011111 : '⠟',
    0b00100000 : '⠠',
    0b00100001 : '⠡',
    0b00100010 : '⠢',
    0b00100011 : '⠣',
    0b00100100 : '⠤',
    0b00100101 : '⠥',
    0b00100110 : '⠦',
    0b00100111 : '⠧',
    0b00101000 : '⠨',
    0b00101001 : '⠩',
    0b00101010 : '⠪',
    0b00101011 : '⠫',
    0b00101100 : '⠬',
    0b00101101 : '⠭',
    0b00101110 : '⠮',
    0b00101111 : '⠯',
    0b00110000 : '⠰',
    0b00110001 : '⠱',
    0b00110010 : '⠲',
    0b00110011 : '⠳',
    0b00110100 : '⠴',
    0b00110101 : '⠵',
    0b00110110 : '⠶',
    0b00110111 : '⠷',
    0b00111000 : '⠸',
    0b00111001 : '⠹',
    0b00111010 : '⠺',
    0b00111011 : '⠻',
    0b00111100 : '⠼',
    0b00111101 : '⠽',
    0b00111110 : '⠾',
    0b00111111 : '⠿',
    0b01000000 : '⡀',
    0b01000001 : '⡁',
    0b01000010 : '⡂',
    0b01000011 : '⡃',
    0b01000100 : '⡄',
    0b01000101 : '⡅',
    0b01000110 : '⡆',
    0b01000111 : '⡇',
    0b01001000 : '⡈',
    0b01001001 : '⡉',
    0b01001010 : '⡊',
    0b01001011 : '⡋',
    0b01001100 : '⡌',
    0b01001101 : '⡍',
    0b01001110 : '⡎',
    0b01001111 : '⡏',
    0b01010000 : '⡐',
    0b01010001 : '⡑',
    0b01010010 : '⡒',
    0b01010011 : '⡓',
    0b01010100 : '⡔',
    0b01010101 : '⡕',
    0b01010110 : '⡖',
    0b01010111 : '⡗',
    0b01011000 : '⡘',
    0b01011001 : '⡙',
    0b01011010 : '⡚',
    0b01011011 : '⡛',
    0b01011100 : '⡜',
    0b01011101 : '⡝',
    0b01011110 : '⡞',
    0b01011111 : '⡟',
    0b01100000 : '⡠',
    0b01100001 : '⡡',
    0b01100010 : '⡢',
    0b01100011 : '⡣',
    0b01100100 : '⡤',
    0b01100101 : '⡥',
    0b01100110 : '⡦',
    0b01100111 : '⡧',
    0b01101000 : '⡨',
    0b01101001 : '⡩',
    0b01101010 : '⡪',
    0b01101011 : '⡫',
    0b01101100 : '⡬',
    0b01101101 : '⡭',
    0b01101110 : '⡮',
    0b01101111 : '⡯',
    0b01110000 : '⡰',
    0b01110001 : '⡱',
    0b01110010 : '⡲',
    0b01110011 : '⡳',
    0b01110100 : '⡴',
    0b01110101 : '⡵',
    0b01110110 : '⡶',
    0b01110111 : '⡷',
    0b01111000 : '⡸',
    0b01111001 : '⡹',
    0b01111010 : '⡺',
    0b01111011 : '⡻',
    0b01111100 : '⡼',
    0b01111101 : '⡽',
    0b01111110 : '⡾',
    0b01111111 : '⡿',
    0b10000000 : '⢀',
    0b10000001 : '⢁',
    0b10000010 : '⢂',
    0b10000011 : '⢃',
    0b10000100 : '⢄',
    0b10000101 : '⢅',
    0b10000110 : '⢆',
    0b10000111 : '⢇',
    0b10001000 : '⢈',
    0b10001001 : '⢉',
    0b10001010 : '⢊',
    0b10001011 : '⢋',
    0b10001100 : '⢌',
    0b10001101 : '⢍',
    0b10001110 : '⢎',
    0b10001111 : '⢏',
    0b10010000 : '⢐',
    0b10010001 : '⢑',
    0b10010010 : '⢒',
    0b10010011 : '⢓',
    0b10010100 : '⢔',
    0b10010101 : '⢕',
    0b10010110 : '⢖',
    0b10010111 : '⢗',
    0b10011000 : '⢘',
    0b10011001 : '⢙',
    0b10011010 : '⢚',
    0b10011011 : '⢛',
    0b10011100 : '⢜',
    0b10011101 : '⢝',
    0b10011110 : '⢞',
    0b10011111 : '⢟',
    0b10100000 : '⢠',
    0b10100001 : '⢡',
    0b10100010 : '⢢',
    0b10100011 : '⢣',
    0b10100100 : '⢤',
    0b10100101 : '⢥',
    0b10100110 : '⢦',
    0b10100111 : '⢧',
    0b10101000 : '⢨',
    0b10101001 : '⢩',
    0b10101010 : '⢪',
    0b10101011 : '⢫',
    0b10101100 : '⢬',
    0b10101101 : '⢭',
    0b10101110 : '⢮',
    0b10101111 : '⢯',
    0b10110000 : '⢰',
    0b10110001 : '⢱',
    0b10110010 : '⢲',
    0b10110011 : '⢳',
    0b10110100 : '⢴',
    0b10110101 : '⢵',
    0b10110110 : '⢶',
    0b10110111 : '⢷',
    0b10111000 : '⢸',
    0b10111001 : '⢹',
    0b10111010 : '⢺',
    0b10111011 : '⢻',
    0b10111100 : '⢼',
    0b10111101 : '⢽',
    0b10111110 : '⢾',
    0b10111111 : '⢿',
    0b11000000 : '⣀',
    0b11000001 : '⣁',
    0b11000010 : '⣂',
    0b11000011 : '⣃',
    0b11000100 : '⣄',
    0b11000101 : '⣅',
    0b11000110 : '⣆',
    0b11000111 : '⣇',
    0b11001000 : '⣈',
    0b11001001 : '⣉',
    0b11001010 : '⣊',
    0b11001011 : '⣋',
    0b11001100 : '⣌',
    0b11001101 : '⣍',
    0b11001110 : '⣎',
    0b11001111 : '⣏',
    0b11010000 : '⣐',
    0b11010001 : '⣑',
    0b11010010 : '⣒',
    0b11010011 : '⣓',
    0b11010100 : '⣔',
    0b11010101 : '⣕',
    0b11010110 : '⣖',
    0b11010111 : '⣗',
    0b11011000 : '⣘',
    0b11011001 : '⣙',
    0b11011010 : '⣚',
    0b11011011 : '⣛',
    0b11011100 : '⣜',
    0b11011101 : '⣝',
    0b11011110 : '⣞',
    0b11011111 : '⣟',
    0b11100000 : '⣠',
    0b11100001 : '⣡',
    0b11100010 : '⣢',
    0b11100011 : '⣣',
    0b11100100 : '⣤',
    0b11100101 : '⣥',
    0b11100110 : '⣦',
    0b11100111 : '⣧',
    0b11101000 : '⣨',
    0b11101001 : '⣩',
    0b11101010 : '⣪',
    0b11101011 : '⣫',
    0b11101100 : '⣬',
    0b11101101 : '⣭',
    0b11101110 : '⣮',
    0b11101111 : '⣯',
    0b11110000 : '⣰',
    0b11110001 : '⣱',
    0b11110010 : '⣲',
    0b11110011 : '⣳',
    0b11110100 : '⣴',
    0b11110101 : '⣵',
    0b11110110 : '⣶',
    0b11110111 : '⣷',
    0b11111000 : '⣸',
    0b11111001 : '⣹',
    0b11111010 : '⣺',
    0b11111011 : '⣻',
    0b11111100 : '⣼',
    0b11111101 : '⣽',
    0b11111110 : '⣾',
    0b11111111 : '⣿'
}

def normalize(coord):
    coord_type = type(coord)

    if coord_type == int:
        return coord

    elif coord_type == float:
        return int(round(coord))


class Canvas(object):
    """docstring for Surface"""
    def __init__(self, line_ending='\n'):
        super(Canvas, self).__init__()
        self.clear()
        self.line_ending = line_ending

    def clear(self):
        self.pixels = defaultdict(dict)

    def set(self, x, y):
        x = normalize(x)
        y = normalize(y)
        self.pixels[y][x] = pixel_map[y % 4][x % 2]

    def unset(self, x, y):
        x = normalize(x)
        y = normalize(y)
        if y in self.pixels and x in self.pixels[y]:
            del(self.pixels[y][x])
            if not self.pixels[y]:
                del(self.pixels[y])

    def toggle(self, x, y):
        x = normalize(x)
        y = normalize(y)
        if y in self.pixels and x in self.pixels[y]:
            self.unset(x, y)
        else:
            self.set(x, y)

    def frame(self):
        minrow = min(self.pixels.keys())
        minrow -= minrow % 4
        maxrow = max(self.pixels.keys())
        mincol = min(min(x) for x in self.pixels.values())//2
        mincol -= mincol % 2
        maxcol = max(max(x) for x in self.pixels.values())//2
        maxcol += maxcol % 2
        ret = ''
        i = 0
        for rownum in range(minrow, maxrow+1):

            if not i % 4:
                buff = defaultdict(set)

            if rownum in self.pixels:
                for colnum in self.pixels[rownum]:
                    buff[colnum // 2].add(self.pixels[rownum][colnum])

            if i % 4 == 3:
                maxcol = max(buff.keys() or [0])
                ret += ''.join(braille_map[reduce(or_, buff.get(x, [0]))] for x in range(mincol, maxcol+1))
                if rownum != maxrow:
                    ret += self.line_ending

            i += 1

        if buff and i % 4:
            maxcol = max(buff.keys() or [0])
            ret += ''.join(braille_map[reduce(or_, buff.get(x, [0]))] for x in range(mincol, maxcol+1))

        return ret


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
