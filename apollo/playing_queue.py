from itertools import cycle

class PlayingQueue:
    """
    PlayingQueue is used as a track queue to manage track Playback.
    Base datatype used as the queue is an List and related operations of lists.
    """
    
    def __init__(self):
        self.PlayingQueue = []
        self.CurrentIndex = None
    
    def AddElements(self, element: list, Index = None):
        """
        Adds Elements to the playing Queue according to the index
        
        :Args:
            element: List
                A list of a single or multiple elements to add
            Index: Int
                Index to add elements to
        """
        #element insertion to an empty queue
        if Index == None:
            self.PlayingQueue.extend(element)
        
        # element insertion at an index
        else:
            if Index > len(self.PlayingQueue):
                self.PlayingQueue.extend(element)
            else:
                for offset, item in enumerate(element):
                    self.PlayingQueue.insert((Index + offset), item)
        return True
         
    def RemoveElements(self, Index = None, Start = None, End = None):
        """
        Removes a single element Or Elements between an Range Of indexs
        
        :Args:
            Index: Int
                index of the element to pop
            Start: Int
                Start position of the slice
            End: Int
                End Position of the slice
        """
        # removing single element from an index
        if Index != None and (Start == None or End == None):
            self.PlayingQueue.pop(Index)
            
        # slice removal
        if Start != None and End != None:
            if End >= len(self.PlayingQueue):
                del self.PlayingQueue[Start:]
            else:
                del self.PlayingQueue[Start: End]
        
        # Only start Args given
        if Start != None and End == None:
            del self.PlayingQueue[Start:]
            
        return True

    def IncrementPointer(self, by = 1): ...
    def DecrementPointer(self, by = 1): ...
    def GetQueue(self):
        return self.PlayingQueue
