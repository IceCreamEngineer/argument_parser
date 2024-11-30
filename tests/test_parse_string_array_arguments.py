import unittest

from entities.argument_error import *
from entities.argument_schema import ArgumentSchemaElement
from use_cases.parse_arguments import ParseArgumentsUseCase
from adapters.strings_argument_marshaler_factory import StringsArgumentMarshalerFactory
from tests.templates.argument_parser_test_template import ParseArgumentsTestTemplate


class ParseStringArrayArgumentsTests(ParseArgumentsTestTemplate):
    def setUp(self):
        super().setUp()
        self.am_factory = StringsArgumentMarshalerFactory()

    def test_string_array(self):
        argument_parser = ParseArgumentsUseCase([(ArgumentSchemaElement('x', '[*]'))], ['-x', 'alpha'], self.am_factory, self.present_help_message_use_case)
        self.assertTrue(argument_parser.has('x'))
        result = argument_parser.get_value_of(('x', ''))
        self.assertEqual(1, len(result))
        self.assertEqual('alpha', result[0])

    def test_missing_string_array_element(self):
        try:
            ParseArgumentsUseCase([(ArgumentSchemaElement('x', '[*]'))], ['-x'], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_STRING, 'x')

    def test_many_string_elements(self):
        argument_parser = ParseArgumentsUseCase([(ArgumentSchemaElement('x', '[*]'))],
                                                ['-x', 'alpha', '-x', 'beta', '-x', 'gamma'], self.am_factory, self.present_help_message_use_case)
        self.assertTrue(argument_parser.has('x'))
        result = argument_parser.get_value_of(('x', ''))
        self.assertEqual(3, len(result))
        self.assertEqual('alpha', result[0])
        self.assertEqual('beta', result[1])
        self.assertEqual('gamma', result[2])

    def test_present_help_with_flag_value(self):
        ParseArgumentsUseCase([ArgumentSchemaElement('x', '[*]', long_name='excelsior', description='My arg')],
            ['-h'], self.am_factory, self.present_help_message_use_case)
        self.assertEqual(""
             "usage: client.py [-h] -x EXCELSIOR\n"
             "\n"
             "My client\n"
             "\n"
             "optional arguments:\n"
             "  -h, --help                 show this help message and exit\n"
             "  -x, --excelsior EXCELSIOR  My arg\n", self.presenter.get_presented())


if __name__ == '__main__':
    unittest.main()
