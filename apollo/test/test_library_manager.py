import unittest
import unittest.mock as mock
import datetime

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QTableView, QApplication

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
    
class TestQT_LibraryManager(unittest.TestCase):
        
    QAPP_INSTANCE = None
    
    def setUp(self):
        if self.QAPP_INSTANCE == None:
            self.QAPP_INSTANCE = QApplication([])
        
        self.Librarymanager = LibraryManager(":memory:")
        self.app = self.QAPP_INSTANCE
            
    def tearDown(self):
        del self.app
            
    def test_SetTable_horizontalHeader(self):
        View = QTableView()
        View.setModel(QStandardItemModel())
        Labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        View = self.Librarymanager.SetTable_horizontalHeader(View = View, Labels = Labels)
        print(self.Librarymanager.GetTable_horizontalHeader(View))
        
        
if __name__ == '__main__':
    unittest.main()
