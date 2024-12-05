import unittest

from tests.test_doubles.presenters import PresenterSpy
from use_cases.present_help_message import PresentHelpMessageUseCase


class PresentHelpMessageTestTemplate(unittest.TestCase):
    def setUp(self):
        self.presenter = PresenterSpy()
        self.help_message_presenter = (
            PresentHelpMessageUseCase("client.py", "My client", self.presenter))
