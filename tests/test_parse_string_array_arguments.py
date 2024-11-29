import unittest

from src.argument_error import *
from src.argument_schema import ArgumentSchemaElement
from src.parse_arguments import ArgumentParser
from src.strings_argument_marshaler_factory import StringsArgumentMarshalerFactory
from tests.templates.argument_parser_test_template import ArgumentParserTestTemplate


class StringArrayArgumentParserTests(ArgumentParserTestTemplate):
    def setUp(self):
        self.am_factory = StringsArgumentMarshalerFactory()

    def test_string_array(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('x', '[*]'))], ['-x', 'alpha'], self.am_factory)
        self.assertTrue(argument_parser.has('x'))
        result = argument_parser.get_value_of(('x', ''))
        self.assertEqual(1, len(result))
        self.assertEqual('alpha', result[0])

    def test_missing_string_array_element(self):
        try:
            ArgumentParser([(ArgumentSchemaElement('x', '[*]'))], ['-x'], self.am_factory)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_STRING, 'x')

    def test_many_string_elements(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('x', '[*]'))],
            ['-x', 'alpha', '-x', 'beta', '-x', 'gamma'], self.am_factory)
        self.assertTrue(argument_parser.has('x'))
        result = argument_parser.get_value_of(('x', ''))
        self.assertEqual(3, len(result))
        self.assertEqual('alpha', result[0])
        self.assertEqual('beta', result[1])
        self.assertEqual('gamma', result[2])


if __name__ == '__main__':
    unittest.main()
