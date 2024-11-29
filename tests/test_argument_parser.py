import unittest

from src.argument_error import ArgumentError, ArgumentErrorCode
from src.argument_parser import ArgumentParser
from src.argument_schema import *


class ArgumentParserTests(unittest.TestCase):
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

    def test_simple_string_present(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('x', '*'))], ['-x', 'param'])
        self.assertTrue(argument_parser.has("x"))

    def test_long_string_name(self):
        argument_parser = ArgumentParser(
            [ArgumentSchemaElement('x', '*', long_name='excelsior')], ['--excelsior', 'alpha'])
        self.assertTrue(argument_parser.has('excelsior'))
        self.assertEqual('alpha', argument_parser.get_string(('x', 'excelsior')))

    def test_missing_string_argument(self):
        try:
            ArgumentParser([(ArgumentSchemaElement('x', '*'))], ['-x'])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_STRING, 'x')

    def test_missing_required_argument_for_no_arguments(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', '*')], [])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT)

    def test_missing_required_argument_for_some_argument(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', '*'), ArgumentSchemaElement('y', '*')], ['-x', 'alpha'])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_REQUIRED_ARGUMENT, 'y')

    def test_missing_optional_argument_for_no_arguments(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', '*', is_required=False)], [])
        except ArgumentError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_missing_optional_argument_for_some_argument(self):
        try:
            ArgumentParser([ArgumentSchemaElement('x', '*'), ArgumentSchemaElement('y', '*', is_required=False)],
                           ['-x', 'alpha'])
        except ArgumentError as e:
            self.fail(f"Unexpected exception raised: {e}")

    def test_string_array(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('x', '[*]'))], ['-x', 'alpha'])
        self.assertTrue(argument_parser.has('x'))
        result = argument_parser.get_string_array(('x', ''))
        self.assertEqual(1, len(result))
        self.assertEqual('alpha', result[0])

    def test_missing_string_array_element(self):
        try:
            ArgumentParser([(ArgumentSchemaElement('x', '[*]'))], ['-x'])
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_STRING, 'x')

    def test_many_string_elements(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('x', '[*]'))], ['-x', 'alpha', '-x', 'beta', '-x', 'gamma'])
        self.assertTrue(argument_parser.has('x'))
        result = argument_parser.get_string_array(('x', ''))
        self.assertEqual(3, len(result))
        self.assertEqual('alpha', result[0])
        self.assertEqual('beta', result[1])
        self.assertEqual('gamma', result[2])

    def test_extra_arguments(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('y', '*'))], ['-y', 'alpha', 'beta'])
        self.assertEqual('alpha', argument_parser.get_string(('y', '')))
        self.assertEqual(0, argument_parser.next_argument())

    def test_extra_arguments_that_look_like_flags(self):
        argument_parser = ArgumentParser(
            [ArgumentSchemaElement('x', ''), ArgumentSchemaElement('y', '', is_required=False)],
            ['-x', 'alpha', '-y', 'alpha'])
        self.assertTrue(argument_parser.has('x'))
        self.assertFalse(argument_parser.has('y'))
        self.assertEqual(0, argument_parser.next_argument())

    def assert_correct_argument_error(self, e, expected_error_code, expected_argument_id=None):
        self.assertEqual(expected_error_code, e.get_error_code())
        if expected_argument_id:
            self.assertEqual(expected_argument_id, e.get_error_argument_id())


if __name__ == '__main__':
    unittest.main()
