import unittest

from adapters.no_argument_marshaler_factory import NoArgumentMarshalerFactory
from entities.argument_schema import ArgumentSchemaElement
from tests.test_doubles.presenters import PresenterSpy
from use_cases.parse_arguments import ParseArgumentsUseCase
from use_cases.present_help_message import PresentHelpMessageUseCase


class PresentHelpMessageUseCaseTests(unittest.TestCase):
    def setUp(self):
        self.presenter = PresenterSpy()

    def test_wrapped_long_description(self):
        use_case = PresentHelpMessageUseCase('client.py', ""
            "Two roads diverged in a yellow wood, And sorry I could not travel both And be one traveler, long I stood And looked down one as far as I could To where it bent in the undergrowth;\n"
            "Then took the other, as just as fair, And having perhaps the better claim, Because it was grassy and wanted wear; Though as for that the passing there Had worn them really about the same,\n"
            "And both that morning equally lay In leaves no step had trodden black. Oh, I kept the first for another day! Yet knowing how way leads on to way, I doubted if I should ever come back.\n"
            "I shall be telling this with a sigh Somewhere ages and ages hence: Two roads diverged in a wood, and I— I took the one less traveled by, And that has made all the difference.\n"
            "", self.presenter)
        use_case.present_help_message()
        self.assertEqual(""
            "usage: client.py [-h]\n"
            "\n"
            "Two roads diverged in a yellow wood, And sorry I could not travel both\n"
            "And be one traveler, long I stood And looked down one as far as I could\n"
            "To where it bent in the undergrowth; Then took the other, as just as\n"
            "fair, And having perhaps the better claim, Because it was grassy and\n"
            "wanted wear; Though as for that the passing there Had worn them really\n"
            "about the same, And both that morning equally lay In leaves no step had\n"
            "trodden black. Oh, I kept the first for another day! Yet knowing how way\n"
            "leads on to way, I doubted if I should ever come back. I shall be\n"
            "telling this with a sigh Somewhere ages and ages hence: Two roads\n"
            "diverged in a wood, and I— I took the one less traveled by, And that has\n"
            "made all the difference.\n"
            "\n"
            "optional arguments:\n"
            "  -h, --help  show this help message and exit\n", self.presenter.get_presented())

    def test_wrapped_long_argument_help(self):
        use_case = PresentHelpMessageUseCase("client.py", "My program", self.presenter)
        ParseArgumentsUseCase([ArgumentSchemaElement('f', '', long_name='frankenstein', is_required=False, description=""
            "The event on which this fiction is founded has been supposed, by Dr. Darwin, and some of the physiological writers of Germany, as not of impossible occurrence. I shall not be supposed as according the remotest degree of serious faith to such an imagination; yet, in assuming it as the basis of a work of fancy, I have not considered myself as merely weaving a series of supernatural terrors."
            )], ['-h'], NoArgumentMarshalerFactory(), use_case)
        self.assertEqual(""
            "usage: client.py [-h]\n"
            "\n"
            "My program\n"
            "\n"
            "optional arguments:\n"
            "  -h, --help          show this help message and exit\n"
            "  -f, --frankenstein  The event on which this fiction is founded has\n"
            "                      been supposed, by Dr. Darwin, and some of the\n"
            "                      physiological writers of Germany, as not of\n"
            "                      impossible occurrence. I shall not be supposed as\n"
            "                      according the remotest degree of serious faith to\n"
            "                      such an imagination; yet, in assuming it as the\n"
            "                      basis of a work of fancy, I have not considered\n"
            "                      myself as merely weaving a series of supernatural\n"
            "                      terrors.\n", self.presenter.get_presented())


if __name__ == '__main__':
    unittest.main()
