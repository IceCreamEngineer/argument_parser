from src.argument_marshaler import ArgumentMarshaler


class NoArgumentMarshaler(ArgumentMarshaler):
    def set(self, current_argument):
        pass
