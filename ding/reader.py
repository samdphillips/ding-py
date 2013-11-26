

from ding.term         import CompoundTerm
from ding.util.grammar import BaseGrammar, ParseFail
from ding.util.stream  import Stream


class Reader(BaseGrammar):
    @classmethod
    def from_string(cls, s):
        st = Stream.from_iterable(s)
        return cls(st)

    def many_join(self, rule, *args):
        v = self.many(rule, *args)
        return ''.join(v)

    def many1_join(self, rule, *args):
        v = self.many1(rule, *args)
        return ''.join(v)

    def char(self, c):
        self.debug('char')
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

    # XXX: move to BaseGrammar
    def in_range(self, start_value, end_value):
        s = self.stream
        v = self.anything()

        if start_value <= v and v <= end_value:
            return v
        raise ParseFail(s)

    def not_string(self, s):
        self.not_parse('string', s)
        return self.anything()

    def space(self):
        s = self.stream
        c = self.anything()
        if c.isspace():
            return c
        raise ParseFail(s)

    def whitespace(self):
        self.debug('whitespace')
        return self.many1_join('space')

    def line_comment(self):
        self.debug('line_comment')
        self.string('//')
        self.many('not_string', '\n')
        self.char('\n')

    def block_comment(self):
        self.debug('block_comment')
        self.string('/*')
        self.many('not_string', '*/')
        self.string('*/')

    def digit(self):
        return self.in_range('0', '9')

    def id_start_char(self):
        return self.choice(('in_range', 'a', 'z'), ('char', '_'))

    def id_char(self):
        return self.choice('id_start_char', 'digit')

    def identifier(self):
        i = self.id_start_char()
        dentifier = self.many_join('id_char')
        return i + dentifier

    def compound_term_delim(self, start, end):
        self.char(start)
        v = self.many('token', 'term')
        self.char(end)
        return CompoundTerm(start+end, v)

    def compound_term(self):
        return self.choice(('compound_term_delim', '{', '}'),
                           ('compound_term_delim', '[', ']'),
                           ('compound_term_delim', '(', ')'))

    def delimiter_term(self):
        return self.choice(('char', ','), ('char', ';'))

    def term(self):
        return self.choice('compound_term',
                           'delimiter_term',
                           'identifier')

    def token_space(self):
        self.choice('whitespace', 'line_comment', 'block_comment')

    def token_spaces(self):
        self.many('token_space')

    def token(self, rule, *args):
        self.token_spaces()
        v = self.apply(rule, *args)
        self.token_spaces()
        return v


