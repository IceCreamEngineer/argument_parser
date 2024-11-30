class ArgumentSchemaElement:
    def __init__(self, name, argument_type, description="", is_required=True, long_name=""):
        self.name = name
        self.argument_type = argument_type
        self.description = description
        self.is_required = is_required
        self.long_name = long_name
