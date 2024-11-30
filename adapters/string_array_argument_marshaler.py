from entities.argument_error import *
from ports.argument_marshaler import ArgumentMarshaler


class StringArrayArgumentMarshaler(ArgumentMarshaler):
    def __init__(self):
        self._strings = []

    def set(self, current_argument):
        try:
            self._strings.append(next(current_argument))
        except StopIteration:
            raise ArgumentError(ArgumentErrorCode.MISSING_STRING)

    def get_value_from(self, marshaler):
        return self._strings
