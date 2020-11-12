import time, json

def exe_time(method):
    def timed(*args, **kw):
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
    string = string.expandtabs().splitlines()
    string = ("\n".join([line[(indent_size):] for line in string]))
    return (string.strip("\n"))

class ConfigManager:
    """
    Manages the Configuration Parameters of Apollo
    
    >>> inst = ConfigManager()
    >>> config = {1:1, 1:2}
    >>> inst.Getvariable(config, [1, 4, 2])
    """
    def __init__(self):...
    def openConfig(self): ...
    
    def Getvariable(self, config: dict, location: list):
        if len(location) >= 1:
            value = config[location.pop(0)]
            if isinstance(value, dict) or isinstance(value, list):
                return self.Getvariable(value, location)
            else:
                return value
        else:
            return config
        
    def Setvariable(self, value, config: dict, location: list):
        if len(location) >= 1:
            index = location.pop(0)
            data = config[index]
            if isinstance(data, dict) or isinstance(data, list):
                return self.Setvariable(value, data, location)
            else:
                config[index] = value
                return True
        else:
            return False
        
if __name__ == "__main__":
    inst = ConfigManager()
    inst.Getvariable(a, [1, 4, 2])
