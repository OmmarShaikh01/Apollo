import time, json, os, threading

import apollo

parent_dir = apollo.__path__[0]

def exe_time(method):
    def timed(*args, **kw):
        """
        Calculates the method execution time. exe_time is used as an Method
        decorator.
        """

        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r %2.4f s' % (method.__name__, (te - ts)))
        return result
    return timed

def ThreadIt(method):
    def Exe(*args, **kw):
        """
        Threads the function passed in as an argumnet
        """
        Thread = threading.Thread(target = method, args = args, kwargs = kw, name = method.__name__)
        Thread.start()
    return Exe

def dedenter(string = '', indent_size = 4):
    """
    Dedents the string according to the given indent

    :Args:
        string: String
            String dedent

        indent_size: Int
            indent size to reduce
    """
    string = string.expandtabs().splitlines()
    string = ("\n".join([line[(indent_size):] for line in string]))
    return (string.strip("\n"))

class ConfigManager:
    """
    Manages the Configuration Parameters of Apollo

    >>> inst = ConfigManager()
    >>> inst.Getvariable("ROOT/SUB/SUB1")
    >>> inst.Setvariable(["VALUE"], "ROOT/SUB/SUB1")
    """

    def __init__(self):
        self.file = os.path.join(parent_dir,"config.cfg")
        self.config_dict = self.openConfig(self.file)

    def deafult_settings(self):
        """
        Initilizes the default launch config
        """
        config = {
            "APPTHEMES": [],
            "LIBRARY_GROUPORDER": "file_path",
            "ACTIVETHEME": "",
            "CURRENT_DB": "Default",
            "MONITERED_DB": {
                "Default": {
                    "name": "Default",
                    "db_loc": os.path.join(parent_dir, 'db', 'default.db'),
                    "file_mon": [],
                    "filters": ""
                }
            }
        }
        return config

    def openConfig(self, file = None):
        """
        Opens the config file and loads the settings JSON

        :Args:
            file: String
                Config File path
        """
        if file == None:
            file = self.file

        self.config_dict = {}
        if not os.path.isfile(file):
            with open(file, "w") as FP:
                json.dump(self.deafult_settings(), FP, indent = 4)
                self.config_dict = self.deafult_settings()
        else:
            try:
                with open(file) as FP:
                    self.config_dict = json.load(FP)
            except json.JSONDecodeError as e:
                print(e)
                with open(file, "w") as FP:
                    json.dump({}, FP, indent = 4)
        return self.config_dict


    def writeConfig(self, file = None):
        """
        Writes Data to the Config File

        :Args:
            data: Dict
                Data Dict to Write

            file: String
                File Name To write Into
        """
        if file == None:
            file = self.file

        with open(file, "w") as FP:
            json.dump(self.config_dict, FP, indent = 4)


    def Getvalue(self, path = "", config = None):
        """
        Recursively Traverses the path and gets the value

        :Args:
            config: Dict
                dict to traverse

            path: String, List
                Path used to traverse the dict
        """
        if config == None:
            config = self.config_dict

        if isinstance(path, str):
            path = path.split("/")

        if len(path) >= 1 and not("" in path):
            index = path.pop(0)
            data = config.get(index)

            if isinstance(data, dict):
                return self.Getvalue(path, data)
            else:
                return data
        else:
            return config


    def Setvalue(self, value, path = '', config = None):
        """
        Recursively Traverses the path and Sets the value
        >>> self.Config_manager.Setvalue(["VALUE"], "ROOT/SUB/SUB1")
        :Args:
            value: Any
                Value to replace or set

            config: Dict
                dict to traverse

            path: String, List
                Path used to traverse the dict
        """
        if config == None:
            config = self.config_dict

        if isinstance(path, str):
            path = path.split("/")

        if len(path) >= 1 and not("" in path):
            index = path.pop(0)
            if not config.get(index):
                config[index] = value
                return None

            data = config.get(index)
            if isinstance(data, dict):
                return self.Setvalue(value, path, data)
            else:
                if isinstance(data, list):
                    config[index].append(value)
                else:
                    config[index] = [value]
        else:
            return None


