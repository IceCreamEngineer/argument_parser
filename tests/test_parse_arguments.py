import unittest

from src.argument_error import *
from src.parse_arguments import ArgumentParser
from src.argument_schema import *
from tests.templates.argument_parser_test_template import ArgumentParserTestTemplate


class ArgumentParserTests(ArgumentParserTestTemplate):
    def test_no_schema_or_arguments(self):
        args_parser = ArgumentParser([], [])
        self.assertEqual(0, args_parser.next_argument())

    def test_no_schema_one_argument(self):
        try:
            ArgumentParser([], ['-x'])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.UNEXPECTED_ARGUMENT, 'x')

    def test_no_schema_multiple_arguments(self):
        try:
            ArgumentParser([], ['-x', '-y'])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.UNEXPECTED_ARGUMENT, 'x')

    def test_non_letter_schema(self):
        try:
            ArgumentParser([(ArgumentSchemaElement('*', ''))], [])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.INVALID_ARGUMENT_NAME, '*')

    def test_non_letter_long_name(self):
        try:
            ArgumentParser([(ArgumentSchemaElement('x', '', long_name='**'))], [])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.INVALID_ARGUMENT_NAME, '**')

    def test_invalid_argument_format(self):
        try:
            ArgumentParser([(ArgumentSchemaElement('f', '~'))], [])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.INVALID_ARGUMENT_FORMAT, 'f')

    def test_missing_required_argument_for_no_arguments(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', '*')], [])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT)

    def test_missing_required_argument_for_some_argument(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', ''), ArgumentSchemaElement('y', '')], ['-x'])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT, 'y')

    def test_missing_optional_argument_for_no_arguments(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', '', is_required=False)], [])
        except ArgumentError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_missing_optional_argument_for_some_argument(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', ''), ArgumentSchemaElement('y', '', is_required=False)], ['-x'])
        except ArgumentError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_extra_arguments_that_look_like_flags(self):
        argument_parser = ArgumentParser(
            [ArgumentSchemaElement('x', ''), ArgumentSchemaElement('y', '', is_required=False)],
            ['-x', 'alpha', '-y', 'alpha'])
        self.assertTrue(argument_parser.has('x'))
        self.assertFalse(argument_parser.has('y'))
        self.assertEqual(0, argument_parser.next_argument())


if __name__ == '__main__':
    unittest.main()
