#!/usr/bin/env python

"""
vidille.py

by prehensile [ twitter.com/prehensile | me@prehensile.co.uk ]
2019-12-29

A hack of image2term3, which uses pyav to pull frames from a video,
drawille to render frames and curses to draw frames in the terminal. 

I'm pleasantly surprised it works at all,
let alone at a reasonable frame rate!

Requires:
- drawille: https://pypi.org/project/drawille/
- pillow: https://pypi.org/project/Pillow/
- av: https://pypi.org/project/av/

"""


import sys
import curses

import av
from drawille import Canvas
from PIL import Image


def image2term(i:Image, canvas_width=160, canvas_height=100, threshold=128, dither=False, invert=False):
    """
    Prints an image converted to drawille
    Args:
        i: a Pillow image, either "L" (grayscale) or "1" (1-bit) format
        threshold: The luminance (0-255) threshold to convert a pixel to a drawille dot
        ratio: Ratio to scale the printed image (e.g. ratio=0.5 is 50%)
        invert: Inverts the threshold check
    """
 
    image_width, image_height = i.size
   
    w_ratio = 1
    h_ratio = 1

    if canvas_width < image_width:
        w_ratio = canvas_width / float(image_width)
    
    if canvas_height < image_height:
        h_ratio = canvas_height / float(image_height)
    

    ratio = min([w_ratio,h_ratio])
    image_width = int(image_width * ratio)
    image_height = int(image_height * ratio)
    i = i.resize((image_width, image_height), Image.ANTIALIAS)

    if dither:
        i = i.convert( "1", dither=Image.FLOYDSTEINBERG )
    
    can = Canvas()
    x = y = 0

    # getdata will be more consistent across different formats of image than i.tobytes()
    i_converted = i.getdata()

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


def play( video_path, terminal_width=80, terminal_height=25, dither=False ):
    """
    A generator which yields drawille-rendered frames from a video file.
    
    Args:
        video_path: path to a video file.
        terminal_with: width of the terminal, in columns.
        terminal_height: height of the terminal, in rows.
        dither: if True, will dither the frames using Pillow's built-in Floyd-Steinberg dither.
    """
    container = av.open( video_path )

    canvas_width = terminal_width *2
    canvas_height = terminal_height *4

    for frame in container.decode(video=0):
        i = frame.to_image()
        f = image2term(
            i.convert("L"),
            canvas_width = canvas_width,
            canvas_height = canvas_height,
            dither = dither,
            invert = True
        )
        yield f


def curses_main( stdscr ): 
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        raise Exception( "usage: vidille.py [path to video file]" )
    
    # get terminal height and width from curses
    terminal_height, terminal_width = stdscr.getmaxyx()

    # hide cursoṛ̣
    curses.curs_set( 0 )

    for screen in play(
            path,
            terminal_width = terminal_width,
            terminal_height = terminal_height,
            dither = False
        ):
        stdscr.clear()
        stdscr.addstr( screen )
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper( curses_main )
   
