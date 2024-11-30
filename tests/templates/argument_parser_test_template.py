import unittest

from use_cases.present_help_message import PresentHelpMessageUseCase
from tests.test_doubles.presenters import PresenterSpy


class ParseArgumentsTestTemplate(unittest.TestCase):
    def setUp(self):
        self.presenter = PresenterSpy()
        self.present_help_message_use_case = PresentHelpMessageUseCase("client.py", "My client", self.presenter)

    def assert_correct_argument_error(self, e, expected_error_code, expected_argument_id=None):
        self.assertEqual(expected_error_code, e.get_error_code())
        if expected_argument_id:
            self.assertEqual(expected_argument_id, e.get_error_argument_id())
