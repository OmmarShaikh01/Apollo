import sys

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from apollo.db.library_manager import DataBaseManager
from apollo.utils import exe_time
from apollo.app.dataproviders import SQLTableModel


class LibraryTab:
    """
    Info: LIbrary Tab class
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self, UI):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """
        ### Development code not production code will cause bugs if not removed
        if UI != None:
            self.UI = UI
        else:
            from apollo.app.mainapp_ux import ApolloMain
            self.UI = ApolloMain()
        ###
        self.DataProvider = self.UI.DataProvider
        self.Init_DataModels()

    def Init_DataModels(self):
        self.MainView = self.UI.LDT_TBV_maintable
        self.MainModel = SQLTableModel()
        self.MainModel.LoadTable("library", self.MainModel.DB_FIELDS)
        self.DataProvider.AddModel(self.MainModel, "library_model")
        self.MainView.setModel(self.MainModel)


if __name__ == "__main__":
    from apollo.app.mainapp import ApolloExecute
    from apollo.plugins.app_theme.GRAY_100 import *

    app = ApolloExecute()
    app.Execute()
