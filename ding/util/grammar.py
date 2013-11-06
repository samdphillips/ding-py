

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

    def apply(self, name, *args):
        m = getattr(self, name)
        return m(*args)

    def not_parse(self, rule):
        s = self.stream
        try:
            v = self.apply(rule)
        except ParseFail:
            return None
        finally:
            self.stream = s
        raise ParseFail(self.stream)

    def nothing(self):
        return self.not_parse('anything')

    def many(self, rule):
        ret = []
        while True:
            try:
                v = self.apply(rule)
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


class CharGrammar(BaseGrammar):
    def char(self, c):
        s = self.stream
        v = self.anything()
        if v == c:
            return v
        else:
            raise ParseFail(s)


