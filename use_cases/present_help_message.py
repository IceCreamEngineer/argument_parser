import textwrap


class PresentHelpMessageUseCase:
    def __init__(self, program_filename, description, presenter):
        self._program_filename = program_filename
        self._description = textwrap.fill(description, 72)
        self._presenter = presenter
        self._help_message = ""

    def present_help_message(self, schema=None):
        self._build_help_message_from(schema)
        self._presenter.present(self._help_message)

    def _build_help_message_from(self, schema):
        schema = self._check_to_default(schema)
        self._add_usage_line_with_required(schema)
        self._add_description()
        self._add_optional_arguments_from(schema)

    def _add_usage_line_with_required(self, schema):
        self._help_message += f"usage: {self._program_filename} [-h]"
        for element in schema:
            if element.is_required:
                self._help_message += f" -{element.name}{self._add_flag_value_for(element)}"

    @staticmethod
    def _add_flag_value_for(element):
        if element.argument_type:
            return f' {element.long_name.upper()}' if element.long_name else f' {element.name.upper()}'
        return ''

    def _add_description(self):
        self._help_message += "\n" + \
                              f"\n" + \
                              f"{self._description}\n" + \
                              f"\n"

    def _add_optional_arguments_from(self, schema):
        help_arg_names = "  -h, --help"
        max_arg_names_length = self._get_max_arg_names_length_from(schema, help_arg_names)
        self._build_optional_arguments_from(schema, help_arg_names, max_arg_names_length)

    def _get_max_arg_names_length_from(self, schema, help_arg_names):
        arg_names_lengths = self._get_arg_names_lengths_from(schema, help_arg_names)
        max_arg_names_length = len(help_arg_names) if not schema else max(arg_names_lengths)
        return max_arg_names_length

    def _get_arg_names_lengths_from(self, schema, help_arg_names):
        arg_names_lengths = []
        self._append_arg_names_lengths_from(schema, arg_names_lengths)
        arg_names_lengths.append(len(help_arg_names))
        return arg_names_lengths

    def _append_arg_names_lengths_from(self, schema, arg_names_lengths):
        for element in schema:
            arg_names_lengths.append(len(f"  -{element.name}"
                f"{'' if not element.long_name else f', --{element.long_name}'}{self._add_flag_value_for(element)}"))

    def _build_optional_arguments_from(self, schema, help_arg_names, max_arg_names_length):
        self._help_message += "optional arguments:\n"
        self._help_message += f"  -h, --help{self._spacer(help_arg_names, max_arg_names_length)}show this help message and exit\n"
        self._add_arg_help_messages(schema, max_arg_names_length)

    @staticmethod
    def _spacer(arg_names, max_arg_names_length):
        return " " * abs((max_arg_names_length + 2) - len(arg_names))

    def _add_arg_help_messages(self, schema, max_arg_names_length):
        for element in schema:
            long_name_label = "" if not element.long_name else f", --{element.long_name}"
            args_names = f"  -{element.name}{long_name_label}{self._add_flag_value_for(element)}"
            self._help_message += f"{args_names}{self._spacer(args_names, max_arg_names_length)}{element.description}\n"

    @staticmethod
    def _check_to_default(schema):
        if not schema:
            schema = []
        return schema
