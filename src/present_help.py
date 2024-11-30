from abc import ABC, abstractmethod


class HelpPresenter(ABC):
    def __init__(self, program_filename, description):
        self._help_message = \
            (f"usage: {program_filename} [-h]\n"
             f"\n"
             f"{description}\n"
             f"\n"
             f"optional arguments:\n")

    def present(self, schema=None):
        schema = self._check_to_default(schema)
        help_arg_names = "  -h, --help"
        arg_names_lengths = []
        for element in schema:
            long_name_label = "" if not element.long_name else f", --{element.long_name}"
            arg_names_lengths.append(len(f"  -{element.name}{long_name_label}"))
        arg_names_lengths.append(len(help_arg_names))
        max_arg_names_length = len(help_arg_names) if not schema else max(arg_names_lengths)
        self._help_message += f"  -h, --help{self._spacer(help_arg_names, max_arg_names_length)}show this help message and exit\n"
        self._add_arg_help_messages(schema, max_arg_names_length)

    def _add_arg_help_messages(self, schema, max_arg_names_length):
        for element in schema:
            long_name_label = "" if not element.long_name else f", --{element.long_name}"
            args_names = f"  -{element.name}{long_name_label}"
            self._help_message += f"{args_names}{self._spacer(args_names, max_arg_names_length)}{element.description}\n"

    def _spacer(self, arg_names, max_arg_names_length):
        return " " * abs((max_arg_names_length + 2) - len(arg_names))

    @staticmethod
    def _check_to_default(schema):
        if not schema:
            schema = []
        return schema


class NullHelpPresenter(HelpPresenter):
    def __init__(self):
        super().__init__('', '')

    def present(self, schema=None):
        pass
