

import unittest


class ReaderTests(unittest.TestCase):
    log_format = "[%(name)15s] [%(levelname)8s] [%(tag)15s] %(stream)s -- %(message)s"

    def test_whitespace(self):
        from ding.reader import Reader
        r = Reader.from_string('    ')
        self.assertEqual('    ', r.whitespace())
        r.nothing()

    def test_whitespace_takes_just_enough(self):
        from ding.reader import Reader
        r = Reader.from_string('    test')
        r.whitespace()
        self.assertEqual('t', r.anything())

    def test_line_comment(self):
        from ding.reader import Reader
        r = Reader.from_string('// this is a test\n')
        r.line_comment()
        r.nothing()

    def test_block_comment_even(self):
        from ding.reader import Reader
        r = Reader.from_string('/*  */')
        r.block_comment()
        r.nothing()

    def test_block_comment_odd(self):
        from ding.reader import Reader
        r = Reader.from_string('/* */')
        r.block_comment()
        r.nothing()

    def test_token_space(self):
        from ding.reader import Reader
        r = Reader.from_string('  // abcde \n\n\n/* fghi\n * jklm\n */  ')
        r.token_spaces()
        r.nothing()

    def test_identifier(self):
        from ding.reader import Reader
        tests = ['id', 'x', 'x1', 'a_variable', '_var']
        for t in tests:
            r = Reader.from_string(t)
            self.assertEqual(t, r.identifier())
            r.nothing()

    def test_id_tokens(self):
        from ding.reader import Reader
        r = Reader.from_string(' a// abe \nb\n\n c /* gh\n * jklm\n */ d ')
        v = r.many('token', 'identifier')
        self.assertEqual(['a', 'b', 'c', 'd'], v)
        r.nothing()

    def test_operator_identifiers(self):
        from ding.reader import Reader
        r = Reader.from_string('+ - = ++ / * == += -= := ? : <=>')
        v = ['+', '-', '=', '++', '/', '*', '==', '+=', '-=',
                ':=', '?', ':', '<=>']
        for x in v:
            self.assertEqual(x, r.token('operator_identifier'))
        r.nothing()

    def test_compound_term(self):
        from ding.reader import Reader
        r = Reader.from_string('{ a b c d e }')
        v = r.token('compound_term')
        self.assertEqual('{}', v.shape)
        self.assertEqual(['a','b','c','d','e'], v.terms)
        r.nothing()

    def test_comma_term(self):
        from ding.reader import Reader
        r = Reader.from_string('a, b, c')
        v = r.many('token', 'term')
        self.assertEqual(['a',',','b',',','c'], v)
        r.nothing()

    def test_semicolon_term(self):
        from ding.reader import Reader
        r = Reader.from_string('a ; b ; c')
        v = r.many('token', 'term')
        self.assertEqual(['a',';','b',';','c'], v)
        r.nothing()


