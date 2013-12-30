
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

    def test_predicate(self):
        def is_odd(n):
            return n % 2 == 1
        v = self.grammar.predicate(is_odd)
        self.assertEqual(1, v)

    def test_predicate_fail(self):
        from ding.util.grammar import ParseFail
        def is_even(n):
            return n % 2 == 0
        with self.assertRaises(ParseFail):
            self.grammar.predicate(is_even)

    def test_foreign_rule_success(self):
        from ding.util.grammar import BaseGrammar
        class Foreign(BaseGrammar):
            def one(self):
                return self.equal(1)

        v = self.grammar.foreign(Foreign, 'one')
        self.assertEqual(1, v)

    def test_foreign_rule_success(self):
        from ding.util.grammar import BaseGrammar, ParseFail
        class Foreign(BaseGrammar):
            def one(self):
                return self.equal(1)

            def two(self):
                return self.equal(2)

        with self.assertRaises(ParseFail):
            self.grammar.foreign(Foreign, 'two')
        v = self.grammar.foreign(Foreign, 'one')
        self.assertEqual(1, v)


