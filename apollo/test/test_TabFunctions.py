from unittest import TestCase
from unittest.mock import Mock
import sys, os

sys.path.append(os.path.split(os.path.abspath(__file__))[0].rsplit("\\", 2)[0])
from apollo.app.tab_manager import ApolloTabFunctions
from apollo.test.testUtilities import TesterObjects, TestSuit_main

from PyQt5 import QtWidgets, QtGui, QtCore   

# TODO
#  Documnetation -> 1.12.2020

class Test_ApolloTabFunctions_selection(TestCase):
    """
    Class to test all the functions that get Indexes Of all the selected Items From Views and Tables
    """
    
    def setUp(self):
        """
        Initilizes the class and loads a Db in Memory
        """
        self.TabInstance = ApolloTabFunctions()
        self.TabInstance.LoadDB(":memory:")
        
    def tearDown(self):
        del self.TabInstance
        
    def test_ColumnSelection_INDEX(self):
        """
        Tests the Indexing and returing of values From inside a TBV that have been selected
        either by using index
        
        Expected Behaviour:
        Takes A TableView and Column Index or FieldName as an input and returns all the
        items that are selected in a Table.
        """
        # checks for indexing at 0 column
        (RawTable, TableView) = TesterObjects.Gen_TableView()
        TableView.selectAll()
        
        with (self.subTest("Indexing Column using Integer index")):
            ResultTable = self.TabInstance._ColumnSelection(TableView, 0)
            ExpectedTable = [row[0] for row in RawTable]
            self.assertEqual(ExpectedTable, ResultTable)
            
        with (self.subTest("Indexing Column using String Column Name")):
            field = self.TabInstance.LibraryManager.db_fields[5]
            # checks for indexing at 0 column
            ResultTable = self.TabInstance._ColumnSelection(TableView, field)
            # index column same as the index of DB fields
            ExpectedTable = [row[5] for row in RawTable]
            self.assertEqual(ExpectedTable, ResultTable)        
        
        with (self.subTest("Indexing Column using Out Of bounds")):        
            # checks for Out of bounds indexing
            ResultTable = self.TabInstance._ColumnSelection(TableView, 1000)
            self.assertEqual(None, ResultTable)


    def test_GetSelectionIndexes(self):
        """
        Used to test Data retrival from a view of all the selected Indexes
        
        Expected Behaviour:
        Takes A TableView as an input and returns all the items that are selected in a Table.
        """
        (RawTable, TableView) = TesterObjects.Gen_TableView()
        TableView.selectAll()
        ResultTable = self.TabInstance._GetSelectionIndexes(TableView)
        self.assertEqual(RawTable, ResultTable)
     
     
    def test_SetSortMarkers(self):
        """
        tests for setting the indexs of the group table
        
        Expected Behaviour
        selects a field and creates a table of all the distinct groups
        """
        
        # data and table set up and databse Data insertion 
        MainTable = Mock()
        Config = {"property.return_value": "library"}
        MainTable.configure_mock(**Config)        
        DataTable = TesterObjects.Gen_DbTable_Data(10)
        self.TabInstance.LibraryManager.BatchInsert_Metadata(DataTable)        
        
        # tests for all the fields needed for grouping
        for fields in ["artist", "album", "genre", "albumartist"]:            
            with self.subTest(f"{fields} grouping"):            
                SortTable = QtWidgets.QTableView()
                self.TabInstance.SetGroupMarkers(MainTable, f"{fields}", SortTable)        
                SortModel = SortTable.model()
                for R in range(SortModel.rowCount()):
                    for C in range(SortModel.columnCount()):
                        self.assertIn(SortModel.index(R, C).data().strip(), DataTable[f"{fields}"])                        
                self.assertEqual(SortTable.property("GROUP_BY"), fields)
                self.TabInstance.LibraryManager.ExeQuery("DELETE FROM library")
        
        # tests fro folder field
        with self.subTest(f"folders grouping"):
            DataTable = TesterObjects.Gen_DbTable_Data(10)
            Expected = [
                "E:\\Folder\\file.for", 
                "E:\\Folder\\SUBFolder\\file.for", 
                "E:\\Folder\\SUBFolder\\file.for", 
                "E:\\Folder\\file.for", 
                "E:\\Folder\\file.for", 
                "E:\\file.for", 
                "E:\\file.for", 
                "E:\\Folder\\file.for", 
                "E:\\Folder\\file.for", 
                "E:\\Folder\\file.for"                             
            ]
            DataTable["file_path"] = Expected
            self.TabInstance.LibraryManager.BatchInsert_Metadata(DataTable)        
            fields = "file_path"
            
            SortTable = QtWidgets.QTableView()
            self.TabInstance.SetGroupMarkers(MainTable, f"{fields}", SortTable)        
            SortModel = SortTable.model()
            for R in range(SortModel.rowCount()):
                for C in range(SortModel.columnCount()):
                    self.assertIn(SortModel.index(R, C).data().strip(),
                                  list(map(lambda x: os.path.split(x)[0], Expected)))                        
            self.assertEqual(SortTable.property("GROUP_BY"), fields)            
            
            
            
        
