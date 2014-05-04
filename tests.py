# -*- coding: utf-8 -*-
from drawille import Canvas, line
from unittest import TestCase, main


class CanvasTestCase(TestCase):


    def test_set(self):
        c = Canvas()
        c.set(1, 1)
        self.assertTrue(1 in c.pixels and 1 in c.pixels[1])


    def test_unset_empty(self):
        c = Canvas()
        c.set(1, 1)
        c.unset(1, 1)
        self.assertEqual(c.pixels, dict())


    def test_unset_nonempty(self):
        c = Canvas()
        c.set(1, 1)
        c.set(2, 1)
        c.unset(1, 1)
        self.assertEqual(c.pixels, {1:{2: 2}})


    def test_clear(self):
        c = Canvas()
        c.set(1, 1)
        c.clear()
        self.assertEqual(c.pixels, dict())


    def test_toggle(self):
        c = Canvas()
        c.toggle(0, 0)
        self.assertEqual(c.pixels, {0: {0: 1}})
        c.toggle(0, 0)
        self.assertEqual(c.pixels, dict())


    def test_set_text(self):
        c = Canvas()
        c.set_text(0, 0, "asdf")
        self.assertEqual(c.frame(), "asdf")


    def test_frame(self):
        c = Canvas()
        c.set(0, 0)
        self.assertEqual(c.frame(), '⠁')


class LineTestCase(TestCase):


    def test_single_pixel(self):
        self.assertEqual(list(line(0, 0, 0, 0)), [(0, 0)])


    def test_row(self):
        self.assertEqual(list(line(0, 0, 1, 0)), [(0, 0), (1, 0)])


    def test_column(self):
        self.assertEqual(list(line(0, 0, 0, 1)), [(0, 0), (0, 1)])


    def test_diagonal(self):
        self.assertEqual(list(line(0, 0, 1, 1)), [(0, 0), (1, 1)])


if __name__ == '__main__':
    main()
