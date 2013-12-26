
import unittest


class IteratorStreamTests(unittest.TestCase):
    def setUp(self):
        from ding.util.stream import Stream
        self.stream = Stream.from_iterable(xrange(10))

    def test_first(self):
        self.assertEqual(self.stream.first, 0)
        self.assertEqual(self.stream.first, 0)

    def test_rest_first(self):
        self.assertEqual(self.stream.rest.first, 1)
        self.assertEqual(self.stream.rest.first, 1)

    def test_rest_rest_first(self):
        self.assertEqual(self.stream.rest.rest.first, 2)
        self.assertEqual(self.stream.rest.rest.first, 2)

    def test_is_empty(self):
        self.assertFalse(self.stream.is_empty)

    def test_all_read_is_empty(self):
        s = self.stream
        for n in xrange(10):
            self.assertEqual(s.first, n)
            s = s.rest
        self.assertTrue(s.is_empty)


class EmptyStreamTests(unittest.TestCase):
    def setUp(self):
        from ding.util.stream import Stream
        self.stream = Stream.from_iterable([])

    def test_is_empty(self):
        self.assertTrue(self.stream.is_empty)

    def test_first(self):
        from ding.util.stream import EmptyStreamError
        with self.assertRaises(EmptyStreamError):
            self.stream.first

    def test_rest(self):
        from ding.util.stream import EmptyStreamError
        with self.assertRaises(EmptyStreamError):
            self.stream.rest


class IteratorTests(unittest.TestCase):
    def setUp(self):
        from ding.util.stream import Stream
        self.stream = Stream.from_iterable(xrange(10))

    def test_iterate_over_values(self):
        from itertools import izip
        for x,y in izip(self.stream, xrange(10)):
            self.assertEqual(x, y)
        self.assertEqual(self.stream.first, 0)


class CharIoIteratorTests(unittest.TestCase):
    def setUp(self):
        from StringIO import StringIO
        from ding.util.stream import CharIoIterator
        sio = StringIO('0123456789')
        self.cio_iter = CharIoIterator(sio)

    def test_iteration(self):
        from itertools import izip
        s = '0123456789'
        for c1, c2 in izip(self.cio_iter, s):
            self.assertEqual(c1, c2)


class PositionPropertyTests(unittest.TestCase):
    def test_regular_characters(self):
        from ding.util.stream import PositionPropertyUpdater
        s = 'abcde'
        ppu = PositionPropertyUpdater()
        for c in s:
            p = ppu.update(c)

        self.assertEqual(p['offset'], 5)
        self.assertEqual(p['line'],   1)
        self.assertEqual(p['column'], 5)

    def test_newlines(self):
        from ding.util.stream import PositionPropertyUpdater
        s = '\n\n\n'
        ppu = PositionPropertyUpdater()
        for c in s:
            p = ppu.update(c)

        self.assertEqual(p['offset'], 3)
        self.assertEqual(p['line'],   3)
        self.assertEqual(p['column'], 0)


