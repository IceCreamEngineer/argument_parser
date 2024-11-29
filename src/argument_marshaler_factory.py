from abc import ABC, abstractmethod

from src.no_argument_marshaler import NoArgumentMarshaler


class ArgumentMarshalerFactory(ABC):
    @abstractmethod
    def get_argument_types(self):
        pass

    @abstractmethod
    def create_from(self, argument_type):
        pass


class NoArgumentMarshalerFactory(ArgumentMarshalerFactory):
    def get_argument_types(self):
        return ['']

    def create_from(self, argument_type):
        return NoArgumentMarshaler()
