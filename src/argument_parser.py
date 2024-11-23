from src.argument_error import ArgumentError, ArgumentErrorCode
from src.no_argument_marshaler import NoArgumentMarshaler
from src.string_argument_marshaler import StringArgumentMarshaler
from src.string_array_argument_marshaler import StringArrayArgumentMarshaler


class ArgumentParser:
    def __init__(self, schema, arguments):
        self._marshalers = {}
        self._arguments_found = set()
        self._current_argument = None
        self._parse_schema(schema)
        self._parse_arguments(arguments)

    def _parse_schema(self, schema):
        for element in schema.split(','):
            if len(element) > 0:
                self._parse_schema_element(element.strip())

    def _parse_schema_element(self, element):
        element_id = element[0]
        element_tail = element[1:]
        self._validate_schema_element_id(element_id)
        self._set_marshaler(element_id, element_tail)

    def _set_marshaler(self, element_id, element_tail):
        if len(element_tail) == 0:
            self._marshalers[element_id] = NoArgumentMarshaler()
        elif element_tail == '*':
            self._marshalers[element_id] = StringArgumentMarshaler()
        elif element_tail == '[*]':
            self._marshalers[element_id] = StringArrayArgumentMarshaler()
        else:
            raise ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_FORMAT, element_id)

    @staticmethod
    def _validate_schema_element_id(element_id):
        if not element_id.isalpha():
            raise ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_NAME, element_id)

    def _parse_arguments(self, arguments):
        self._current_argument = iter(arguments)
        while True:
            try:
                argument = next(self._current_argument)
                if argument.startswith('-'):
                    self._parse_argument_characters(argument[1:])
                else:
                    argument_index = arguments.index(argument)
                    arguments.pop(argument_index)
                    self._current_argument = iter(arguments)
                    break
            except StopIteration:
                break

    def _parse_argument_characters(self, argument_characters):
        for i in range(len(argument_characters)):
            self._parse_argument_character(argument_characters[i])

    def _parse_argument_character(self, argument_character):
        if argument_character not in self._marshalers:
            raise ArgumentError(ArgumentErrorCode.UNEXPECTED_ARGUMENT, argument_character)
        self._arguments_found.add(argument_character)
        try:
            self._marshalers[argument_character].set(self._current_argument)
        except ArgumentError as e:
            e.set_error_argument_id(argument_character)
            raise e

    def has(self, argument):
        return argument in self._arguments_found

    def next_argument(self):
        return 0 if len(self._arguments_found) == 0 else len(self._arguments_found) - 1

    def get_string(self, argument):
        return StringArgumentMarshaler.get_value(self._marshalers[argument])

    def get_string_array(self, argument):
        return StringArrayArgumentMarshaler.get_value(self._marshalers[argument])
