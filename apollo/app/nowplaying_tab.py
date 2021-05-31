import sys

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from apollo.utils import PlayingQueue, exe_time
from apollo.app.dataproviders import SQLTableModel

class NowPlayingQueue(SQLTableModel):
    """
    Info: Utilities for data and communication between tabs
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self):
        """
        Info: Constructor
        Args: None
        Returns: None
        Errors: None
        """
        super().__init__()
        self.PlayingQueue = PlayingQueue()

    def Get_columnData(self, Column):
        """
        Info: Gets Data grom the model
        Args:
        Column: int
            -> index of the column to get data from

        Returns: List
        Errors: None
        """
        return self.Data_atIndex(Rows = list(range(self.rowCount())), Columns = [Column])

    def PlayNow(self, Indexes):
        """
        Info: Gets selected indexes from View and adds to model
        Args:
        View: QtTableView
            -> view to get data from

        Returns: None
        Errors: None
        """
        Indexes = self.Data_atIndex(Indexes = Indexes, Columns = [0])
        self.DBManager.CreateView("nowplaying", Indexes)
        self.RefreshData()

        self.PlayingQueue.RemoveElements()
        self.PlayingQueue.AddElements(self.Get_columnData(0))

    def PlayShuffled(self, Indexes):
        """
        Info: Gets selected indexes from View and adds Shuffled Data to model
        Args:
        View: QtTableView
            -> view to get data from

        Returns: None
        Errors: None
        """
        Indexes = self.Data_atIndex(Indexes = Indexes, Columns = [0])
        self.DBManager.CreateView("nowplaying", Indexes, Shuffled = True)
        self.RefreshData()

        self.PlayingQueue.RemoveElements()
        self.PlayingQueue.AddElements(self.Get_columnData(0))

    def PlayArtist(self, Indexes):
        """
        Info: Gets selected Artists from View and adds to model
        Args:
        View: QtTableView
            -> view to get data from

        Returns: None
        Errors: None
        """
        Indexes = self.Data_atIndex(Indexes = Indexes,Columns = [self.DB_FIELDS.index('artist')])
        self.DBManager.CreateView("nowplaying", Indexes, FilterField  = 'artist', Filter = True)
        self.RefreshData()

        self.PlayingQueue.RemoveElements()
        self.PlayingQueue.AddElements(self.Get_columnData(0))

    def PlayAlbum(self, Indexes):
        """
        Info: Gets selected Album from View and adds to model
        Args:
        View: QtTableView
            -> view to get data from

        Returns: None
        Errors: None
        """
        Indexes = self.Data_atIndex(Indexes = Indexes,Columns = [self.DB_FIELDS.index('album')])
        self.DBManager.CreateView("nowplaying", Indexes, FilterField  = 'album', Filter = True)
        self.RefreshData()

        self.PlayingQueue.RemoveElements()
        self.PlayingQueue.AddElements(self.Get_columnData(0))

    def PlayGenre(self, Indexes):
        """
        Info: Gets selected genre from View and adds to model
        Args:
        View: QtTableView
            -> view to get data from

        Returns: None
        Errors: None
        """
        Indexes = self.Data_atIndex(Indexes = Indexes,Columns = [self.DB_FIELDS.index('genre')])
        self.DBManager.CreateView("nowplaying", Indexes, FilterField  = 'genre', Filter = True)
        self.RefreshData()

        self.PlayingQueue.RemoveElements()
        self.PlayingQueue.AddElements(self.Get_columnData(0))

    def QueueNext(self, Indexes):
        """
        Info: Gets selected indexes from View and queues to model
        Args:
        View: QtTableView
            -> view to get data from

        Returns: None
        Errors: None
        """
        NewIndexes = self.Data_atIndex(Indexes = Indexes, Columns = [0])
        self.PlayingQueue.AddNext(NewIndexes)
        Indexes = self.PlayingQueue.GetQueue()
        self.DBManager.CreateView("nowplaying", Indexes)
        self.OrderTable(Indexes)

    def QueueLast(self, Indexes):
        """
        Info: Gets selected indexes from View and queues to model
        Args:
        View: QtTableView
            -> view to get data from

        Returns: None
        Errors: None
        """
        NewIndexes = self.Data_atIndex(Indexes = Indexes, Columns = [0])
        self.PlayingQueue.AddElements(NewIndexes)
        Indexes = self.PlayingQueue.GetQueue()
        self.DBManager.CreateView("nowplaying", Indexes)
        self.OrderTable(Indexes)


class NowPlayingTab:
    """
    Info: Now PLaying Tab
    Args: None
    Returns: None
    Errors: None
    """
    def __init__(self, UI):
        """
        Info: constructor
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
        self.MainModel = NowPlayingQueue()
        self.MainModel.LoadTable("nowplaying", self.MainModel.DB_FIELDS)
        self.DataProvider.AddModel(self.MainModel, "nowplaying_model")
        self.UI.NPQ_LSV_mainqueue.setModel(self.MainModel)


if __name__ == "__main__":
    from apollo.app.mainapp import ApolloExecute
    from apollo.plugins.app_theme import Theme

    Theme().LoadAppIcons("GRAY_100")
    app = ApolloExecute()
    app.Execute()
