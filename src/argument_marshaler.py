from abc import ABC, abstractmethod


class ArgumentMarshaler(ABC):
    @abstractmethod
    def set(self, current_argument):
        pass
