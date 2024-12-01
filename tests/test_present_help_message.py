import unittest

from tests.test_doubles.presenters import PresenterSpy
from use_cases.present_help_message import PresentHelpMessageUseCase


class PresentHelpMessageUseCaseTests(unittest.TestCase):
    def test_wrapped_long_description(self):
        presenter = PresenterSpy()
        use_case = PresentHelpMessageUseCase('client.py', ""
            "Two roads diverged in a yellow wood, And sorry I could not travel both And be one traveler, long I stood And looked down one as far as I could To where it bent in the undergrowth;\n"
            "Then took the other, as just as fair, And having perhaps the better claim, Because it was grassy and wanted wear; Though as for that the passing there Had worn them really about the same,\n"
            "And both that morning equally lay In leaves no step had trodden black. Oh, I kept the first for another day! Yet knowing how way leads on to way, I doubted if I should ever come back.\n"
            "I shall be telling this with a sigh Somewhere ages and ages hence: Two roads diverged in a wood, and I— I took the one less traveled by, And that has made all the difference.\n"
            "", presenter)
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
            "  -h, --help  show this help message and exit\n", presenter.get_presented())


if __name__ == '__main__':
    unittest.main()
