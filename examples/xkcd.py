# -*- coding: utf-8 -*-

from drawille import Canvas
from PIL import Image
from sys import argv, exit
from StringIO import StringIO
import urllib2
import re


def getTerminalSize():
    import os
    env = os.environ

    def ioctl_GWINSZ(fd):
        import fcntl
        import termios
        import struct
        cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
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


def usage():
    print 'Usage: %s <url/id>'

if __name__ == '__main__':
    if len(argv) < 2:
        usage()
        exit()
    if argv[1].startswith('http'):
        url = argv[1]
    else:
        url = 'http://xkcd.com/%s/' % argv[1]
    c = urllib2.urlopen(url).read()
    img_url = re.findall('http:\/\/imgs.xkcd.com\/comics\/[^"\']+', c)[0]
    i = Image.open(StringIO(urllib2.urlopen(img_url).read())).convert('L')
    w, h = i.size
    tw, th = getTerminalSize()
    tw *= 2
    th *= 2
    if tw < w:
        ratio = tw / float(w)
        w = tw
        h = int(h * ratio)
        i = i.resize((w, h), Image.ANTIALIAS)
    can = Canvas()
    x = y = 0
    for pix in i.tobytes():
        if ord(pix) < 128:
            can.set(x, y)
        x += 1
        if x >= w:
            y += 1
            x = 0
    print can.frame()
