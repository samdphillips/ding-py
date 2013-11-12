

class ParseFail(Exception):
    def __init__(self, stream):
        self._stream = stream


class BaseGrammar(object):
    def __init__(self, stream):
        self.stream = stream

    def anything(self):
        if self.stream.is_empty:
            raise ParseFail(self.stream)

        v = self.stream.first
        self.stream = self.stream.rest
        return v

    def equal(self, value):
        s = self.stream
        if self.stream.is_empty:
            raise ParseFail(s)

        v = self.stream.first
        if value == v:
            self.stream = self.stream.rest
            return v
        raise ParseFail(s)

    def apply(self, name, *args):
        m = getattr(self, name)
        return m(*args)

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
                v = self.apply(rule, *args)
            except ParseFail:
                return ret
            ret.append(v)

    def many1(self, rule):
        try:
            s = self.stream
            v = self.apply(rule)
            return [v] + self.many(rule)
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


