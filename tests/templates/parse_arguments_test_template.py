from tests.templates.present_help_message_test_template import PresentHelpMessageTestTemplate


class ParseArgumentsTestTemplate(PresentHelpMessageTestTemplate):
    def assert_correct_argument_error(self, e, expected_error_code, expected_argument_id=None):
        self.assertEqual(expected_error_code, e.get_error_code())
        if expected_argument_id:
            self.assertEqual(expected_argument_id, e.get_error_argument_id())
