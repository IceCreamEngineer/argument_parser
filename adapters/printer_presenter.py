from ports.presenter import Presenter


class PrinterPresenter(Presenter):
    def present(self, message):
        print(message)
