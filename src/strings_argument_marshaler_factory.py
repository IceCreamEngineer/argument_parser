from src.argument_marshaler_factory import ArgumentMarshalerFactory
from src.no_argument_marshaler import NoArgumentMarshaler
from src.string_argument_marshaler import StringArgumentMarshaler
from src.string_array_argument_marshaler import StringArrayArgumentMarshaler


class StringsArgumentMarshalerFactory(ArgumentMarshalerFactory):
    def __init__(self):
        self._strings_marshalers = {'*': StringArgumentMarshaler(), '[*]': StringArrayArgumentMarshaler(), '': NoArgumentMarshaler()}

    def get_argument_types(self):
        return self._strings_marshalers.keys()

    def create_from(self, argument_type):
        return self._strings_marshalers[argument_type]
