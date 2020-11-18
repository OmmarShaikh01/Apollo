import unittest
from apollo.playing_queue import PlayingQueue

class Test_PlayingQueue(unittest.TestCase):
    
    def setUp(self):
        self.PlayingQueue = PlayingQueue()
    
    def test_AddElements(self):
        # tests for element insertion to an empty queue
        self.PlayingQueue.AddElements(["Test", 1, 2, 3, 4])
        self.assertEqual(["Test", 1, 2, 3, 4], self.PlayingQueue.GetQueue())
        
        # tests for element insertion at an index
        self.PlayingQueue.AddElements(["Test1", 11, 21, 31, 41], 3)
        self.assertEqual(["Test", 1, 2, "Test1", 11, 21, 31, 41, 3, 4], self.PlayingQueue.GetQueue())
        
        # tests for element insertion at the last index
        self.PlayingQueue.AddElements(["Test2", 12, 22, 32, 42])
        self.assertEqual(['Test', 1, 2, 'Test1', 11, 21, 31, 41, 3, 4, 'Test2', 12, 22, 32, 42], self.PlayingQueue.GetQueue())
        
        # tests for out of bounds
        self.PlayingQueue.AddElements(["Test3", 13, 23, 33, 43], 18)
        expectedlist = ['Test', 1, 2, 'Test1', 11, 21, 31, 41, 3, 4, 'Test2', 12, 22, 32, 42, "Test3", 13, 23, 33, 43]
        self.assertEqual(expectedlist, self.PlayingQueue.GetQueue())
   
    def test_RemoveElements(self):     
        # test for removing single element from an index
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.RemoveElements(Index = 3)
        self.assertEqual([0, 1, 2, 4, 5, 6, 7, 8, 9], self.PlayingQueue.GetQueue())
        
        # Test for slice removal
        self.PlayingQueue.RemoveElements(Start = 1, End = 4)
        self.assertEqual([0, 5, 6, 7, 8, 9], self.PlayingQueue.GetQueue())        
        
        # Test for end out of bounds removal
        self.PlayingQueue.RemoveElements(Start = 1, End = 8)
        self.assertEqual([0], self.PlayingQueue.GetQueue())
        
        # Test for Only start Args given
        self.PlayingQueue.AddElements([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.PlayingQueue.RemoveElements(Start = 3)
        self.assertEqual([0, 0, 1], self.PlayingQueue.GetQueue())        
        
        
if  __name__ == "__main__":
    unittest.main()
    
