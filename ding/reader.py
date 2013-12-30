

import logging

from ding.term         import CompoundTerm
from ding.util.grammar import BaseGrammar, ParseFail
from ding.util.stream  import Stream


logger = logging.getLogger(__name__)


class Reader(BaseGrammar):
    @classmethod
    def from_string(cls, s):
        st = Stream.from_iterable(s)
        return cls(st, logger)

    def many_join(self, rule, *args):
        self.debug('many_join', '%s %s', rule, args)
        v = self.many(rule, *args)
        return ''.join(v)

    def many1_join(self, rule, *args):
        self.debug('many1_join', '%s %s', rule, args)
        v = self.many1(rule, *args)
        return ''.join(v)

    def char(self, c):
        self.debug('char', '%s', `c`)
        s = self.stream
        v = self.anything()
        if v == c:
            return v
        else:
            raise ParseFail(s)

    def string(self, t):
        self.debug('string', '%s', `t`)
        r = []
        for c in t:
            r.append(self.char(c))
        return ''.join(r)

    # XXX: move to BaseGrammar
    def in_range(self, start_value, end_value):
        self.debug('in_range', '%s -> %s', `start_value`, `end_value`)
        s = self.stream
        v = self.anything()

        if start_value <= v and v <= end_value:
            return v
        raise ParseFail(s)

    def not_string(self, s):
        self.debug('not_string', '%s', `s`)
        self.not_parse('string', s)
        return self.anything()

    def space(self):
        self.debug('space')
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
        self.debug('digit')
        return self.in_range('0', '9')

    def id_start_char(self):
        self.debug('id_start_char')
        return self.choice(('in_range', 'a', 'z'), ('char', '_'))

    def id_char(self):
        self.debug('id_char')
        return self.choice('id_start_char', 'digit')

    def identifier(self):
        self.debug('identifier')
        i = self.id_start_char()
        dentifier = self.many_join('id_char')
        return i + dentifier

    def operator_char(self):
        self.debug('operator_char')
        op_chars = '~!@#$%^&*-+==<>./?:|'
        s = self.stream
        v = self.anything()

        if v in op_chars:
            return v
        raise ParseFail(s)

    def operator_identifier(self):
        self.debug('operator_identifier')
        return self.many1_join('operator_char')

    def compound_term_delim(self, start, end):
        self.debug('compound_term_delim', '%s %s', `start`, `end`)
        self.char(start)
        v = self.many('token', 'term')
        self.char(end)
        return CompoundTerm(start+end, v)

    def compound_term(self):
        self.debug('compound_term')
        return self.choice(('compound_term_delim', '{', '}'),
                           ('compound_term_delim', '[', ']'),
                           ('compound_term_delim', '(', ')'))

    def delimiter_term(self):
        self.debug('delimiter_term')
        return self.choice(('char', ','), ('char', ';'))

    def term(self):
        self.debug('term')
        return self.choice('compound_term',
                           'delimiter_term',
                           'identifier')

    def token_space(self):
        self.debug('token_space')
        self.choice('whitespace', 'line_comment', 'block_comment')

    def token_spaces(self):
        self.debug('token_spaces')
        self.many('token_space')

    def token(self, rule, *args):
        self.debug('token', '%s %s', rule, args)
        self.token_spaces()
        v = self.apply(rule, *args)
        self.token_spaces()
        return v


