from unittest import TestCase
from unittest.mock import Mock
import sys, os, time

sys.path.append(os.path.split(os.path.abspath(__file__))[0].rsplit("\\", 2)[0])
from apollo.app.apollo_TabBindings import ApolloUtility_Functions, SearchSelection_Utils, Queue_Utils
from apollo.test.testUtilities import TesterObjects, TestSuit_main
from apollo.utils import exe_time

from PyQt5 import QtWidgets, QtGui, QtCore

# TODO
#  Documnetation -> 1.12.2020

class Test_ApolloUtility_Functions(TestCase):
    """"""
    def setUp(self):
        """Constructor"""
        self.INSTANCE = ApolloUtility_Functions()
        self.INSTANCE.LoadDB(":memory:")

    def test_HeaderActionsBinding(self):
        """Test For"""
        _, View = TesterObjects.Gen_TableView()
        Model = View.model()
        Header = View.horizontalHeader()
        Actions = [(self.INSTANCE.HeaderActionsBinding(index, Model, Header)) for index in range(Model.columnCount())]

        with self.subTest("Checks if all headers sections are bounded by an action and returned"):
            returned = list(map(lambda Act: Act.text(), Actions))
            Expected = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                        '11', '12', '13', '14', '15', '16', '17', '18', '19']
            self.assertEqual(returned, Expected)

        with self.subTest("Checks if all headers sections are checked"):
            returned = list(map(lambda Act: Act.isChecked(), Actions))
            Expected =[True, True, True, True, True, True, True, True, True, True,
                       True, True, True, True, True, True, True, True, True, True]
            self.assertEqual(returned, Expected)

        with self.subTest("checks for hide functions of the header actions"):
            Actions[2].trigger()
            Actions[4].trigger()
            Actions[6].trigger()
            Actions[8].trigger()
            self.assertTrue(Header.isSectionHidden(2))
            self.assertTrue(Header.isSectionHidden(4))
            self.assertTrue(Header.isSectionHidden(6))
            self.assertTrue(Header.isSectionHidden(8))

        with self.subTest("checks for unhide functions of the header actions"):
            Actions[2].trigger()
            Actions[4].trigger()
            Actions[6].trigger()
            Actions[8].trigger()
            self.assertFalse(Header.isSectionHidden(2))
            self.assertFalse(Header.isSectionHidden(4))
            self.assertFalse(Header.isSectionHidden(6))
            self.assertFalse(Header.isSectionHidden(8))


    def test_ColumnSelection(self):
        """Test For"""
        (Raw, TableView) = TesterObjects.Gen_TableView()
        [TableView.selectRow(Row) for Row in range(0, 20, 2)]
        Expected = [(Raw[Row])[4] for Row in range(0, 20, 2)]

        with self.subTest("Integer Index"):
            Selection = self.INSTANCE.ColumnSelection(TBV = TableView, Col = 4)
            [self.assertIn(Item, Expected) for Item in Selection]

        with self.subTest("String Index"):
            Col = self.INSTANCE.LibraryManager.db_fields[4]
            Selection = self.INSTANCE.ColumnSelection(TBV = TableView, Col = Col)
            [self.assertIn(Item, Expected) for Item in Selection]

        with self.subTest("Out Of range Index"):
            Selection = self.INSTANCE.ColumnSelection(TBV = TableView, Col = 100)
            self.assertEqual(Selection, None)

    def test_GetSelectionIndexes(self):
        """Test For getting the items at selected rows in agiven TableView"""
        (Raw, TableView) = TesterObjects.Gen_TableView()
        [TableView.selectRow(Row) for Row in range(0, 20, 2)]
        Expected = [(Raw[Row]) for Row in range(0, 20, 2)]

        Selection = self.INSTANCE.GetSelectionIndexes(TBV = TableView)
        [self.assertIn(Item, Expected) for Item in Selection]


