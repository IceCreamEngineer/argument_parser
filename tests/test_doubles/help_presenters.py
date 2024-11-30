from src.present_help import HelpPresenter


class HelpPresenterSpy(HelpPresenter):
    def __init__(self, program_filename, description):
        super().__init__(program_filename, description)
        self._presented = ""

    def present(self, schema=None):
        super().present(schema)
        self._presented = self._help_message

    def get_presented(self):
        return self._presented
