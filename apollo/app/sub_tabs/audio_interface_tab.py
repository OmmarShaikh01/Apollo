from __future__ import annotations

from typing import TYPE_CHECKING

from apollo.database.models import Model_Provider
from apollo.utils import Apollo_Generic_View, Apollo_Global_Signals


if TYPE_CHECKING:
    from apollo.app.main import Apollo_MainWindow_UI


class Audio_Interface_Tab(Apollo_Generic_View):
    def __init__(self, ui: Apollo_MainWindow_UI):
        self.SIGNALS = Apollo_Global_Signals()
        self.UI = ui
        self.MODEL_PROVIDER = Model_Provider

    def setup_conections(self):
        pass

    def setup_defaults(self):
        pass

    def save_states(self):
        pass
