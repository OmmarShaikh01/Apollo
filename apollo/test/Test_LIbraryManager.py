from unittest import TestCase
from unittest.mock import MagicMock, Mock
import datetime
import sys, os

from apollo.db.library_manager import LibraryManager
from apollo.test.testUtilities import TesterObjects

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTableView, QApplication, QLineEdit


class Test_LibraryManager(TestCase):
    # TODO
    # write Tests for advanced query search
    # write tests for file parsing and scanning
    
    def setUp(self):
        """
        Connects to an In memory DB using a DB driver
        """
        self.Librarymanager = LibraryManager(':memory:')
        self.maxDiff = None
        # Creates a temporary table tpo query data from
        if self._testMethodName in ["test_TableSize", "test_TablePlaytime", "test_TableAlbumcount",
                                    "test_TableArtistcount", "test_Tabletrackcount"]:
            self.Librarymanager.BatchInsert_Metadata(TesterObjects.Gen_DbTable_Data(10))
            
    def tearDown(self):
        if hasattr(self, "Librarymanager"):            
            self.Librarymanager.close_connection()

    def run(self, result=None):
        """
        reimplementation of run method to support skipping of the setup and teardown of tests
        """
        testskip = ['test_Connect']
        if self._testMethodName in testskip:
            # replaces the setUp with an empty function and stores the original inside OrignalsetUp
            (OrignalsetUp, self.setUp) = (self.setUp, lambda : None)
            try:
                # Executes the test
                super(Test_LibraryManager, self).run(result)
            finally:
                # replaces it to the original one
                self.setUp = OrignalsetUp
        else:
            # normal execution of the test
            super(Test_LibraryManager, self).run(result)
    
    def test_Connect(self):
        """
        Checks for:
        1. Connection to a database
        2. Checks if tables dont exists it creats valid structure
        3. Closes and commits changes
        """
        # connects to a db
        with (self.subTest(msg = "connects to a db")):        
            Library_Inst = LibraryManager(":memory:")
            self.assertTrue(Library_Inst.IsConneted(), msg = "DB open failed")
        
        # Checks for a proper Stratup and Structure
        ## checks if library table is set up correctly
        with (self.subTest(msg = "checks if library table is set up correctly")):        
            self.assertTrue(Library_Inst.StartUpChecks(), msg = "setup failed")
            
        # tests the closing of the DB
        with (self.subTest(msg = "tests the closing of the DB")):
            self.assertTrue(Library_Inst.close_connection(), msg = "DB close failed")
     
     
    def test_BatchInsert_Metadata(self):
        """
        Checks for batch insertion in the tables of the DB 
        """
        DataTable = TesterObjects.Gen_DbTable_Data(10)
        self.Librarymanager.BatchInsert_Metadata(DataTable)
        
        ## checks if library data is set up correctly
        Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT * FROM library")) 
        structData = {}
        while Query.next():
            for col, fields in enumerate(self.Librarymanager.db_fields):
                val = Query.value(col)
                if structData.get(fields):
                    structData[fields].append(val)
                else:
                    structData[fields] = [val]
        self.assertDictEqual(DataTable,structData, msg = "<library> table data not valid")        
        
    def test_Create_LibraryTable(self):
        """
        Checks for the Library Table structure Integrity
        """
        self.Librarymanager.DropTable("library")
        self.Librarymanager.Create_LibraryTable()

        ## checks if library table is set up correctly
        Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT cid, name FROM pragma_table_info('library')")) 
        structTable = []
        while Query.next():
            structTable.append([Query.value(0), Query.value(1)])
        
        expression = len(self.Librarymanager.db_fields) == len(structTable)
        self.assertTrue(expression, msg = "<library> table structure not valid")
        
        
    def test_Create_EmptyView(self):
        """
        Checks for creation of an empty view and its initilization
        """
        self.Librarymanager.Create_EmptyView("testview")

        ## checks if testview table is set up correctly
        Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT cid, name FROM pragma_table_info('testview')")) 
        structTable = []
        while Query.next():
            structTable.append([Query.value(0), Query.value(1)])
        
        expression = len(self.Librarymanager.db_fields) == len(structTable)
        self.assertTrue(expression, msg = "<testview> table structure not valid")
        
        
    def test_CreateView(self):
        """
        Checks for data filling into testview using data from library table
        """
        # data insertion into library table
        DataTable = TesterObjects.Gen_DbTable_Data()
        self.Librarymanager.BatchInsert_Metadata(DataTable)
        self.Librarymanager.CreateView("testview",Selector = DataTable["file_id"], Normal = True)
        
        ###### checks if testview table is set up correctly
        with (self.subTest(msg = "checks if testview table is set up correctly")):
            Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT cid, name FROM pragma_table_info('testview')")) 
            structTable = []
            while Query.next():
                structTable.append([Query.value(0), Query.value(1)])
            
            expression = len(self.Librarymanager.db_fields) == len(structTable)
            self.assertTrue(expression, msg = "<testview> table structure not valid")        
        
        ###### checks if testview data is set up correctly
        with (self.subTest(msg = "checks if testview data is set up correctly")):
            Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT * FROM testview")) 
            structData = {}
            while Query.next():
                for col, fields in enumerate(self.Librarymanager.db_fields):
                    val = Query.value(col)
                    self.assertIn(val, DataTable.get(fields), msg = "<testview> table data not valid")
            
        
    def test_TableSize(self):         
        """tests the tablesize in GB"""
        self.assertEqual(10, self.Librarymanager.TableSize("library"))
        
        
    def test_TablePlaytime(self): 
        """tests the tableplaytime"""
        tabletime = str(self.Librarymanager.TablePlaytime("library"))
        expectedtime = datetime.time(minute = 10).isoformat()
        
        tabletime = datetime.datetime.strptime(tabletime, '%H:%M:%S')
        expectedtime = datetime.datetime.strptime(expectedtime, '%H:%M:%S')

        self.assertEqual(expectedtime, tabletime)
        
    def test_TableAlbumcount(self):         
        """tests the Albumcount"""
        self.assertEqual(10, self.Librarymanager.TableAlbumcount("library"))
        
    def test_TableArtistcount(self):        
        """tests the Artistcount"""
        self.assertEqual(10, self.Librarymanager.TableArtistcount("library"))
        
    def test_Tabletrackcount(self):
        """tests the TrackCount"""
        self.assertEqual(10, self.Librarymanager.TableArtistcount("library"))
    
    def test_horizontalHeader_functions(self):
        """Test For Horizontal Header Initilization and assignment"""
        View = QTableView()
        Model = QStandardItemModel()
        for Rows in range(10):
            for index, Cols_field in enumerate(self.Librarymanager.db_fields):
                item = QStandardItem(f"{Cols_field}X{index}")
                Model.setItem(Rows, index, item)
        View.setModel(Model)
        Labels = self.Librarymanager.db_fields
        self.Librarymanager.SetTable_horizontalHeader(View = View, Labels = Labels)
        self.assertEqual(self.Librarymanager.db_fields, self.Librarymanager.GetTable_horizontalHeader(View))
        
    def test_TableModel_functions_unordered(self):
        """
        Tests for the data assignment From the DB to a TableView
        """
        # data insertion into library table
        DataTable = TesterObjects.Gen_DbTable_Data(10)
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)              

        # creates an empty QTableView and gets the table library from db
        View = QTableView()
        View.setProperty("DB_Table", "library")
        View.setProperty("DB_Columns", self.Librarymanager.db_fields)
        View.setProperty("Order", [])            
        
        # sets the tablemodel aqquired from Db 
        Table = self.Librarymanager.SetTableModle("library", View)
        with (self.subTest("Test For All attribute assignment")):            
            self.assertEqual("library", View.property("DB_Table"),
                             msg = "DB_Table Property Not assigned to View")
            
            self.assertEqual(self.Librarymanager.db_fields, View.property('DB_Columns'), 
                             msg = "DB_Columns Property Not assigned to View")
            
            self.assertEqual([], View.property("Order"), msg = "Order Property Not assigned to View")
        
        
        # Tests fo data getter and setter for te Db and View bindding
        with (self.subTest("Tests fo data getter and setter for te Db and View bindding")):                    
            for index, column in enumerate(self.Librarymanager.db_fields):
                data = [Table.index(rows, index).data() for rows in range(Table.rowCount())]
                original = [str(i) for i in DataTable[column]]
                self.assertEqual(original, data)
                
                
    def test_TableModel_functions_ordered(self):
        """
        Checks for ordered Filling of data in a tablemodel
        """
        # data insertion into library table
        DataTable = TesterObjects.Gen_DbTable_Data(10)
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)          
        
        # creates an empty QTableView and gets the table library from db
        View = QTableView()
        View.setProperty("DB_Table", "library")
        View.setProperty("DB_Columns", self.Librarymanager.db_fields)
        
        Expected = ['file_idX5', 'file_idX6', 'file_idX7', 'file_idX8', 'file_idX9',
                    'file_idX0', 'file_idX1', 'file_idX2', 'file_idX3', 'file_idX4',]
        View.setProperty("Order", list(map(str, Expected)))
                
        # Tests fo data getter and setter for te Db and View bindding
        with (self.subTest("Tests fo data getter and setter for te Db and View bindding")):
            Table = self.Librarymanager.SetTableModle("library", View)
            data = [Table.index(rows, 0).data() for rows in range(Table.rowCount())]
            original = [str(i) for i in DataTable["file_id"]]
            self.assertEqual(Expected, data)        
        
    def test_SearchSimilarField(self):
        """
        Checks for filtering of the TableView and refreshes it.
        Searches in [album, artist, genre] Fields
        """        
        # data insertion into library table
        DataTable = TesterObjects.Gen_DbTable_Data(10)
        self.Librarymanager.BatchInsert_Metadata(DataTable)
        View = QTableView()
        View.setProperty("DB_Table", "library")
        View.setProperty("DB_Columns", self.Librarymanager.db_fields)
        View.setProperty("Order", [])        
        self.Librarymanager.SetTableModle("library", View)
        
        self.Librarymanager.SearchSimilarField(View, "album", ["albumX8", "albumX1"])
        TableModel = View.model()
        Result = []
        for Row in range(TableModel.rowCount()):
            if not View.isRowHidden(Row):                
                Result.append(TableModel.index(Row, 0).data())
        self.assertEqual(Result, ['file_idX1', 'file_idX8'])
        
    def test_BasicTablesearch(self):
        """
        Applies a Search and filters out rows in the view with simmilar data
        """
        LEDT = QLineEdit()
        LEDT.setText("X5")
        
        # data insertion into library table
        DataTable = TesterObjects.Gen_DbTable_Data(10)
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)
        
        # creates an empty QTableView and gets the table library from db
        View = QTableView()
        View.setProperty("DB_Table", "library")
        View.setProperty("DB_Columns", self.Librarymanager.db_fields)
        View.setProperty("Order", [])
        
        Table = self.Librarymanager.SetTableModle("library", View)

        # Runs the searcg query
        self.Librarymanager.TableSearch(LEDT, View)
        
        Table = View.model()
        Result = []
        for Row in range(Table.rowCount()):
            if not View.isRowHidden(Row):                
                Result.append(Table.index(Row, 0).data())
       
        # Queries the DB and Generates the FileId used to show valid rows 
        self.assertEqual(['file_idX5'], Result)
        
    def test_ClearView_Masks(self):
        """
        Test the function that clears the filter masks that are applied on searches 
        """
        View = QTableView()
        TableModel = QStandardItemModel()
        [TableModel.appendRow(QStandardItem(Row)) for Row in range(20)]
        View.setModel(TableModel)
        View.hideRow(1)
        View.hideRow(3)        
        View.hideRow(5)
        self.Librarymanager.ClearView_Masks(View)        
        self.assertFalse(View.isRowHidden(1))
        self.assertFalse(View.isRowHidden(3))
        self.assertFalse(View.isRowHidden(5))

if __name__ == '__main__':
    from apollo.test.testUtilities import TestSuit_main
    App = QApplication([])
    Suite = TestSuit_main()
    Suite.AddTest(Test_LibraryManager)
    Suite.Run()
