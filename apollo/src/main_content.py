from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.src.tabs import LibraryTab


class MainContent:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()
        self.LibraryTab = LibraryTab(ui)

    def setupUI(self):
        # TODO save initial states into a temporary dump
        pass
