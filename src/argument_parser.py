from src.argument_error import ArgumentError, ArgumentErrorCode
from src.no_argument_marshaler import NoArgumentMarshaler
from src.string_argument_marshaler import StringArgumentMarshaler
from src.string_array_argument_marshaler import StringArrayArgumentMarshaler


class ArgumentParser:
    def __init__(self, schema, arguments):
        self._marshalers = {}
        self._arguments_found = set()
        self._current_argument = None
        self._parse(schema, arguments)

    def _parse(self, schema, arguments):
        self._parse_schema(schema)
        self._parse_arguments(arguments)
        self._check_for_required_arguments_from(schema)

    def _parse_schema(self, schema):
        for element in schema.get_elements():
            self._parse_schema_element(element)

    def _parse_schema_element(self, element):
        element_id = (element.name, element.long_name)
        element_tail = element.type_notation
        self._validate(element)
        self._set_marshaler_for(element_id, element_tail)

    @staticmethod
    def _validate(element):
        if not element.name.isalpha():
            raise ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_NAME, element.name)

    def _set_marshaler_for(self, element_id, element_tail):
        if len(element_tail) == 0:
            self._marshalers[element_id] = NoArgumentMarshaler()
        elif element_tail == '*':
            self._marshalers[element_id] = StringArgumentMarshaler()
        elif element_tail == '[*]':
            self._marshalers[element_id] = StringArrayArgumentMarshaler()
        else:
            raise ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_FORMAT, element_id[0])

    def _parse_arguments(self, arguments):
        self._current_argument = iter(arguments)
        while True:
            try:
                argument = next(self._current_argument)
                if argument.startswith('--'):
                    self._parse_argument_character(argument[2:])
                elif argument.startswith('-'):
                    self._parse_argument_character(argument[1:])
                else:
                    argument_index = arguments.index(argument)
                    arguments.pop(argument_index)
                    self._current_argument = iter(arguments)
                    break
            except StopIteration:
                break

    def _parse_argument_character(self, argument_character):
        matching_element_names = [element_names for element_names in self._marshalers if argument_character in element_names]
        if not matching_element_names:
            raise ArgumentError(ArgumentErrorCode.UNEXPECTED_ARGUMENT, argument_character)
        self._arguments_found.add(argument_character)
        try:
            self._marshalers[matching_element_names[0]].set(self._current_argument)
        except ArgumentError as e:
            e.set_error_argument_id(argument_character)
            raise e

    def _check_for_required_arguments_from(self, schema):
        for element in schema.get_elements():
            if element.is_required and not (self.has(element.name) or self.has(element.long_name)):
                raise ArgumentError(ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT, element.name)

    def has(self, argument):
        return argument in self._arguments_found

    def next_argument(self):
        return 0 if len(self._arguments_found) == 0 else len(self._arguments_found) - 1

    def get_string(self, argument):
        return StringArgumentMarshaler.get_value(self._marshalers[argument])

    def get_string_array(self, argument):
        return StringArrayArgumentMarshaler.get_value(self._marshalers[argument])
