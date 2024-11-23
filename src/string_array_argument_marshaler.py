from src.argument_error import *
from src.argument_marshaler import ArgumentMarshaler


class StringArrayArgumentMarshaler(ArgumentMarshaler):
    def __init__(self):
        self._strings = []

    def set(self, current_argument):
        try:
            self._strings.append(next(current_argument))
        except StopIteration:
            raise ArgumentError(ArgumentErrorCode.MISSING_STRING)

    @staticmethod
    def get_value(argument_marshaler):
        if argument_marshaler and isinstance(argument_marshaler, StringArrayArgumentMarshaler):
            return argument_marshaler._strings
        return []
