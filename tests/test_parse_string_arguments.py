import unittest

from entities.argument_error import *
from use_cases.parse_arguments import ParseArgumentsUseCase
from entities.argument_schema import ArgumentSchemaElement
from adapters.strings_argument_marshaler_factory import StringsArgumentMarshalerFactory
from tests.templates.parse_arguments_test_template import ParseArgumentsTestTemplate


class ParseStringArgumentsUseCaseTests(ParseArgumentsTestTemplate):
    def setUp(self):
        super().setUp()
        self.am_factory = StringsArgumentMarshalerFactory()

    def test_simple_string_present(self):
        argument_parser = ParseArgumentsUseCase([(ArgumentSchemaElement('x', '*'))], ['-x', 'param'], self.am_factory, self.help_message_presenter)
        self.assertTrue(argument_parser.has("x"))

    def test_long_string_name(self):
        argument_parser = ParseArgumentsUseCase(
            [ArgumentSchemaElement('x', '*', long_name='excelsior')], ['--excelsior', 'alpha'], self.am_factory, self.help_message_presenter)
        self.assertTrue(argument_parser.has('excelsior'))
        self.assertEqual('alpha', argument_parser.get_value_of(('x', 'excelsior')))

    def test_missing_string_argument(self):
        try:
            ParseArgumentsUseCase([(ArgumentSchemaElement('x', '*'))], ['-x'], self.am_factory, self.help_message_presenter)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_STRING, 'x')

    def test_extra_arguments(self):
        argument_parser = ParseArgumentsUseCase([(ArgumentSchemaElement('y', '*'))],
                                                ['-y', 'alpha', 'beta'], self.am_factory, self.help_message_presenter)
        self.assertEqual('alpha', argument_parser.get_value_of(('y', '')))
        self.assertEqual(0, argument_parser.next_argument())

    def test_present_help_with_flag_value(self):
        ParseArgumentsUseCase([ArgumentSchemaElement('x', '*', long_name='excelsior', description='My arg')],
                              ['-h'], self.am_factory, self.help_message_presenter)
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
