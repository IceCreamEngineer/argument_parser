import unittest

from src.argument_error import ArgumentError, ArgumentErrorCode


class MyTestCase(unittest.TestCase):
    def test_unexpected_message(self):
        e = ArgumentError(ArgumentErrorCode.UNEXPECTED_ARGUMENT, 'x')
        self.assertEqual("Argument -x unexpected.", e.error_message())

    def test_missing_string_message(self):
        e = ArgumentError(ArgumentErrorCode.MISSING_STRING, 'x')
        self.assertEqual("Could not find string parameter for -x", e.error_message())

    def test_invalid_argument_name(self):
        e = ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_NAME, '#')
        self.assertEqual("'#' is not a valid argument name.", e.error_message())

    def test_invalid_format(self):
        e = ArgumentError(ArgumentErrorCode.INVALID_ARGUMENT_FORMAT, '$')
        self.assertEqual("'$' is not a valid argument format.", e.error_message())


if __name__ == '__main__':
    unittest.main()