class Test_ApolloTabFunctions_Queueing(TestCase):
    """
    Tests for all track queuing and table Refreshes
    """
    
    def setUp(self):
        self.TabInstance = ApolloTabFunctions()
        self.TabInstance.LoadDB(":memory:")
        self.DataTable = TesterObjects.Gen_DbTable_Data(10)
        self.TabInstance.LibraryManager.BatchInsert_Metadata(self.DataTable)
        self.View = TesterObjects.Gen_TableView_fromData(self.DataTable)
        self.View.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        
    def tearDown(self):
        del self.TabInstance
        
    def test_PlayNow(self):
        """
        Test clearing the original queue and adding New Items to a queue
        
        Expected Behaviour:
            Clears the Queue whenever new data is added and is indexed Using File_id
        """
        
        with (self.subTest("test adding 4 Items to an empty queue")):
            [self.View.selectRow(R) for R in range(4)]
            
            # Adds items to an empty queue
            self.TabInstance.PlayNow(self.View)            
            self.View.clearSelection()
            
            # gets result from DB as items dont need order
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id"))
            Expected = self.DataTable["file_id"][:4] # checks with expected value
            self.assertEqual(Expected, Result)
            
            
        with (self.subTest("test readding last 4 Items to an filled queue")):
            [self.View.selectRow(R) for R in [6, 7, 8, 9]]
            
            # Adds new items to an filled queue
            self.TabInstance.PlayNow(self.View)            
            self.View.clearSelection()
            
            # gets result from DB as items dont need order 
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id"))    
            Expected = self.DataTable["file_id"][6:]
            self.assertEqual(Expected, Result)
            
        
    def test_QueueNext(self):
        """
        Test adding New Items to a queue after the current pointer
        
        Expected Behaviour:
            Adds Data After the Pointer in the Queue whenever new data is ready and is indexed Using File_id
        """
        
        with (self.subTest("test Queuing 4 Items to an empty queue")):
            [self.View.selectRow(R) for R in range(4)]
            # Adds items to an empty queue
            self.TabInstance.QueueNext(self.View)            
            self.View.clearSelection()
            
            # gets data from DataTable to check for data simmilarity
            Expected = self.DataTable["file_id"][:4]
            
            with (self.subTest("test Queuing 4 Items to an queue in DB")):
                Result = self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id")
                self.assertEqual(Expected, Result)
                
            with (self.subTest("test Queuing 4 Items to an queue in PlayQueue")):
                Result = self.TabInstance.PlayQueue.GetQueue()
                self.assertEqual(Expected, Result)
            
        with (self.subTest("test Queuing last 6 Items to an filled queue")):
            [self.View.selectRow(R) for R in [4, 5, 6, 7, 8, 9]]
            # Adds items after pointer to queue
            self.TabInstance.QueueNext(self.View)            
            self.View.clearSelection()
            
            # gets data from DataTable to check for data simmilarity
            Expected = ['file_idX0', 'file_idX4', 'file_idX5', 'file_idX6', 'file_idX7',
                        'file_idX8', 'file_idX9', 'file_idX1', 'file_idX2', 'file_idX3']
            
            # order is important in which playqueue is arranged but not in Db            
            with (self.subTest("test Queuing 6 Items to an queue in DB")):
                Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id"))
                [self.assertIn(val, Expected) for val in Result]
                
            with (self.subTest("test Queuing 6 Items to an queue in PlayQueue")):
                Result = self.TabInstance.PlayQueue.GetQueue()
                self.assertEqual(Expected, Result)   
    
    def test_QueueLast(self):
        """
        Test adding new items at the end of the queue
        
        Expected Behaviour:
            Adds Data at the end in the Queue whenever new data is ready and is indexed Using File_id
        """
        
        with (self.subTest("test adding 4 Items to an empty queue")):
            [self.View.selectRow(R) for R in range(4)]
            # Adds items to an empty queue
            self.TabInstance.QueueLast(self.View)            
            self.View.clearSelection()
            Expected = self.DataTable["file_id"][:4]
            
            with (self.subTest("test Queuing 4 Items to an queue in DB")):
                Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id"))
                self.assertEqual(Expected, Result)
            
            with (self.subTest("test Queuing 4 Items to an queue in PlayQueue")):
                Result = self.TabInstance.PlayQueue.GetQueue()
                self.assertEqual(Expected, Result)            

        with (self.subTest("test readding last 4 Items to the end of the queue")):
            [self.View.selectRow(R) for R in [6, 7, 8, 9]]
            # Adds items To the end of the queue
            self.TabInstance.QueueLast(self.View)            
            self.View.clearSelection()
            Expected = [v for i, v in enumerate(self.DataTable["file_id"]) if i not in [4, 5]]
            
            with (self.subTest("test Queuing 6 Items to an queue in DB")):
                Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id"))
                self.assertEqual(Expected, Result)
            
            with (self.subTest("test Queuing 6 Items to an queue in PlayQueue")):
                Result = self.TabInstance.PlayQueue.GetQueue()
                self.assertEqual(Expected, Result) 
            
            
    def test_PlayAllShuffled(self):
        """
        Test adding Shuffled items in the queue and clearing the queue
        
        Expected Behaviour:
            Adds Shuffled Data in the Queue whenever new data is ready and is indexed Using File_id
            
        #Issue: Fails sometime due to randomness generating smae pattern
        """        
        
        with (self.subTest("test Shuffle adding 4 Items to an empty queue")):
            [self.View.selectRow(R) for R in range(4)]
            
            # Adds items to an empty queue
            self.TabInstance.PlayAllShuffled(self.View)            
            self.View.clearSelection()
            
            # gets result from DB as items dont need order
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id"))
            Expected = self.DataTable["file_id"][:4] # checks with expected value
            [self.assertIn(val, Expected) for val in Result]
            self.assertNotEqual(Expected, Result)
            
        with (self.subTest("test shuffle readding last 4 Items to an filled queue")):
            [self.View.selectRow(R) for R in [6, 7, 8, 9]]
            
            # Adds new items to an filled queue
            self.TabInstance.PlayAllShuffled(self.View)            
            self.View.clearSelection()
            
            # gets result from DB as items dont need order 
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","file_id"))    
            Expected = self.DataTable["file_id"][6:]
            [self.assertIn(val, Expected) for val in Result]
            self.assertNotEqual(Expected, Result)
            
    
    def test_PlayArtist(self):
        """
        Test adding Similar Artist items in the queue and clearing the queue
        
        Expected Behaviour:
            Adds Data in the Queue whenever new data is ready and is indexed Using artist
        """         
        
        with (self.subTest("test Shuffle adding 4 Items to an empty queue")):
            [self.View.selectRow(R) for R in range(4)]
            # Adds items to an empty queue
            self.TabInstance.PlayArtist(self.View)            
            self.View.clearSelection()
            # gets result from DB as items dont need order
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","artist"))
            Expected = self.DataTable["artist"][:4] # checks with expected value
            self.assertEqual(Expected, Result)

            
        with (self.subTest("test shuffle readding last 4 Items to an filled queue")):
            [self.View.selectRow(R) for R in [6, 7, 8, 9]]
            # Adds new items to an filled queue
            self.TabInstance.PlayArtist(self.View)            
            self.View.clearSelection()
            # gets result from DB as items dont need order 
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","artist"))    
            Expected = self.DataTable["artist"][6:]
            self.assertEqual(Expected, Result)

    
    def test_PlayAlbumNow(self):
        """
        Test adding Similar Album items in the queue and clearing the queue
        
        Expected Behaviour:
            Adds Data in the Queue whenever new data is ready and is indexed Using album
        """ 
        
        with (self.subTest("test Shuffle adding 4 Items to an empty queue")):
            [self.View.selectRow(R) for R in range(4)]
            # Adds items to an empty queue
            self.TabInstance.PlayAlbumNow(self.View)            
            self.View.clearSelection()
            # gets result from DB as items dont need order
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","album"))
            Expected = self.DataTable["album"][:4] # checks with expected value
            self.assertEqual(Expected, Result)
            
        with (self.subTest("test shuffle readding last 4 Items to an filled queue")):
            [self.View.selectRow(R) for R in [6, 7, 8, 9]]
            # Adds new items to an filled queue
            self.TabInstance.PlayAlbumNow(self.View)            
            self.View.clearSelection()
            # gets result from DB as items dont need order 
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","album"))    
            Expected = self.DataTable["album"][6:]
            self.assertEqual(Expected, Result)
    
    def test_QueueAlbumNext(self):
        """
        Test adding Similar Album items in the queue
        
        Expected Behaviour:
            Adds Data After the Pointer in the Queue whenever new data is ready and is indexed Using album
        """
        
        # test Stetup that creates a view with selected rows 
        [self.View.selectRow(R) for R in range(4)]
        self.TabInstance.PlayAlbumNow(self.View)
        self.View.clearSelection()       
            
        with (self.subTest("test Queuing last 6 Items to an filled queue")):
            [self.View.selectRow(R) for R in [4, 5, 6, 7, 8, 9]]
            # Adds items after pointer to queue
            self.TabInstance.QueueAlbumNext(self.View)            
            self.View.clearSelection()            

            # order is important in which playqueue is arranged but not in Db            
            with (self.subTest("test Queuing 6 Items to an queue in DB")):
                # gets data from DataTable to check for data simmilarity
                Expected = ['albumX0', 'albumX4', 'albumX5', 'albumX6', 'albumX7',
                            'albumX8', 'albumX9', 'albumX1', 'albumX2', 'albumX3']                
                Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","album"))
                [self.assertIn(val, Expected) for val in Result]
                
            with (self.subTest("test Queuing 6 Items to an queue in PlayQueue")):
                # gets data from DataTable to check for data simmilarity
                Expected = ['file_idX0', 'file_idX4', 'file_idX5', 'file_idX6', 'file_idX7',
                            'file_idX8', 'file_idX9', 'file_idX1', 'file_idX2', 'file_idX3']                
                Result = self.TabInstance.PlayQueue.GetQueue()
                self.assertEqual(Expected, Result)          
        
    
    def test_QueueAlbumLast(self):
        """
        Test adding Similar Album items in the queue
        
        Expected Behaviour:
            Adds Data in the end of the Queue whenever new data is ready and is indexed Using album
        """         
        # test Stetup that creates a view with selected rows 
        [self.View.selectRow(R) for R in range(4)]
        self.TabInstance.PlayAlbumNow(self.View)
        self.View.clearSelection()       
            
        with (self.subTest("test Queuing last 6 Items to an filled queue")):
            [self.View.selectRow(R) for R in [4, 5, 6, 7, 8, 9]]
            # Adds items after pointer to queue
            self.TabInstance.QueueAlbumLast(self.View)            
            self.View.clearSelection()            

            # order is important in which playqueue is arranged but not in Db            
            with (self.subTest("test Queuing 6 Items to an queue in DB")):
                # gets data from DataTable to check for data simmilarity
                Expected = ['albumX0', 'albumX4', 'albumX5', 'albumX6', 'albumX7',
                            'albumX8', 'albumX9', 'albumX1', 'albumX2', 'albumX3']                
                Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","album"))
                [self.assertIn(val, Expected) for val in Result]
                
            with (self.subTest("test Queuing 6 Items to an queue in PlayQueue")):
                # gets data from DataTable to check for data simmilarity
                Expected = ['file_idX0', 'file_idX1', 'file_idX2', 'file_idX3', 'file_idX4',
                            'file_idX5', 'file_idX6', 'file_idX7','file_idX8', 'file_idX9', ]                
                Result = self.TabInstance.PlayQueue.GetQueue()
                self.assertEqual(Expected, Result)       
       
    def test_PlayGenre(self):
        """
        Test adding Similar genre items in the queue
        
        Expected Behaviour:
            Adds Data in the Queue whenever new data is ready and is indexed Using genre
        """        
        
        with (self.subTest("test Shuffle adding 4 Items to an empty queue")):
            [self.View.selectRow(R) for R in range(4)]
            # Adds items to an empty queue
            self.TabInstance.PlayGenre(self.View)            
            self.View.clearSelection()
            # gets result from DB as items dont need orde
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","genre"))
            Expected = self.DataTable["genre"][:4] # checks with expected value
            self.assertEqual(Expected, Result)
            
        with (self.subTest("test shuffle readding last 4 Items to an filled queue")):
            [self.View.selectRow(R) for R in [6, 7, 8, 9]]
            # Adds new items to an filled queue
            self.TabInstance.PlayGenre(self.View)            
            self.View.clearSelection()
            # gets result from DB as items dont need order 
            Result = (self.TabInstance.LibraryManager.IndexSelector("nowplaying","genre"))    
            Expected = self.DataTable["genre"][6:]
            self.assertEqual(Expected, Result)     
                 
                 
