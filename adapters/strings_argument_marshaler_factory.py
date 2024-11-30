from ports.argument_marshaler_factory import ArgumentMarshalerFactory
from adapters.no_argument_marshaler import NoArgumentMarshaler
from adapters.string_argument_marshaler import StringArgumentMarshaler
from adapters.string_array_argument_marshaler import StringArrayArgumentMarshaler


class StringsArgumentMarshalerFactory(ArgumentMarshalerFactory):
    def __init__(self):
        self._strings_marshalers = {'*': StringArgumentMarshaler(), '[*]': StringArrayArgumentMarshaler(), '': NoArgumentMarshaler()}

    def get_argument_types(self):
        return self._strings_marshalers.keys()

    def create_from(self, argument_type):
        return self._strings_marshalers[argument_type]