class PlayingQueue:
    """
    PlayingQueue is used as a track queue to manage track Playback.
    Base datatype used as the queue is an List and related operations of lists.
    """

    # management of index scaling when indexes are modified
    def __init__(self, circ = False):
        self.PlayingQueue = []
        self.CurrentIndex = 0
        self.IsCircular = circ
        self.index_pos = []


    def __len__(self):
        return len(self.PlayingQueue)

    def __repr__(self):
        return str(self.PlayingQueue)

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
                # index scaling when elements are added
                if self.CurrentIndex >= Index:
                    self.CurrentIndex += len(element)

        return True


    def AddNext(self, element):
        """
        Adds Elements to the playing Queue after currest position
        :Args:
            element: List
                A list of a single or multiple elements to add
        """
        self.AddElements(element, Index = self.GetPointer() + 1)


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
            if  self.CurrentIndex > Index:
                self.CurrentIndex -= 1
            elif self.CurrentIndex == Index:
                self.JumpPos(0)
            else:
                pass

        # slice removal
        if Start != None and End != None:
            if End >= len(self.PlayingQueue):
                del self.PlayingQueue[Start:]
                if Start <= self.CurrentIndex:
                    self.JumpPos(0)
            else:
                del self.PlayingQueue[Start: End]
                if Start == self.CurrentIndex or self.CurrentIndex == End:
                    self.JumpPos(0)
                elif Start < self.CurrentIndex < End:
                    self.JumpPos(0)
                elif End < self.CurrentIndex:
                    offset = (End - Start)
                    self.CurrentIndex -= offset

        # Only start Args given
        if Start != None and End == None:
            del self.PlayingQueue[Start:]
            if Start <= self.CurrentIndex:
                self.JumpPos(0)

        # Complete dump of queue
        if Index == None and Start == None and End == None:
            self.PlayingQueue = []
            self.CurrentIndex = 0

        # index scaling when elements are removed


        return True


    def IncrementPointer(self, by = 1):
        """
        Increments the index with an given offset

        :Args:
            by: Int
                offset to incerment index
        """

        if (self.CurrentIndex + by) < len(self.PlayingQueue):
            self.CurrentIndex += by
        else:
            # Circular Indexing of queue
            if self.IsCircular:
                self.CurrentIndex = 0
            # Normal Indexing of queue
            else:
                self.CurrentIndex = 0
                raise IndexError()
        return self.CurrentIndex



    def DecrementPointer(self, by = 1):
        """
        Decrements the index with an given offset

        :Args:
            by: Int
                offset to Decerment index
        """
        if (self.CurrentIndex - by) >= 0:
            self.CurrentIndex -= by
        else:
            # Circular Indexing of queue
            if self.IsCircular:
                self.CurrentIndex = len(self.PlayingQueue) - 1
            # Normal Indexing of queue
            else:
                self.CurrentIndex = 0
                raise IndexError()

        return self.CurrentIndex


    def JumpPos(self, Pos):
        """
        Random access of queue

        :Args:
            Pos: Int
                index to jump to
        """
        if Pos in range(len(self.PlayingQueue)):
            self.CurrentIndex = Pos


    def SetCircular(self, bool_):
        """
        Enables and disables endpoint Circling of a list

        :Args:
            bool_: Boolean
        """
        self.IsCircular = bool_


    def GetPointer(self):
        return self.CurrentIndex


    def GetCurrent(self):
        """
        Gets the current value at index
        """
        if self.CurrentIndex != None:
            return self.PlayingQueue[self.CurrentIndex]


    def GetNext(self):
        """
        gets the next value
        """
        self.IncrementPointer()
        return self.GetCurrent()


    def GetPrevious(self):
        """
        Gets the previous value
        """
        self.DecrementPointer()
        return self.GetCurrent()


    def GetQueue(self):
        """
        Returns the complete queue
        """
        return self.PlayingQueue


if __name__ == "__main__":
    inst = ConfigManager()
    inst.Getvalue("children/children")
