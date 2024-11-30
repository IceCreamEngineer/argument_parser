from ports.argument_marshaler import ArgumentMarshaler


class NoArgumentMarshaler(ArgumentMarshaler):
    def set(self, current_argument):
        pass

    def get_value_from(self, marshaler):
        pass
