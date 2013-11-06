
import unittest


class BaseGrammarTests(unittest.TestCase):
    def setUp(self):
        from ding.util.stream import Stream
        from ding.util.grammar import BaseGrammar
        s = Stream.from_iterable([1, 2, 3, 4])
        self.grammar = BaseGrammar(s)

    def test_anything(self):
        self.assertEqual(1, self.grammar.anything())

    def test_nothing(self):
        self.assertEqual(1, self.grammar.anything())
        self.assertEqual(2, self.grammar.anything())
        self.assertEqual(3, self.grammar.anything())
        self.assertEqual(4, self.grammar.anything())
        self.assertEqual(None, self.grammar.nothing())

    def test_many(self):
        self.assertEqual([1, 2, 3, 4], self.grammar.many('anything'))

    def test_many1(self):
        self.assertEqual([1, 2, 3, 4], self.grammar.many1('anything'))

    def test_choice(self):
        v = self.grammar.choice('nothing', 'anything')
        self.assertEqual(1, v)


class CharGrammarTests(unittest.TestCase):
    def setUp(self):
        from ding.util.stream import Stream
        from ding.util.grammar import CharGrammar
        s = Stream.from_iterable("test")
        self.grammar = CharGrammar(s)

    def test_char(self):
        self.assertEqual('t', self.grammar.char('t'))

    def test_chars(self):
        self.assertEqual('t', self.grammar.char('t'))
        self.assertEqual('e', self.grammar.char('e'))
        self.assertEqual('s', self.grammar.char('s'))
        self.assertEqual('t', self.grammar.char('t'))


