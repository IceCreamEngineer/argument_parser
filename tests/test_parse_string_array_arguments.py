import unittest

from src.argument_error import *
from src.argument_schema import ArgumentSchemaElement
from src.parse_arguments import ArgumentParser
from tests.templates.argument_parser_test_template import ArgumentParserTestTemplate


class StringArrayArgumentParserTests(ArgumentParserTestTemplate):
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


if __name__ == '__main__':
    unittest.main()
