#!/usr/bin/env python
# -*- coding: utf-8 -*-
# NOTE: This example requires Pillow, a PIL fork for python3 
# https://pillow.readthedocs.io/en/5.1.x/installation.html 
# example:
# $  PYTHONPATH=`pwd` python3 examples/image2term3.py http://fc00.deviantart.net/fs71/f/2011/310/5/a/giant_nyan_cat_by_daieny-d4fc8u1.png -t 100 -r 0.01

try:
    from PIL import Image
except:
    from sys import stderr
    stderr.write('[E] PIL not installed\n')
    exit(1)
from drawille import Canvas
from io import BytesIO
from io import StringIO
import requests

def ioctl_GWINSZ(fd):
    """
    Get Window Size given a file descriptor
    """
    import fcntl
    import termios
    import struct
    #Hex Tuple 
    # Terminal IO Current Window Size ? - 1234 ?!
    cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    return cr

def getTerminalSize():
    import os
    env = os.environ

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
    #Returns Columns (X), Lines (Y)
    return int(cr[1]), int(cr[0])
    

def image2term(image, threshold=128, ratio=None, invert=False):
    """
    Prints an image converted to drawille
    Args:
        image: filepath / URL of the image
        threshold: The color (0-255) threshold to convert a pixel to a drawille dot
        ratio: Ratio to scale the printed image (e.g. ratio=0.5 is 50%)
        invert: Inverts the threshold check
    """

    if image.startswith('http://') or image.startswith('https://'):
        r = requests.get(image,stream=True)
        i = Image.open(r.raw).convert('L')
    else:
        f = open(image,'rb') #Open in binary mode
        i = Image.open(f).convert('L')
    image_width, image_height = i.size
    if ratio:
        image_width = int(image_width * ratio)
        image_height = int(image_height * ratio)
        i = i.resize((image_width, image_height), Image.ANTIALIAS)
    else:
        terminal_width = getTerminalSize()[0] * 2#Number of Columns
        terminal_height = getTerminalSize()[1] * 4
    
        w_ratio = 1
        h_ratio = 1

        if terminal_width < image_width:
            w_ratio = terminal_width / float(image_width)
        
        if terminal_height < image_height:
            h_ratio = terminal_height / float(image_height)
        

        ratio = min([w_ratio,h_ratio])
        image_width = int(image_width * ratio)
        image_height = int(image_height * ratio)
        i = i.resize((image_width, image_height), Image.ANTIALIAS)
    can = Canvas()
    x = y = 0

    try:
        i_converted = i.tobytes()
    except AttributeError:
        i_converted = i.tostring()

    for pix in i_converted:
        if invert:
            if pix > threshold:
                can.set(x, y)
        else:
            if pix < threshold:
                can.set(x, y)
        x += 1
        if x >= image_width:
            y += 1
            x = 0
    return can.frame(0, 0)


def argparser():
    import argparse
    from sys import stdout
    argp = argparse.ArgumentParser(description='drawille - image to terminal example script')
    argp.add_argument('-o', '--output'
                     ,help      = 'Output file - default is STDOUT'
                     ,metavar   = 'FILE'
                     ,default   = stdout
                     ,type      = argparse.FileType('image_width')
                     )
    argp.add_argument('-r', '--ratio'
                     ,help      = 'Image resize ratio'
                     ,default   = None
                     ,action    = 'store'
                     ,type      = float
                     ,metavar   = 'N'
                     )
    argp.add_argument('-t', '--threshold'
                     ,help      = 'Color threshold'
                     ,default   = 128
                     ,action    = 'store'
                     ,type      = int
                     ,metavar   = 'N'
                     )
    argp.add_argument('-i', '--invert'
                     ,help      = 'Invert colors'
                     ,default   = False
                     ,action    = 'store_true'
                     )
    argp.add_argument('image'
                     ,metavar   = 'FILE'
                     ,help      = 'Image file path/url'
                     )
    return vars(argp.parse_args())


def __main__():
    args = argparser()
    args['output'].write(image2term(args['image'], args['threshold'], args['ratio'], args['invert']))
    args['output'].write('\n')


if __name__ == '__main__':
    __main__()
