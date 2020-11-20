import unittest

from apollo.utils import ConfigManager, PlayingQueue

class Test_ConfigManager(unittest.TestCase):
    
    def setUp(self):
        self.config_manager = ConfigManager()
        self.jsondict = {
            "destination_addresses": [
              "Philadelphia, PA, USA"
            ],
            "origin_addresses": [
              "New York, NY, USA"
            ],
            
            "rows": {
              "elements": {
                "distance": {
                  "text": "94.6 mi",
                  "value": 152193
                },
                "duration": {
                  "text": "1 hour 44 mins",
                  "value": [6227, 1324]
                },
                "status": "OK"
              }
            },
            "status": "OK"
          }
               
                  
    def test_Getvalue(self):
        
        # tests the handling of an empty path argument
        self.assertEqual(self.jsondict, self.config_manager.Getvalue(self.jsondict, ""))
        
        # tests for existance of data value
        self.assertEqual("94.6 mi", self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text"))
        self.assertEqual([6227, 1324], self.config_manager.Getvalue(self.jsondict, "rows/elements/duration/value"))
        
        
        # tests for handling non existance keys indexing
        self.assertEqual(None, self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text_NONE"))
        
        
    def test_Setvalue(self):
        # tests the handling of an empty path argument
        self.assertEqual(None, self.config_manager.Setvalue("TEST", self.jsondict, ""))
        
        # tests for updation of data value
        self.config_manager.Setvalue("TEST", self.jsondict, "rows/elements/distance/text")
        self.assertEqual("TEST", self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text"))
        
        self.config_manager.Setvalue("TEST", self.jsondict, "rows/elements/duration/value")
        self.assertEqual([6227, 1324, "TEST"], self.config_manager.Getvalue(self.jsondict, "rows/elements/duration/value"))
        
        # tests for handling non existance keys indexing
        self.config_manager.Setvalue("TEST", self.jsondict, "rows/elements/distance/text_NONE")
        self.assertEqual("TEST", self.config_manager.Getvalue(self.jsondict, "rows/elements/distance/text_NONE"))
        

class Test_PlayingQueue(unittest.TestCase):
    
    def setUp(self):
        self.PlayingQueue = PlayingQueue()
    
    def test_AddElements(self):
        # Tests For Element Insertion To An Empty Queue
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4])
        self.assertEqual([0, 1, 2, 3, 4], self.PlayingQueue.GetQueue())
        
        # Tests For Element Insertion At An Index
        self.PlayingQueue.AddElements([11, 21, 31, 41], 3)
        self.assertEqual([0, 1, 2, 11, 21, 31, 41, 3, 4], self.PlayingQueue.GetQueue())
        
        # Tests For Element Insertion At The Last Index
        self.PlayingQueue.AddElements([12, 22, 32, 42])
        self.assertEqual([0, 1, 2, 11, 21, 31, 41, 3, 4, 12, 22, 32, 42], self.PlayingQueue.GetQueue())
        
        # Tests For Out Of Bounds
        self.PlayingQueue.AddElements([13, 23, 33, 43], 18)
        expectedlist = [0, 1, 2, 11, 21, 31, 41, 3, 4, 12, 22, 32, 42, 13, 23, 33, 43]
        self.assertEqual(expectedlist, self.PlayingQueue.GetQueue())
        
        # Tests elements after current index.
        self.PlayingQueue.JumpPos(3)
        self.PlayingQueue.AddNext([53, 53, 53, 53])
        expectedlist = [0, 1, 2, 11, 53, 53, 53, 53, 21, 31, 41, 3, 4, 12, 22, 32, 42, 13, 23, 33, 43]
        self.assertEqual(expectedlist, self.PlayingQueue.GetQueue())
        
        # tests for index scaling whene elements are added
        self.PlayingQueue.RemoveElements()
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.JumpPos(3)
        
        # adding at the index the pointer is at 
        self.PlayingQueue.AddElements([11, 12, 13, 14, 15], 3)
        self.assertAlmostEqual(8, self.PlayingQueue.GetPointer())
        self.assertEqual(3, self.PlayingQueue.GetCurrent())
   
        # adding before the index the pointer is at 
        self.PlayingQueue.AddElements([21, 22, 23, 24, 25], 3)
        self.assertEqual(13, self.PlayingQueue.GetPointer())
        self.assertEqual(3, self.PlayingQueue.GetCurrent())
        
   
    def test_RemoveElements(self):     
        # Test For Removing Single Element From An Index
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.RemoveElements(Index = 3)
        self.assertEqual([0, 1, 2, 4, 5, 6, 7, 8, 9], self.PlayingQueue.GetQueue())
        
        # Test For Slice Removal
        self.PlayingQueue.RemoveElements(Start = 1, End = 4)
        self.assertEqual([0, 5, 6, 7, 8, 9], self.PlayingQueue.GetQueue())        
        
        # Test For End Out Of Bounds Type Removal
        self.PlayingQueue.RemoveElements(Start = 0, End = 8)
        self.assertEqual([], self.PlayingQueue.GetQueue())
        
        # Test For Only Start Args Given
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.RemoveElements(Start = 3)
        self.assertEqual([0, 1, 2], self.PlayingQueue.GetQueue())        
        
        
        # tests for index scaling when elements are removed(Index Args tests)
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.JumpPos(5)
        
        # pointer is at element that will be removed(Index Args tests)
        self.PlayingQueue.RemoveElements(Index = 5)
        self.assertEqual(0, self.PlayingQueue.GetPointer())

        # pointer is after the element that will be removed(Index Args tests)
        self.PlayingQueue.JumpPos(3)        
        self.PlayingQueue.RemoveElements(Index = 2)
        self.assertEqual(2, self.PlayingQueue.GetPointer())
        
        self.PlayingQueue.RemoveElements()
        
        # tests for index scaling when elements are removed(Start, End Args tests)
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.JumpPos(5)
        
        # pointer in between slice
        self.PlayingQueue.RemoveElements(Start = 4, End = 7)
        self.assertEqual([0, 1, 2, 3, 7, 8, 9], self.PlayingQueue.GetQueue())
        self.assertEqual(0, self.PlayingQueue.GetPointer())
        
        # pointer after Start
        self.PlayingQueue.JumpPos(5)
        self.PlayingQueue.RemoveElements(Start = 4)
        self.assertEqual([0, 1, 2, 3], self.PlayingQueue.GetQueue())
        self.assertEqual(0, self.PlayingQueue.GetPointer())
        
        # pointer on endpoint
        self.PlayingQueue.RemoveElements(Start = 0)
        self.assertEqual([], self.PlayingQueue.GetQueue())
        self.assertEqual(0, self.PlayingQueue.GetPointer())
        
        # pointer after the slice
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.JumpPos(7)
        self.PlayingQueue.RemoveElements(Start = 0, End = 6)
        self.assertEqual([6, 7, 8, 9], self.PlayingQueue.GetQueue())
        self.assertEqual(1, self.PlayingQueue.GetPointer())
        
        
    def test_IncrementPointer(self):
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        # Test End Cases
        self.PlayingQueue.IncrementPointer(9)
        self.assertAlmostEqual(9, self.PlayingQueue.GetCurrent())
        
        # Checks Fo Random Access Of Queue
        self.PlayingQueue.JumpPos(0)
        self.assertAlmostEqual(0, self.PlayingQueue.GetCurrent())
        
        # Test Normal Indexing Of Queue
        self.PlayingQueue.IncrementPointer(3)
        self.assertAlmostEqual(3, self.PlayingQueue.GetCurrent())
        
        # Tests Single Increment Of Pointer
        self.assertAlmostEqual(4, self.PlayingQueue.GetNext())
        
        # Test Circular Indexing Of Queue
        self.PlayingQueue.SetCircular(True)
        self.PlayingQueue.IncrementPointer(6)
        self.assertEqual(0, self.PlayingQueue.GetCurrent())
        
        self.PlayingQueue.IncrementPointer(3)
        self.assertEqual(3, self.PlayingQueue.GetCurrent())
        self.PlayingQueue.SetCircular(False)
        
        # Test For Non Circular Out Of Bounds
        try:
            self.PlayingQueue.IncrementPointer(9)
        except IndexError:
            self.assertTrue(True)
        else:
            self.assertTrue(False, msg = "Out of Bound Index Test Failed")
            
    def test_DecrementPointer(self):
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

        # Test End Cases
        self.PlayingQueue.IncrementPointer(9)
        self.assertAlmostEqual(9, self.PlayingQueue.GetCurrent())
        
        self.PlayingQueue.DecrementPointer(9)
        self.assertAlmostEqual(0, self.PlayingQueue.GetCurrent())        
        
        self.PlayingQueue.IncrementPointer(9)

        # Test Normal Indexing Of Queue
        self.PlayingQueue.DecrementPointer(3)
        self.assertAlmostEqual(6, self.PlayingQueue.GetCurrent())
        
        # Tests Single Increment Of Pointer
        self.assertAlmostEqual(5, self.PlayingQueue.GetPrevious())
        
        # Test Circular Indexing Of Queue
        self.PlayingQueue.SetCircular(True)
        self.PlayingQueue.DecrementPointer(6)
        self.assertEqual(9, self.PlayingQueue.GetCurrent())
        
        self.PlayingQueue.DecrementPointer(3)
        self.assertEqual(6, self.PlayingQueue.GetCurrent())
        self.PlayingQueue.SetCircular(False)
        
        # Test For Non Circular Out Of Bounds
        try:
            self.PlayingQueue.IncrementPointer(9)
        except IndexError:
            self.assertTrue(True)
        else:
            self.assertTrue(False, msg = "Out of Bound Index Test Failed")        
        
      
if __name__ == '__main__':
    unittest.main()
