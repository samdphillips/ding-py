

import unittest


class ReaderTests(unittest.TestCase):
    def test_whitespace(self):
        from ding.reader import Reader
        r = Reader.from_string('    ')
        self.assertEqual('    ', r.whitespace())
        r.nothing()

    def test_line_comment(self):
        from ding.reader import Reader
        r = Reader.from_string('// this is a test\n')
        r.line_comment()
        r.nothing()


