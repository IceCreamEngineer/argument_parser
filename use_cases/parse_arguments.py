from entities.argument_error import ArgumentError, ArgumentErrorCode


class ParseArgumentsUseCase:
    def __init__(self, schema, arguments, argument_marshaler_factory, present_help_message_use_case):
        self._argument_marshaler_factory = argument_marshaler_factory
        self._present_help_message_use_case = present_help_message_use_case
        self._initialize_members()
        self._try_to_parse(schema, arguments)

    def _initialize_members(self):
        self._marshalers = {}
        self._arguments_found = set()
        self._current_argument = None

    def _try_to_parse(self, schema, arguments):
        try:
            self._parse(schema, arguments)
        except PresentHelp:
            self._present_help_message_use_case.present_help_message(schema)
            return

    def _parse(self, schema, arguments):
        self._parse_schema(schema)
        self._parse_arguments(arguments)
        self._check_for_required_arguments_from(schema)

    def _parse_schema(self, schema):
        for element in schema:
            self._parse_schema_element(element)

    def _parse_schema_element(self, element):
        self._validate(element)
        self._set_marshaler_for(element)

    def _validate(self, element):
        long_name_is_alphabetic = self.is_long_name_alphabetic_for(element)
        if not element.name.isalpha() or not long_name_is_alphabetic:
            raise ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_NAME,
                element.name if long_name_is_alphabetic else element.long_name)

    @staticmethod
    def is_long_name_alphabetic_for(element):
        long_name = element.long_name
        if '_' in element.long_name or '-' in element.long_name:
            long_name = long_name.replace('_', '').replace('-', '')
        return long_name.isalpha() or not element.long_name

    def _set_marshaler_for(self, element):
        marshaler = self._make_marshaler_from(element)
        self._marshalers[(element.name, element.long_name)] = marshaler

    def _make_marshaler_from(self, element):
        if element.argument_type in self._argument_marshaler_factory.get_argument_types():
            return self._argument_marshaler_factory.create_from(element.argument_type)
        raise ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_FORMAT, element.name)

    def _parse_arguments(self, arguments):
        self._current_argument = iter(arguments)
        while True:
            if not self._iterating_through(arguments):
                break

    def _iterating_through(self, arguments):
        try:
            return self._iterate_through(arguments)
        except StopIteration:
            return False

    def _iterate_through(self, arguments):
        argument = next(self._current_argument)
        is_argument_name = argument.startswith(('--', '-'))
        self._check_to_parse(argument, arguments, is_argument_name)
        return is_argument_name

    def _check_to_parse(self, argument, arguments, is_argument_name):
        if is_argument_name:
            self._parse_argument_character(argument[2:] if argument.startswith('--') else argument[1:])
        else:
            self._backup_to_previous(argument, arguments)

    def _parse_argument_character(self, argument_character):
        matching_element_names = self._get_matching_element_names_for(argument_character)
        self._arguments_found.add(argument_character)
        self._try_to_marshal(argument_character, matching_element_names)

    def _backup_to_previous(self, argument, arguments):
        argument_index = arguments.index(argument)
        arguments.pop(argument_index)
        self._current_argument = iter(arguments)

    def _get_matching_element_names_for(self, argument_character):
        matching_element_names = [element_names for element_names in self._marshalers if argument_character in element_names]
        self._check_for_expected(argument_character, matching_element_names)
        return matching_element_names

    def _check_for_expected(self, argument_character, matching_element_names):
        if argument_character == 'h' or argument_character == 'help':
            raise PresentHelp
        if not matching_element_names:
            raise ArgumentError(ArgumentErrorCode.UNEXPECTED_ARGUMENT, argument_character)

    def _try_to_marshal(self, argument_character, matching_element_names):
        try:
            self._marshalers[matching_element_names[0]].set(self._current_argument)
        except ArgumentError as e:
            e.set_error_argument_id(argument_character)
            raise e

    def _check_for_required_arguments_from(self, schema):
        for element in schema:
            if element.is_required and not (self.has(element.name) or self.has(element.long_name)):
                raise ArgumentError(ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT, element.name)

    def has(self, argument):
        return argument in self._arguments_found

    def next_argument(self):
        return 0 if len(self._arguments_found) == 0 else len(self._arguments_found) - 1

    def get_value_of(self, argument_names):
        return self._marshalers[argument_names].get_value_from(self._marshalers[argument_names])


class PresentHelp(RuntimeWarning):
    pass
