class ArgumentSchema:
    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self._elements = elements

    def get_elements(self):
        return self._elements


class ArgumentSchemaElement:
    def __init__(self, name, type_notation, description="", is_required=True, long_name=""):
        self.name = name
        self.type_notation = type_notation
        self.description = description
        self.is_required = is_required
        self.long_name = long_name