class Test_SearchSelection_Utils(TestCase):
    """"""

    def setUp(self):
        self.INSTANCE = SearchSelection_Utils()
        self.INSTANCE.LoadDB(":memory:")
        self.Data = TesterObjects.Gen_DbTable_Data()

    def test_SetGroupMarkers(self):
        """Test For"""
        TBV = Mock()
        TBV.property.return_value = 'library'
        SortTBV = QtWidgets.QTableView()
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(self.Data)

        self.INSTANCE.SetGroupMarkers(TBV, "genre", SortTBV)
        Model = SortTBV.model()
        Returned = [(Model.index(row, 0).data()).strip() for row in range(Model.rowCount())]
        [self.assertIn(Item, Returned) for Item in self.Data.get("genre")]


    def test_SearchSimilarField(self):
        """Test For"""
        Data = {key: value + value for key, value in self.Data.items()}
        Data["file_id"] = [f"file_idX{index}"for index in range(len(Data["file_id"]))]
        TBV = TesterObjects.Gen_TableView_fromData(Data)
        TBV.setProperty("DB_Table", "library")
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(Data)

        with self.subTest("Checks for empty indexes"):
            self.INSTANCE.SearchSimilarField(TBV, "genre")

        with self.subTest("Checks for indexes"):
            TBV.selectRow(10)
            TBV.selectRow(3)
            # (genreX1) used to check for addition chareacters in dataitems EG: (genreX10)
            TBV.selectRow(1)
            ind = self.INSTANCE.LibraryManager.db_fields.index("genre")

            self.INSTANCE.SearchSimilarField(TBV, "genre")
            Model = TBV.model()
            Returned = ([Model.index(Row, ind).data() for Row in range(Model.rowCount()) if not TBV.isRowHidden(Row)])

            Expected = ['genreX1', 'genreX3', 'genreX10', 'genreX11', 'genreX12', 'genreX13',
                        'genreX14', 'genreX15', 'genreX16', 'genreX17', 'genreX18', 'genreX19',
                        'genreX1', 'genreX3', 'genreX10', 'genreX11', 'genreX12', 'genreX13',
                        'genreX14', 'genreX15', 'genreX16', 'genreX17', 'genreX18', 'genreX19']
            [self.assertIn(Item, Returned) for Item in Expected]

    def test_SearchGroupTable(self):
        """Test For"""
        TBV = Mock()
        TBV.property.return_value = 'library'

        SortTBV = QtWidgets.QTableView()
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(self.Data)
        self.INSTANCE.SetGroupMarkers(TBV, "genre", SortTBV)

        with self.subTest("checks for the search terms (genreX19) in the sort table will be Present"):
            LEDT = Mock()
            LEDT.text.return_value = 'genreX19'

            self.INSTANCE.SearchGroupTable(LEDT, SortTBV)
            Model = SortTBV.model()
            Return = [Model.index(Row, 0).data().strip() for Row in range(Model.rowCount()) if not SortTBV.isRowHidden(Row)]
            self.assertEqual(Return, ["genreX19"])

        with self.subTest("checks for the search terms (genreX109) in the sort table will be absent"):
            LEDT = Mock()
            LEDT.text.return_value = 'genreX109'

            self.INSTANCE.SearchGroupTable(LEDT, SortTBV)
            Model = SortTBV.model()
            Return = [Model.index(Row, 0).data().strip() for Row in range(Model.rowCount()) if not SortTBV.isRowHidden(Row)]
            self.assertEqual(Return, [])


