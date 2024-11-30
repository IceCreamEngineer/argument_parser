import unittest

from entities.argument_error import *
from adapters.no_argument_marshaler_factory import NoArgumentMarshalerFactory
from use_cases.parse_arguments import ParseArgumentsUseCase
from entities.argument_schema import *
from tests.templates.argument_parser_test_template import ParseArgumentsTestTemplate


class ParseArgumentUseCaseTests(ParseArgumentsTestTemplate):
    def setUp(self):
        super().setUp()
        self.am_factory = NoArgumentMarshalerFactory()

    def test_no_schema_or_arguments(self):
        args_parser = ParseArgumentsUseCase([], [], self.am_factory, self.present_help_message_use_case)
        self.assertEqual(0, args_parser.next_argument())

    def test_no_schema_one_argument(self):
        try:
            ParseArgumentsUseCase([], ['-x'], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.UNEXPECTED_ARGUMENT, 'x')

    def test_no_schema_multiple_arguments(self):
        try:
            ParseArgumentsUseCase([], ['-x', '-y'], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.UNEXPECTED_ARGUMENT, 'x')

    def test_non_letter_schema(self):
        try:
            ParseArgumentsUseCase([(ArgumentSchemaElement('*', ''))], [], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.INVALID_ARGUMENT_NAME, '*')

    def test_non_letter_long_name(self):
        try:
            ParseArgumentsUseCase([(ArgumentSchemaElement('x', '', long_name='**'))], [], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.INVALID_ARGUMENT_NAME, '**')

    def test_invalid_argument_format(self):
        try:
            ParseArgumentsUseCase([(ArgumentSchemaElement('f', '~'))], [], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.INVALID_ARGUMENT_FORMAT, 'f')

    def test_missing_required_argument_for_no_arguments(self):
        try:
            ParseArgumentsUseCase([ArgumentSchemaElement('x', '')], [], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT)

    def test_missing_required_argument_for_some_argument(self):
        try:
            ParseArgumentsUseCase([ArgumentSchemaElement('x', ''),
                                   ArgumentSchemaElement('y', '')], ['-x'], self.am_factory, self.present_help_message_use_case)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT, 'y')

    def test_missing_optional_argument_for_no_arguments(self):
        try:
            ParseArgumentsUseCase([ArgumentSchemaElement('x', '', is_required=False)], [], self.am_factory, self.present_help_message_use_case)
        except ArgumentError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_missing_optional_argument_for_some_argument(self):
        try:
            ParseArgumentsUseCase([ArgumentSchemaElement('x', ''),
                                   ArgumentSchemaElement('y', '', is_required=False)], ['-x'], self.am_factory, self.present_help_message_use_case)
        except ArgumentError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_extra_arguments_that_look_like_flags(self):
        argument_parser = ParseArgumentsUseCase(
            [ArgumentSchemaElement('x', ''), ArgumentSchemaElement('y', '', is_required=False)],
            ['-x', 'alpha', '-y', 'alpha'], self.am_factory, self.present_help_message_use_case)
        self.assertTrue(argument_parser.has('x'))
        self.assertFalse(argument_parser.has('y'))
        self.assertEqual(0, argument_parser.next_argument())

    def test_present_help(self):
        ParseArgumentsUseCase([], ['--help'], self.am_factory, self.present_help_message_use_case)
        self.assertEqual(""
            "usage: client.py [-h]\n"
            "\n"
            "My client\n"
            "\n"
            "optional arguments:\n"
            "  -h, --help  show this help message and exit\n", self.presenter.get_presented())

    def test_present_help_with_schema(self):
        ParseArgumentsUseCase([ArgumentSchemaElement('a', '', description='My arg', is_required=False)],
                              ['-h'], self.am_factory, self.present_help_message_use_case)
        self.assertEqual(""
            "usage: client.py [-h]\n"
            "\n"
            "My client\n"
            "\n"
            "optional arguments:\n"
            "  -h, --help  show this help message and exit\n"
            "  -a          My arg\n", self.presenter.get_presented())

    def test_present_help_with_schema_and_long_name(self):
        ParseArgumentsUseCase([ArgumentSchemaElement('a', '', long_name='arg', description='My arg', is_required=False)],
                              ['-h'], self.am_factory, self.present_help_message_use_case)
        self.assertEqual(""
            "usage: client.py [-h]\n"
            "\n"
            "My client\n"
            "\n"
            "optional arguments:\n"
            "  -h, --help  show this help message and exit\n"
            "  -a, --arg   My arg\n", self.presenter.get_presented())

    def test_present_help_for_required_args(self):
        ParseArgumentsUseCase(
            [ArgumentSchemaElement('a', '', long_name='arg', description='My arg', is_required=True),
                    ArgumentSchemaElement('b', '', long_name='other_arg', description='My other arg', is_required=True)],
            ['-h'], self.am_factory, self.present_help_message_use_case)
        self.assertEqual(""
             "usage: client.py [-h] -a -b\n"
             "\n"
             "My client\n"
             "\n"
             "optional arguments:\n"
             "  -h, --help       show this help message and exit\n"
             "  -a, --arg        My arg\n"
             "  -b, --other_arg  My other arg\n", self.presenter.get_presented())


if __name__ == '__main__':
    unittest.main()
