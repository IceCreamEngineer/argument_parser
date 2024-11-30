from ports.presenter import Presenter


class PresenterSpy(Presenter):
    def __init__(self):
        self._presented = ""

    def present(self, message):
        self._presented += message

    def get_presented(self):
        return self._presented
