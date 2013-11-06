

from ding.util.grammar import BaseGrammar, ParseFail
from ding.util.stream  import Stream


class Reader(BaseGrammar):
    @classmethod
    def from_string(cls, s):
        st = Stream.from_iterable(s)
        return cls(st)

    def many_join(self, rule, *args):
        v = super(Reader, self).many(rule, *args)
        return ''.join(v)

    def char(self, c):
        s = self.stream
        v = self.anything()
        if v == c:
            return v
        else:
            raise ParseFail(s)

    def string(self, t):
        r = []
        for c in t:
            r.append(self.char(c))
        return ''.join(r)

    def not_string(self, s):
        self.not_parse('string', s)
        r = []
        for i in xrange(len(s)):
            r.append(self.anything())
        return ''.join(r)

    def space(self):
        s = self.stream
        c = self.anything()
        if c.isspace():
            return c
        raise ParseFail(s)
        
    def whitespace(self):
        return self.many_join('space')

    def line_comment(self):
        self.string('//')
        self.many('not_string', '\n')
        self.char('\n')


