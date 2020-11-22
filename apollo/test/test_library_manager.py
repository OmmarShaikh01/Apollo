import unittest
import unittest.mock as mock

from PyQt5.QtSql import QSqlQuery

from apollo.db.library_manager import LibraryManager


class Test_LibraryManager(unittest.TestCase):

    def setUp(self):
        """
        Connects to an In-Memory Database For testing
        """
        self.Librarymanager = LibraryManager(':memory:')

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
        
        
if __name__ == '__main__':
    unittest.main()
