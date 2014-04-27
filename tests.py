# -*- coding: utf-8 -*-
from drawille import Canvas
from unittest import TestCase, main


class CanvasTestCase(TestCase):


    def test_set(self):
        c = Canvas()
        c.set(1,1)
        self.assertTrue(1 in c.pixels and 1 in c.pixels[1])


    def test_unset(self):
        c = Canvas()
        c.set(1,1)
        c.unset(1, 1)
        self.assertEqual(c.pixels, dict())


    def test_frame(self):
        c = Canvas()
        c.set(0,0)
        self.assertEqual(c.frame(), '\xe2\xa0\x81')
        self.assertEqual(c.frame(), '⠁')


if __name__ == '__main__':
    main()