class Test_Queue_Utils(TestCase):
    """"""

    def setUp(self):
        self.StartTime = time.monotonic()

        self.INSTANCE = Queue_Utils()
        self.INSTANCE.LoadDB(":memory:")

        self.MAXROWS = 50
        self.Data = TesterObjects.Gen_DbTable_Data(self.MAXROWS)
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(self.Data)

        # sets UP Library Table
        self.LibraryTable = TesterObjects.Gen_TableView_fromData(self.Data)
        self.LibraryTable.setProperty("DB_Table", "library")
        self.LibraryTable.setProperty("DB_Columns", self.INSTANCE.LibraryManager.db_fields)
        self.LibraryTable.setProperty("Order", [])

        # sets UP NowPlaying Table
        self.INSTANCE.setProperty("DB_Table", "nowplaying")
        self.INSTANCE.setProperty("DB_Columns", self.INSTANCE.LibraryManager.db_fields)
        self.INSTANCE.setProperty("Order", [])

    def test_PlayNow(self):
        """Test For"""

        #the order of the files doesnt matter
        with self.subTest("check for track selection and queuing"):
            [self.LibraryTable.selectRow(row) for row in range(self.MAXROWS)]
            self.INSTANCE.PlayNow(self.LibraryTable) # call

            Expected = [f'file_idX{row}' for row in range(self.MAXROWS)]
            returned = self.INSTANCE.PlayQueue.GetQueue()
            self.assertListEqual(Expected, returned)

            self.LibraryTable.clearSelection()

        with self.subTest("check for track selection and queuing"):
            [self.LibraryTable.selectRow(row) for row in range(0, self.MAXROWS, 2)]
            self.INSTANCE.PlayNow(self.LibraryTable) # call

            Expected = [f'file_idX{row}' for row in range(0, self.MAXROWS, 2)]
            returned = self.INSTANCE.PlayQueue.GetQueue()
            self.assertListEqual(Expected, returned)

        with self.subTest("check for track selection and queuing but avoiding duplicates"):
            self.INSTANCE.PlayNow(self.LibraryTable) # call

            Expected = [f'file_idX{row}' for row in range(0, self.MAXROWS, 2)]
            returned = self.INSTANCE.PlayQueue.GetQueue()
            self.assertListEqual(Expected, returned)

    def test_QueueNext(self):
        """Test For"""
        [self.LibraryTable.selectRow(row) for row in range(0, int(self.MAXROWS / 2), 2)]
        self.INSTANCE.PlayNow(self.LibraryTable) # call
        self.LibraryTable.clearSelection()

        with self.subTest("check for track selection and queuing in a order"):
            self.LibraryTable.selectRow(31)
            self.LibraryTable.selectRow(33)
            self.INSTANCE.QueueNext(self.LibraryTable) # call

            Expected = ['file_idX0', 'file_idX31', 'file_idX33', 'file_idX2', 'file_idX4', 'file_idX6',
                        'file_idX8', 'file_idX10', 'file_idX12', 'file_idX14', 'file_idX16', 'file_idX18',
                        'file_idX20', 'file_idX22', 'file_idX24']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            self.assertListEqual(Expected, returned)


        with self.subTest("check for track selection and queuing in a order without dupes"):
            [self.LibraryTable.selectRow(row) for row in range(0, int(self.MAXROWS / 2), 2)]
            self.LibraryTable.selectRow(31)
            self.LibraryTable.selectRow(33)

            self.INSTANCE.QueueNext(self.LibraryTable) # call

            Expected = ['file_idX0', 'file_idX31', 'file_idX33', 'file_idX2', 'file_idX4', 'file_idX6',
                        'file_idX8', 'file_idX10', 'file_idX12', 'file_idX14', 'file_idX16', 'file_idX18',
                        'file_idX20', 'file_idX22', 'file_idX24']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            self.assertListEqual(Expected, returned)

    def test_QueueLast(self):
        """Test For"""
        [self.LibraryTable.selectRow(row) for row in range(0, int(self.MAXROWS / 2), 2)]
        self.INSTANCE.PlayNow(self.LibraryTable) # call
        self.LibraryTable.clearSelection()

        with self.subTest("check for track selection and queuing in a order"):
            self.LibraryTable.selectRow(31)
            self.LibraryTable.selectRow(33)
            self.INSTANCE.QueueLast(self.LibraryTable) # call

            Expected = ['file_idX0', 'file_idX2', 'file_idX4', 'file_idX6', 'file_idX8',
                        'file_idX10', 'file_idX12', 'file_idX14', 'file_idX16', 'file_idX18',
                        'file_idX20', 'file_idX22', 'file_idX24', 'file_idX31', 'file_idX33']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            self.assertListEqual(Expected, returned)


        with self.subTest("check for track selection and queuing in a order without dupes"):
            [self.LibraryTable.selectRow(row) for row in range(0, int(self.MAXROWS / 2), 2)]
            self.LibraryTable.selectRow(31)
            self.LibraryTable.selectRow(33)

            self.INSTANCE.QueueLast(self.LibraryTable) # call

            Expected = ['file_idX0', 'file_idX2', 'file_idX4', 'file_idX6', 'file_idX8',
                        'file_idX10', 'file_idX12', 'file_idX14', 'file_idX16', 'file_idX18',
                        'file_idX20', 'file_idX22', 'file_idX24', 'file_idX31', 'file_idX33']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            self.assertListEqual(Expected, returned)


    def test_PlayAllShuffled(self):
        """Test For"""
        [self.LibraryTable.selectRow(row) for row in range(0, int(self.MAXROWS / 2), 2)]

        with self.subTest("check for track selection and queuing in a shuffled order"):
            self.INSTANCE.PlayAllShuffled(self.LibraryTable) # call

            Expected = ['file_idX0', 'file_idX2', 'file_idX4', 'file_idX6', 'file_idX8',
                        'file_idX10', 'file_idX12', 'file_idX14', 'file_idX16', 'file_idX18',
                        'file_idX20', 'file_idX22', 'file_idX24']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]


        with self.subTest("check for track selection and queuing in a shuffled order without dupes"):
            self.INSTANCE.PlayAllShuffled(self.LibraryTable) # call
            Expected = ['file_idX0', 'file_idX2', 'file_idX4', 'file_idX6', 'file_idX8',
                        'file_idX10', 'file_idX12', 'file_idX14', 'file_idX16', 'file_idX18',
                        'file_idX20', 'file_idX22', 'file_idX24']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]


    def test_PlayArtist(self):
        """Test For selecting artist similar to the artist selected in the table"""
        Data = {key: value + value for key, value in self.Data.items()}
        Data["file_id"] = [f"file_idX{(index + self.MAXROWS)}"for index in range(len(Data["file_id"]))]
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(Data)
        self.INSTANCE.LibraryManager.Refresh_TableModelData(self.LibraryTable)

        self.LibraryTable.selectRow(3)

        with self.subTest("check for track selection and queuing in a shuffled order"):
            self.INSTANCE.PlayArtist(self.LibraryTable) # call

            Expected = ['file_idX103', 'file_idX3', 'file_idX53']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]

        with self.subTest("check for track selection and queuing in a shuffled order without dupes"):
            self.INSTANCE.PlayArtist(self.LibraryTable) # call
            Expected = ['file_idX103', 'file_idX3', 'file_idX53']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]


    def test_PlayAlbumNow(self):
        """Test For selecting artist similar to the artist selected in the table"""
        Data = {key: value + value for key, value in self.Data.items()}
        Data["file_id"] = [f"file_idX{(index + self.MAXROWS)}"for index in range(len(Data["file_id"]))]
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(Data)
        self.INSTANCE.LibraryManager.Refresh_TableModelData(self.LibraryTable)

        self.LibraryTable.selectRow(3)

        with self.subTest("check for track selection and queuing in a shuffled order"):
            self.INSTANCE.PlayAlbumNow(self.LibraryTable) # call
            Expected = ['file_idX103', 'file_idX3', 'file_idX53']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]

        with self.subTest("check for track selection and queuing in a shuffled order without dupes"):
            self.INSTANCE.PlayAlbumNow(self.LibraryTable) # call
            Expected = ['file_idX103', 'file_idX3', 'file_idX53']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]


    def test_PlayGenre(self):
        """Test For selecting artist similar to the artist selected in the table"""
        Data = {key: value + value for key, value in self.Data.items()}
        Data["file_id"] = [f"file_idX{(index + self.MAXROWS)}"for index in range(len(Data["file_id"]))]
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(Data)
        self.INSTANCE.LibraryManager.Refresh_TableModelData(self.LibraryTable)

        self.LibraryTable.selectRow(3)

        with self.subTest("check for track selection and queuing in a shuffled order"):
            self.INSTANCE.PlayGenre(self.LibraryTable) # call
            Expected = ['file_idX103', 'file_idX3', 'file_idX53']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]

        with self.subTest("check for track selection and queuing in a shuffled order without dupes"):
            self.INSTANCE.PlayGenre(self.LibraryTable) # call
            Expected = ['file_idX103', 'file_idX3', 'file_idX53']
            returned = self.INSTANCE.PlayQueue.GetQueue()
            [self.assertIn(Item, returned) for Item in Expected]


    def test_QueueAlbumNext(self):
        """Test For"""
        Data = {key: value + value for key, value in self.Data.items()}
        Data["file_id"] = [f"file_idX{(index + self.MAXROWS)}"for index in range(len(Data["file_id"]))]
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(Data)
        self.INSTANCE.LibraryManager.Refresh_TableModelData(self.LibraryTable)

        self.LibraryTable.selectRow(3)
        self.INSTANCE.PlayAlbumNow(self.LibraryTable) # call

        with self.subTest("check for track selection and queuing in a shuffled order"):
            Expected = ['file_idX103', 'file_idX104', 'file_idX4', 'file_idX54', 'file_idX3', 'file_idX53']
            self.LibraryTable.selectRow(4)
            self.INSTANCE.QueueAlbumNext(self.LibraryTable) # call
            self.assertListEqual(Expected, self.INSTANCE.PlayQueue.GetQueue())

        with self.subTest("check for track selection and queuing in a shuffled order withpout Dupes"):
            Expected = ['file_idX103', 'file_idX104', 'file_idX4', 'file_idX54', 'file_idX3', 'file_idX53']
            self.LibraryTable.selectRow(4)
            self.INSTANCE.QueueAlbumNext(self.LibraryTable) # call
            self.assertListEqual(Expected, self.INSTANCE.PlayQueue.GetQueue())


    def test_QueueAlbumLast(self):
        """Test For"""
        Data = {key: value + value for key, value in self.Data.items()}
        Data["file_id"] = [f"file_idX{(index + self.MAXROWS)}"for index in range(len(Data["file_id"]))]
        self.INSTANCE.LibraryManager.BatchInsert_Metadata(Data)
        self.INSTANCE.LibraryManager.Refresh_TableModelData(self.LibraryTable)

        self.LibraryTable.selectRow(3)
        self.INSTANCE.PlayAlbumNow(self.LibraryTable) # call

        with self.subTest("check for track selection and queuing in a shuffled order"):
            Expected = ['file_idX103', 'file_idX3', 'file_idX53', 'file_idX104', 'file_idX4', 'file_idX54']
            self.LibraryTable.selectRow(4)
            self.INSTANCE.QueueAlbumLast(self.LibraryTable) # call
            self.assertListEqual(Expected, self.INSTANCE.PlayQueue.GetQueue())

        with self.subTest("check for track selection and queuing in a shuffled order withpout Dupes"):
            Expected = ['file_idX103', 'file_idX3', 'file_idX53', 'file_idX104', 'file_idX4', 'file_idX54']
            self.LibraryTable.selectRow(4)
            self.INSTANCE.QueueAlbumLast(self.LibraryTable) # call
            self.assertListEqual(Expected, self.INSTANCE.PlayQueue.GetQueue())


if __name__ == "__main__":
    App = QtWidgets.QApplication([])
    Suite = TestSuit_main()
    Suite.AddTest(Test_ApolloUtility_Functions)
    Suite.AddTest(Test_SearchSelection_Utils)
    Suite.AddTest(Test_Queue_Utils)
    Suite.Run(True)
