

class EmptyStreamError(Exception):
    pass


class EmptyState(object):
    def is_empty(self, stream):
        return True

    def value(self, stream):
        raise EmptyStreamError()

    def rest(self, stream):
        raise EmptyStreamError()


EMPTY = EmptyState()


class NullPropertyUpdater(object):
    def update(self, value):
        return {}


NULL_PROPERTIES = NullPropertyUpdater()


class PositionPropertyUpdater(object):
    FIELDS = ['filename', 'offset', 'line', 'column']

    def __init__(self, filename=None, offset=0, line=1, column=0):
        self._filename = filename
        self._offset   = offset
        self._line     = line
        self._column   = column
        self._prev     = None

    def snapshot(self):
        return dict([(k, getattr(self, '_' + k)) for k in self.FIELDS])

    def update(self, char):
        self._offset += 1
        self._column += 1
        return self.snapshot()


class PendingState(object):
    __slots__ = ['_iterator', '_properties']

    def __init__(self, iterator, properties):
        self._iterator = iterator
        self._properties = properties

    def value(self, stream):
        state = self.force(stream)
        return state.value(stream)

    def rest(self, stream):
        state = self.force(stream)
        return state.rest(stream)

    def is_empty(self, stream):
        state = self.force(stream)
        return state.is_empty(stream)

    def force(self, stream):
        try:
            v = self._iterator.next()
            properties = self._properties.update(v)
            s = ValueState(v, self)
        except StopIteration:
            properties = {}
            s = EMPTY
        stream._state = s
        stream._properties = properties
        return s


class ValueState(object):
    __slots__ = ['_value', '_rest']

    def __init__(self, value, rest):
        self._value = value
        self._rest = Stream(rest)

    def value(self, stream):
        return self._value

    def rest(self, stream):
        return self._rest

    def is_empty(self, stream):
        return False


class Stream(object):
    __slots__ = ['_state', '_properties']

    @classmethod
    def from_iterable(cls, v, property_updater=NULL_PROPERTIES):
        return cls.from_iterator(iter(v), property_updater)

    @classmethod
    def from_iterator(cls, it, property_updater=NULL_PROPERTIES):
        return cls(PendingState(it, property_updater))

    @classmethod
    def from_file(cls, filename, property_updater=NullPropertyUpdater()):
        f = file(filename, 'r')
        it = CharIoIterator(f)
        return cls.from_iterator(it, property_updater)

    def __init__(self, state):
        self._state = state
        self._properties = None

    @property
    def first(self):
        return self._state.value(self)

    @property
    def rest(self):
        return self._state.rest(self)

    @property
    def is_empty(self):
        return self._state.is_empty(self)

    def __iter__(self):
        s = self
        while not s.is_empty:
            yield s.first
            s = s.rest
        raise StopIteration


class CharIoIterator(object):
    def __init__(self, io):
        self._io = io

    def __iter__(self):
        return self

    def next(self):
        c = self._io.read(1)
        if c == '':
            raise StopIteration
        return c


