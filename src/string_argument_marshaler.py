from src.argument_error import *
from src.argument_marshaler import ArgumentMarshaler


class StringArgumentMarshaler(ArgumentMarshaler):
    def __init__(self):
        self._string_value = ''

    def set(self, current_argument):
        try:
            self._string_value = next(current_argument)
        except StopIteration:
            raise ArgumentError(ArgumentErrorCode.MISSING_STRING)

    @staticmethod
    def get_value(argument_marshaler):
        if argument_marshaler and isinstance(argument_marshaler, StringArgumentMarshaler):
            return argument_marshaler._string_value
        return ''
