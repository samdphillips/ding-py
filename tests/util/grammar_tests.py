
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

    def test_basic_choice(self):
        v = self.grammar.choice('nothing', 'anything')
        self.assertEqual(1, v)

    def test_choice(self):
        v = self.grammar.choice(('equal', 4),
                                ('equal', 3),
                                ('equal', 2),
                                ('equal', 1))
        self.assertEqual(1, v)

    def test_many_choice_many(self):
        v = self.grammar.many('choice',
                              ('many1', 'equal', 1),
                              ('equal', 2),
                              ('equal', 3),
                              ('equal', 4))
        self.assertEqual([[1], 2, 3, 4], v)
                                        

