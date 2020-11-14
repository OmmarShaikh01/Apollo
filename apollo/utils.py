import time, json, os

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
    >>> inst.Getvariable(config, "ROOT/SUB/SUB1")
    >>> inst.Setvariable("VALUE", config, "ROOT/SUB/SUB1")
    """
    
    def __init__(self):...
    
    def openConfig(self, file):
        """
        Opens the config file and loads the ssettings JSON
        
        :Args:
            file: String
                Config File path 
        """
        self.config_dict = {}
        if not os.path.isfile(file):
            with open(file, "w") as FP:
                json.dump({}, FP, indent = 4)
        else:
            try:
                with open(file) as FP:
                    self.config_dict = json.load(FP)
            except json.JSONDecodeError:
                with open(file, "w") as FP:
                    json.dump({}, FP, indent = 4)                
                
        return self.config_dict
                
                
    def writeConfig(self, data, file):
        """
        Writes Data to the Config File
        
        :Args:
            data: Dict
                Data Dict to Write
                
            file: String
                File Name To write Into
        """
        with open(file, "w") as FP:
            json.dump(data, FP, indent = 4)
     

    def Getvalue(self, config, path):
        """
        Recursively Traverses the path and gets the value
        
        :Args:
            config: Dict
                dict to traverse
            
            path: String, List
                Path used to traverse the dict
        """
        if isinstance(path, str):
            path = path.split("/")
        if len(path) >= 1 and not("" in path):
            index = path.pop(0)
            data = config.get(index)
            if isinstance(data, dict):
                return self.Getvalue(data, path)
            else:
                return data
        else:
            return config

        
    def Setvalue(self, value, config, path):
        """
        Recursively Traverses the path and Sets the value
        
        :Args:
            value: Any
                Value to replace or set 
        
            config: Dict
                dict to traverse
            
            path: String, List
                Path used to traverse the dict
        """        
        if isinstance(path, str):
            path = path.split("/")
            
        if len(path) >= 1 and not("" in path):
            index = path.pop(0)
            if not config.get(index):
                config[index] = value
                return None
            
            data = config.get(index)
            if isinstance(data, dict):
                return self.Setvalue(value, data, path)
            else:
                if isinstance(data, list):
                    config[index].append(value)
                else:
                    config[index] = value
        else:
            return None

        
            
if __name__ == "__main__":
    inst = ConfigManager()
    config = inst.openConfig("config.cfg")
    inst.Getvalue(config, "children/children")
    print(json.dumps(config, indent = 4))
