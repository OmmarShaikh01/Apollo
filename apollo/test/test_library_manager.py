import unittest
import unittest.mock as mock
import datetime
import copy

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTableView, QApplication, QLineEdit 

from apollo.db.library_manager import LibraryManager


class Test_LibraryManager(unittest.TestCase):

    def setUp(self):
        """
        Connects to an In-Memory Database For testing
        """
        self.Librarymanager = LibraryManager(':memory:')
        if self._testMethodName in ["test_TableSize", "test_TablePlaytime", "test_TableAlbumcount",
                                    "test_TableArtistcount", "test_Tabletrackcount"]:
            self.TableSetup()

    def TableSetup(self): 
        # data insertion into library table
        DataTable = {}
        for fields in self.Librarymanager.db_fields:
            if fields in ["discnumber", "channels"]:
                data = [Row for Row in range(10)]
            else:
                if self._testMethodName == "test_TableSize" and fields == "filesize":
                    data = [f"1024" for Row in range(10)]
                elif self._testMethodName == "test_TablePlaytime" and fields == "length":
                    data = datetime.timedelta(seconds = 60)
                    data = [f"{data}" for Row in range(10)]
                else:
                    data = [f"{fields}X{Row}" for Row in range(10)]
            DataTable[fields] = data
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)
        if not Query.execBatch():
            raise Exception(Query.lastError().text())            
            

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
        # connects to a db 
        Library_Inst = LibraryManager(":memory:")
        self.assertTrue(Library_Inst.IsConneted(), msg = "DB open failed")
        
        # Checks for a proper Stratup and Structure
        ## checks if library table is set up correctly
        Query = Library_Inst.ExeQuery(QSqlQuery("SELECT cid, name FROM pragma_table_info('library')")) 
        structTable = []
        while Query.next():
            structTable.append([Query.value(0), Query.value(1)])        
        self.assertEqual(len(Library_Inst.db_fields), len(structTable), msg = "<library> table structure not valid")
        
        ## checks if nowplaying table is set up correctly
        Query = Library_Inst.ExeQuery(QSqlQuery("SELECT cid, name FROM pragma_table_info('nowplaying')")) 
        structTable = []
        while Query.next():
            structTable.append([Query.value(0), Query.value(1)])        
        self.assertEqual(len(Library_Inst.db_fields), len(structTable), msg = "<nowplaying> table structure not valid")
        
        # tests the closing of the DB
        self.assertTrue(Library_Inst.close_connection(), msg = "DB close failed")
     
     
    def test_BatchInsert_Metadata(self):
        # data insertion into library table
        DataTable = {}
        for fields in self.Librarymanager.db_fields:
            if fields in ["discnumber", "channels"]:
                data = [Row for Row in range(10)]
            else:
                data = [f"{fields}X{Row}" for Row in range(10)]
            DataTable[fields] = data
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)
        if not Query.execBatch():
            raise Exception(Query.lastError().text())              
        
        ## checks if library data is set up correctly
        Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT * FROM library")) 
        structData = {}
        while Query.next():
            for col, fields in enumerate(self.Librarymanager.db_fields):
                val = Query.value(col)
                try:
                    structData[fields].append(val)
                except KeyError:
                    structData[fields] = [val]
        self.assertDictEqual(DataTable,structData, msg = "<library> table data not valid")        
        
        
    def test_Create_LibraryTable(self):
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
        self.Librarymanager.Create_EmptyView("testview")

        ## checks if testview table is set up correctly
        Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT cid, name FROM pragma_table_info('testview')")) 
        structTable = []
        while Query.next():
            structTable.append([Query.value(0), Query.value(1)])
        
        expression = len(self.Librarymanager.db_fields) == len(structTable)
        self.assertTrue(expression, msg = "<testview> table structure not valid")
        
        
    def test_CreateView(self):
        # data insertion into library table
        DataTable = {}
        for fields in self.Librarymanager.db_fields:
            if fields in ["discnumber", "channels"]:
                data = [Row for Row in range(10)]
            else:
                data = [f"{fields}X{Row}" for Row in range(10)]
            DataTable[fields] = data
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)
            
        if not Query.execBatch():
            raise Exception(Query.lastError().text())        
          
        self.Librarymanager.CreateView("testview", "file_id", DataTable["file_id"])
        
        ## checks if testview table is set up correctly
        Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT cid, name FROM pragma_table_info('testview')")) 
        structTable = []
        while Query.next():
            structTable.append([Query.value(0), Query.value(1)])
        
        expression = len(self.Librarymanager.db_fields) == len(structTable)
        self.assertTrue(expression, msg = "<testview> table structure not valid")        
        
        ## checks if testview data is set up correctly
        Query = self.Librarymanager.ExeQuery(QSqlQuery("SELECT * FROM testview")) 
        structData = {}
        while Query.next():
            for col, fields in enumerate(self.Librarymanager.db_fields):
                val = Query.value(col)
                try:
                    structData[fields].append(val)
                except KeyError:
                    structData[fields] = [val]

        self.assertDictEqual(DataTable,structData, msg = "<testview> table data not valid")
        
    def test_TableSize(self):         
        # tests the tablesize in GB
        self.assertEqual(10, self.Librarymanager.TableSize("library"))
        
        
    def test_TablePlaytime(self): 
        # tests the tableplaytime
        tabletime = str(self.Librarymanager.TablePlaytime("library"))
        expectedtime = datetime.time(minute = 10).isoformat()
        
        tabletime = datetime.datetime.strptime(tabletime, '%H:%M:%S')
        expectedtime = datetime.datetime.strptime(expectedtime, '%H:%M:%S')

        self.assertEqual(expectedtime, tabletime)
        
    def test_TableAlbumcount(self):         
        # tests the Albumcount
        self.assertEqual(10, self.Librarymanager.TableAlbumcount("library"))
        
    def test_TableArtistcount(self):        
        # tests the Artistcount
        self.assertEqual(10, self.Librarymanager.TableArtistcount("library"))
        
    def test_Tabletrackcount(self):
        # tests the TrackCount
        self.assertEqual(10, self.Librarymanager.TableArtistcount("library"))
    
    def test_horizontalHeader_functions(self):
        _ = QApplication([])
        
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
        
    def test_TableModel_functions(self):
        _ = QApplication([])
        
        # data insertion into library table
        DataTable = {}
        for fields in self.Librarymanager.db_fields:
            if fields in ["discnumber", "channels"]:
                data = [Row for Row in range(10)]
            else:
                data = [f"{fields}X{Row}" for Row in range(10)]
            DataTable[fields] = data
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)
        if not Query.execBatch():
            raise Exception(Query.lastError().text())         

        # creates an empty view and gets the table library from db
        View = QTableView()
        Table = self.Librarymanager.GetTableModle("library")
        
        # sets the tablemodel aqquired from Db 
        self.Librarymanager.SetTableModle(View = View, Table = Table)
        
        # Tests fo data getter and setter for te Db an d View bindding
        for index, column in enumerate(self.Librarymanager.db_fields):
            data = [Table.index(rows, index).data() for rows in range(Table.rowCount())]
            original = [str(i) for i in DataTable[column]]
            self.assertEqual(original, data)
        
    def Test_BasicTablesearch(self): 
        _ = QApplication([])
            
        # data insertion into library table
        DataTable = {}
        for fields in self.Librarymanager.db_fields:
            if fields in ["discnumber", "channels"]:
                data = [Row for Row in range(10)]
            else:
                data = [f"{fields}X{Row}" for Row in range(10)]
            DataTable[fields] = data
        Query = self.Librarymanager.BatchInsert_Metadata(DataTable)
        if not Query.execBatch():
            raise Exception(Query.lastError().text())         
         
        #get and sets data from the DB as a TableModel    
        View = QTableView()
        Table = self.Librarymanager.GetTableModle("library")
        self.Librarymanager.SetTableModle(View = View, Table = Table)
        
        # creats the LineEdit and sets the search term
        LEDT = QLineEdit()
        LEDT.setText("fieldX5")
        searchExpected = [values[5] for values in DataTable.values()]
        self.Librarymanager.TableSearch(LEDT, View)
        
        # test the search query execution and table Updation
        for rows in range(Table.rowCount()):
            data = [Table.index(rows, index).data() for rows in range(Table.columnCount())]
        self.assertEqual(searchExpected, data)
        
if __name__ == '__main__':    
    unittest.main()
