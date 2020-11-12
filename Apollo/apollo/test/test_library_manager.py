import unittest
import unittest.mock as mock

from apollo.db.library_manager import LibraryManager

class Test_LibraryManager(unittest.TestCase):
    
    def setUp(self):
        self.library_man = LibraryManager()
    
    def test_1(self):
        # Evaluates the LibraryManager.scan_directory and generates valid data 
        # Query on all the files Parsed
        
        self.library_man.scan_directory("")
        

if __name__ == '__main__':
    unittest.main()
