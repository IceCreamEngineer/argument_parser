import unittest

from src.argument_error import *
from src.parse_arguments import ArgumentParser
from src.argument_schema import ArgumentSchemaElement
from tests.templates.argument_parser_test_template import ArgumentParserTestTemplate


class StringArgumentParserTests(ArgumentParserTestTemplate):
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


if __name__ == '__main__':
    unittest.main()
