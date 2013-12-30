

class CompoundTerm(object):
    def __init__(self, shape, terms):
        self.shape = shape
        self.terms = terms


class IdTerm(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, `self.name`)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.name == other.name)


class DelimiterTerm(IdTerm):
    pass


