class ArgumentSchemaElement:
    def __init__(self, name, type_notation, description="", is_required=True, long_name=""):
        self.name = name
        self.type_notation = type_notation
        self.description = description
        self.is_required = is_required
        self.long_name = long_name