class Test_ApolloTabFunctions_menubar(TestCase):
    """
    Tests all the functions inside menubar of the application
    """
    
class Test_ApolloTabFunctions_MISC(TestCase):

    def setUp(self):
        self.TabInstance = ApolloTabFunctions()
        self.TabInstance.LoadDB(":memory:")
        self.DataTable = TesterObjects.Gen_DbTable_Data(10)
        self.TabInstance.LibraryManager.BatchInsert_Metadata(self.DataTable)
        self.View = TesterObjects.Gen_TableView_fromData(self.DataTable)
        self.View.setProperty("DB_Table", "library")
        self.View.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

    def test_DeleteItem(self):
        TableModel = self.View.model()
        
        self.View.selectRow(3)
        with (self.subTest("Delete files from the DB and FileSystem")):
            self.TabInstance.DeleteItem("Delete", self.View)
            Result = (TableModel.index(3, 0).data())
            Query = self.TabInstance.LibraryManager.ExeQuery("""
            SELECT file_id
            FROM library
            WHERE file_id
            LIKE '%file_idX3%'""")
            
            with (self.subTest("Delete files from the table")):
                self.assertNotEqual("file_idX3", Result)
            
            with (self.subTest("Delete files from the DB")):            
                self.assertFalse(Query.next())
            self.View.clearSelection()
                
        self.View.selectRow(4)            
        with (self.subTest("Remove files from the DB")):
            self.TabInstance.DeleteItem("Remove", self.View)                          
            Result = (TableModel.index(4, 0).data())
            Query = self.TabInstance.LibraryManager.ExeQuery("""
            SELECT file_id
            FROM library
            WHERE file_id
            LIKE '%file_idX5%'""")
            
            with (self.subTest("Remove files from the table")):
                self.assertNotEqual("file_idX5", Result)
            
            with (self.subTest("Remove files from the DB")):            
                self.assertFalse(Query.next())                 
               

if __name__ == "__main__":
    App = QtWidgets.QApplication([])
    Suite = TestSuit_main()
    Suite.AddTest(Test_ApolloTabFunctions_selection)
    Suite.AddTest(Test_ApolloTabFunctions_Queueing)
    Suite.AddTest(Test_ApolloTabFunctions_menubar)
    Suite.AddTest(Test_ApolloTabFunctions_MISC)    
    Suite.Run(True)
