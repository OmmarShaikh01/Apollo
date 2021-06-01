import sys

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QPoint, QRect, QSize, Qt

from apollo.utils import PlayingQueue, exe_time
from apollo.app.dataproviders import SQLTableModel
from apollo.gui.ui_NPQ_delegate import Ui_NPQ_WDG_delegate
from apollo.db import DBFIELDS

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


class NPQDelegate_WDG():

    def __init__(self): ...
    def paint(self, option, painter: QtGui.QPainter, *items):
        Rect = option.rect
        Rect.setWidth(Rect.width()-4)
        painter.save()

        # main
        # painter.drawRect(Rect)

        # cover
        TempRec = QRect(Rect.x() + 4, Rect.y() + 4, 56, 56)
        # painter.drawRect(TempRec)
        painter.drawImage(TempRec, QtGui.QImage(':/icon_pack/png/64/music_icon-02.png'))



        painter.restore()


class NowPlaying_ItemDelegate(QtWidgets.QStyledItemDelegate):
    """
    Delegate calss for the NPQ which interfaces with the model
    """
    def __init__(self, Model):
        """
        Class Constructor

        Parameters
        ----------
        Model : QtGui.QStandardItemModel
            Modle to load data from
        """
        super().__init__()
        self._model = Model
        self._style = QtWidgets.QApplication.style()
        self._option = None
        self._painter = None

    def setDataModel(self, Value):
        """
        Setter for the DataModel

        Parameters
        ----------
        Value : QtGui.QStandardItemModel
            DataModel
        """
        self._model = Value

    def setFields(self, T, M, B1, B2, B3):
        self.Fields = [DBFIELDS.index(F) for F in [T, M, B1, B2, B3]]

    def getData(self, index):
        Row = index.row()
        return [self._model.index(Row, Col).data() for Col in self.Fields]

    def DrawWidget(self, Painter, Option, Index):
        Painter.setPen(QtGui.QColor("#c6c6c6"))
        self._style.drawPrimitive(self._style.PE_PanelItemViewItem, Option, Painter, Option.widget)

        items = self.getData(Index)
        self.DrawCover(Painter, Option)
        self.DrawTop(Painter, Option, items[0])
        self.DrawMid(Painter, Option, items[1])
        self.DrawBottom(Painter, Option, [items[2], items[3], items[4]])

        Painter.setPen(QtGui.QColor("#393939"))
        Painter.drawLine(QPoint(0, Option.rect.y() + 64), QPoint(Option.rect.width(), Option.rect.y() + 64))

    def DrawCover(self, Painter, Options):
        self._style.subElementRect(self._style.SE_ItemViewItemDecoration, Options, Options.widget)
        Rect = Options.rect
        TempRec = QRect(Rect.x() + 4, Rect.y() + 4, 56, 56)
        Painter.drawImage(TempRec, QtGui.QImage(':/icon_pack/png/64/music_icon-02.png'))


    def DrawTop(self, Painter, Options, item):
        Rect = Options.rect
        TempRec = QRect(Rect.x() + 64, Rect.y() + 4, Rect.width() - 68, 16)
        Painter.drawText(TempRec, item)

    def DrawMid(self, Painter, Options, item):
        Rect = Options.rect
        TempRec = QRect(Rect.x() + 64, Rect.y() + 24, Rect.width() - 68, 16)
        Painter.drawText(TempRec, item)

    def DrawBottom(self, Painter, Options, items):
        Rect = Options.rect
        Width = round((Rect.width() - 72) / 3)
        # 1
        TempRec = QRect(Rect.x() + 64, Rect.y() + 44, Width, 16)
        Painter.drawText(TempRec, items[0])
        # 2
        TempRec = QRect(Rect.x() + (64 + Width + 4), Rect.y() + 44, Width, 16)
        Painter.drawText(TempRec, items[1])
        # 3
        TempRec = QRect(Rect.x() + (64 + Width + 4 + Width + 4), Rect.y() + 44, Width - 4, 16)
        Painter.drawText(TempRec, items[2])

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index):
        painter.save()
        self.DrawWidget(painter, option, index)
        painter.restore()

    def sizeHint(self, option, index):
        return (QSize(option.rect.height(), 64))

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

        self.Delegate = NowPlaying_ItemDelegate(self.MainModel)
        self.Delegate.setFields("artist", "title", "length", "filesize", "bitrate")

        self.UI.NPQ_LSV_mainqueue.setItemDelegate(self.Delegate)


if __name__ == "__main__":
    from apollo.app.mainapp import ApolloExecute
    from apollo.plugins.app_theme.GRAY_100 import *

    app = ApolloExecute()
    app.Execute()
