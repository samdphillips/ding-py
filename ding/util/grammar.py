

import logging


class ParseFail(Exception):
    def __init__(self, stream):
        self._stream = stream

    def __str__(self):
        if self._stream.is_empty:
            return "Got: <EMPTY>"
        else:
            return "Got: %s" % repr(self._stream.first)


class BaseGrammar(object):
    def __init__(self, stream, logger=None):
        self.stream = stream
        self._logger = logger

    def is_debug_logging(self):
        return (self._logger is not None and
                self._logger.isEnabledFor(logging.DEBUG))

    def debug(self, tag, fmt='', *rest):
        if self.is_debug_logging():
            d = {'tag': tag}
            if self.stream.is_empty:
                d['stream'] = []
            else:
                t = []
                s = self.stream
                for i in xrange(10):
                    if s.is_empty:
                        break
                    t.append(s.first)
                    s = s.rest
                d['stream'] = t
            self._logger.debug(fmt, *rest, extra=d)

    def anything(self):
        if self.stream.is_empty:
            raise ParseFail(self.stream)

        v = self.stream.first
        self.stream = self.stream.rest
        return v

    def predicate(self, pred):
        s = self.stream
        v = self.anything()
        if pred(v):
            return v
        raise ParseFail(s)

    def equal(self, value):
        s = self.stream
        if self.stream.is_empty:
            raise ParseFail(s)

        v = self.stream.first
        if value == v:
            self.stream = self.stream.rest
            return v
        raise ParseFail(s)

    def in_range(self, start_value, end_value):
        self.debug('in_range', '%s -> %s', repr(start_value), repr(end_value))
        s = self.stream
        v = self.anything()

        if start_value <= v and v <= end_value:
            return v
        raise ParseFail(s)

    def apply(self, name, *args):
        m = getattr(self, name)
        return m(*args)

    def foreign(self, grammar, name, *args):
        g = grammar(self.stream)
        m = getattr(g, name)
        v = m(*args)
        self.stream = g.stream
        return v

    def not_parse(self, rule, *args):
        s = self.stream
        try:
            v = self.apply(rule, *args)
        except ParseFail:
            return None
        finally:
            self.stream = s
        raise ParseFail(s)

    def nothing(self):
        return self.not_parse('anything')

    def many(self, rule, *args):
        ret = []
        while True:
            try:
                s = self.stream
                v = self.apply(rule, *args)
            except ParseFail:
                self.stream = s
                return ret
            ret.append(v)

    def many1(self, rule, *args):
        try:
            s = self.stream
            v = self.apply(rule, *args)
            return [v] + self.many(rule, *args)
        except ParseFail:
            self.stream = s
            raise

    def choice(self, *rules):
        for r in rules:
            s = self.stream
            try:
                if type(r) != tuple:
                    r = (r,)
                return self.apply(*r)
            except ParseFail:
                self.stream = s
        raise ParseFail(s)


