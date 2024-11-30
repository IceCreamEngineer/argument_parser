from abc import ABC, abstractmethod


class ArgumentMarshalerFactory(ABC):
    @abstractmethod
    def get_argument_types(self):
        pass

    @abstractmethod
    def create_from(self, argument_type):
        pass
