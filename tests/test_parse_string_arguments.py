import unittest

from src.argument_error import *
from src.parse_arguments import ArgumentParser
from src.argument_schema import ArgumentSchemaElement
from src.strings_argument_marshaler_factory import StringsArgumentMarshalerFactory
from tests.templates.argument_parser_test_template import ArgumentParserTestTemplate


class StringArgumentParserTests(ArgumentParserTestTemplate):
    def setUp(self):
        self.am_factory = StringsArgumentMarshalerFactory()

    def test_simple_string_present(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('x', '*'))], ['-x', 'param'], self.am_factory)
        self.assertTrue(argument_parser.has("x"))

    def test_long_string_name(self):
        argument_parser = ArgumentParser(
            [ArgumentSchemaElement('x', '*', long_name='excelsior')], ['--excelsior', 'alpha'], self.am_factory)
        self.assertTrue(argument_parser.has('excelsior'))
        self.assertEqual('alpha', argument_parser.get_value_of(('x', 'excelsior')))

    def test_missing_string_argument(self):
        try:
            ArgumentParser([(ArgumentSchemaElement('x', '*'))], ['-x'], self.am_factory)
            self.fail()
        except ArgumentError as e:
            self.assert_correct_argument_error(e, ArgumentErrorCode.MISSING_STRING, 'x')

    def test_extra_arguments(self):
        argument_parser = ArgumentParser([(ArgumentSchemaElement('y', '*'))],
            ['-y', 'alpha', 'beta'], self.am_factory)
        self.assertEqual('alpha', argument_parser.get_value_of(('y', '')))
        self.assertEqual(0, argument_parser.next_argument())


if __name__ == '__main__':
    unittest.main()
