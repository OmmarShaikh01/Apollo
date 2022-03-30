from apollo.layout.ui_mainwindow import Ui_MainWindow as Apollo
from apollo.src.tabs import LibraryTab, PlaylistTab, NowPlayingTab


class MainContent:

    def __init__(self, ui: Apollo) -> None:
        super().__init__()
        self.ui = ui
        self.setupUI()

        self.LibraryTab = LibraryTab(ui)
        self.PlaylistTab = PlaylistTab(ui)
        self.NowPlayingTab = NowPlayingTab(ui)

    def setupUI(self):
        # TODO save initial states into a temporary dump
        pass
