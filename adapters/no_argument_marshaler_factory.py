from ports.argument_marshaler_factory import ArgumentMarshalerFactory
from adapters.no_argument_marshaler import NoArgumentMarshaler


class NoArgumentMarshalerFactory(ArgumentMarshalerFactory):
    def get_argument_types(self):
        return ['']

    def create_from(self, argument_type):
        return NoArgumentMarshaler()
