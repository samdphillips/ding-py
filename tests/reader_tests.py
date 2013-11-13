

import unittest


class ReaderTests(unittest.TestCase):
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
