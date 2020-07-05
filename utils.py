import sys, time, os, threading, re, json
import sqlite3 as sql

from PyQt5 import QtGui, QtSql, QtCore, QtWidgets

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r %2.3f s' % (method.__name__, (te - ts)))
        return result
    return timed

def threadit(method):
    def thread_call(*args, **kw):
        print(args, kw)
        thread = threading.Thread(target = method, args = args, kwargs = kw)
        thread.start()
    return thread_call
 
 
def lockthreadit(method):
    def thread_call(*args, **kw):
        lock = threading.Lock()
        with lock:
            thread = threading.Thread(target = method, args = args, kwargs = kw)
            thread.start()
        thread.join()
    return thread_call
    
def database_connector_wrap(funct):
    def database_connector_exec(*args, **kwargs):
        conn = sql.connect('library.db')
        out = funct(conn = conn, *args, **kwargs)
        conn.commit()
        conn.close()            
        return out
    return database_connector_exec

def database_connector_sql_exe(query):
    conn = sql.connect('library.db')
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    conn.close()            
    return data

def tryit(method):
    def try_ex(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            print(f"<{method.__name__}> {e}")        
    return try_ex


def logging_print(fun, e, slot = None, flag = "prnt"):
    # used to log events inside a function
    # fun = method
    # e = event
    # slot = internal function with event as the value
    
    value = (f"<Time: {time.ctime()}> <Name: {fun.__name__}>:<{e}>")
    if slot != None:
        slot(value)
    if flag != "prnt":
        return value
    else:
        print(value) 
  
def RateLimited(maxPerSecond, env = 1):
    minInterval = env / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.time() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.time()
            return ret
        return rateLimitedFunction
    return decorate


def allotter(items, theme_dict = None):
    if not isinstance(items, dict):
        items = {"_": items}

    for key, item in items.items():
        try:    
            item.setFrameShape(QtWidgets.QFrame.NoFrame)
        except:
            pass
        if isinstance(item, QtWidgets.QMenuBar):
            item.setStyleSheet(theme_dict["QMenuBar"])
                    
        elif isinstance(item, QtWidgets.QTabWidget):
            item.setStyleSheet(theme_dict["QTabWidget"])        
                  
        elif isinstance(item, QtWidgets.QScrollArea):
            item.setStyleSheet(theme_dict["QScrollArea"])          
                  
        elif isinstance(item, QtWidgets.QLabel):
            if QtCore.Qt.AlignmentFlag(item.alignment()) == 132:
                item.setStyleSheet(theme_dict["QLabel_Title"])
            else:
                item.setStyleSheet(theme_dict["QLabel"])
                item.setText("")
                
        elif isinstance(item, QtWidgets.QGraphicsView):
            item.setStyleSheet(theme_dict["QGraphicsView"])            
                     
        elif isinstance(item, QtWidgets.QTableView):
            item.setAlternatingRowColors(True)
            item.verticalHeader().setDefaultSectionSize(20)
            item.setFocusPolicy(QtCore.Qt.NoFocus)
            item.setStyleSheet(theme_dict["QTableView"])
               
        elif isinstance(item, QtWidgets.QTreeView):
            item.setStyleSheet(theme_dict["QTreeView"])
                      
        elif isinstance(item, QtWidgets.QDial):
            item.setStyleSheet(theme_dict["QDial"])
                      
        elif isinstance(item, QtWidgets.QScrollBar):
            item.setStyleSheet(theme_dict["QScrollBar"])
                      
        elif isinstance(item, QtWidgets.QSlider):
            item.setStyleSheet(theme_dict["QSlider"])
                      
        elif isinstance(item, QtWidgets.QLineEdit):
            item.setStyleSheet(theme_dict["QLineEdit"])
                      
        elif isinstance(item, QtWidgets.QPushButton):
            if re.search("_en$", str(key)):
                item.setStyleSheet(theme_dict["QPushButton_enable"])
            elif re.search("_dis$", str(key)):
                item.setStyleSheet(theme_dict["QPushButton_disable"])
            else:
                item.setStyleSheet(theme_dict["QPushButton"])
                
        elif isinstance(item, QtWidgets.QLCDNumber):
            item.setStyleSheet(theme_dict["QLCDNumber"])
                      
        elif isinstance(item, QtWidgets.QComboBox):
            item.setStyleSheet(theme_dict["QComboBox"])
                  
        elif isinstance(item, QtWidgets.QCheckBox):
            item.setStyleSheet(theme_dict["QCheckBox"])
                  
        elif isinstance(item, QtWidgets.QRadioButton):
            item.setStyleSheet(theme_dict["QRadioButton"])        
        
        elif isinstance(item, QtWidgets.QMenu):
            item.setStyleSheet(theme_dict["QContextMenu"])
                 
        else:
            try:
                item.setStyleSheet(theme_dict["QDefault"])
            except AttributeError:
                pass
            except Exception as e:
                logging_print(allotter, e)

class QueueIterator:
    def __init__(self, data):
        self.data = data
        self.size = len(data)
        self.index = 0
        
    def __next__(self):
        if (self.index < self.size):
            data = self.data[self.index]
            self.index += 1                
            return (self.index, data)
        else:
            raise StopIteration 
        
class Playback_queue():
    """"""

    def __init__(self, size, circ = False):
        self.playing_queue = {k:"" for k in range(size)}
        self.pointer_put = 0
        self.pointer_get = 0
        self.size = size
        self.circ = circ
        
    def __repr__(self):
        return json.dumps(self.playing_queue, indent = 2)
    
    def __str__(self):
        return json.dumps(self.playing_queue, indent = 2)    
    
    def __len__(self):
        return len(self.playing_queue)
    
    def __iter__(self):
        return QueueIterator(self)
    
    def __getitem__(self, index):
        return self.current()
       
    def put(self, data):
        self.playing_queue[self.pointer_put] = data
        self.pointer_put += 1
    
    def current(self):
        if self.pointer_get in range(len(self.playing_queue)):
            data = self.playing_queue[self.pointer_get]
            return (self.pointer_get, data)
        else:
            return (self.pointer_get,"EOF")
    
    def _next(self):
        try:
            if self.pointer_get in range(len(self.playing_queue) - 1):
                self.pointer_get += 1
                return self.current()
            elif self.circ:
                self.pointer_get = 0
                return self.current()
            else:
                return (self.pointer_get,"EOF")
        except KeyError:                 
            return (self.pointer_get,"EOF")    
        
    def prev(self):
        try:
            if self.pointer_get in range(1, len(self.playing_queue) + 1):
                self.pointer_get -= 1
                return self.current()
            elif self.circ:
                self.pointer_get = (len(self.playing_queue) - 1)
                return self.current()
            else:
                return (self.pointer_get,"EOF")
        except KeyError:                 
            return (self.pointer_get,"EOF")        
    
    def Setcircular(self, bl):
        self.circ = bl
    
    def empty(self):
        if (len(self.playing_queue) - self.pointer_get) == 1:
            return True
        else:
            return False



class Resource_Loader:
    
    def  __init__(self):
        self.resources_path = "resources"
        self.dict_gen()
        self.font_db = QtGui.QFontDatabase()   
        self.add_fonts(self.resource_dict)
        
        
    def add_fonts(self, items):
        for _, item in items.items():   
            if item in [".ttf"]:
                self.font_db.addApplicationFont(item)
                
        
    def dict_gen(self):
        self.resource_dict = {}
        count = 0
        for folder, sub, files in os.walk(self.resources_path):
            if files == []:
                continue
            else:
                for file in  files:
                    self.resource_dict[count] = (os.path.join(folder,file))
                    count += 1
        
class Theme_manup:
    
    def __init__(self, items):
        self.items = items
        self.allotter = allotter
        
    def setTheme(self, name = "default_theme"):
        self.name = name
        if self.name == "default_theme":
            self.default_theme()     
            self.allotter(self.items, self.theme_dict)
        elif name == None:
            self.no_theme()     
            self.allotter(self.items, self.theme_dict)
            
    def apply_theme(self, item):
        self.allotter(item, self.theme_dict)
    
    def replace_item(self, items): 
        self.items = items
       
    def no_theme(self):
        self.theme_dict = {"QMenuBar": "",
                           "QTabWidget": "",
                           "QScrollArea": "",
                           "QLabel": "",
                           "QLabel_Title": "",
                           "QGraphicsView": "",
                           "QTableView": "",
                           "QTreeView": "",
                           "QDial": "",
                           "QScrollBar": "",
                           "QSlider": "",
                           "QLineEdit": "",
                           "QPushButton": "",
                           "QPushButton_enable": "",
                           "QPushButton_disable": "",
                           "QLCDNumber": "",
                           "QComboBox": "",
                           "QCheckBox": "",
                           "QRadioButton": "",
                           "QContextMenu": "",
                           "QDefault": "",}        
          
    def default_theme(self):
        QMenuBar = ('QMenuBar {\n'
                       '    background-color: rgb(0, 0, 0);\n'
                       '    spacing: 3px;\n'
                       '\tcolor: rgb(255, 255, 255);\n'
                       '\tborder-color: 2px solid rgb(255, 255, 0);\n'
                       '}\n'
                       '\n'
                       'QMenuBar::item {\n'
                       '    padding: 1px 4px;\n'
                       '    background:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 '
                       'rgba(0, 137, 255, 255), stop:0.0909091 rgba(0, 0, 0, 255));\n'
                       '    border-radius: 4 px;\n'
                       '\tcolor: rgb(255, 255, 255);\n'
                       '}\n'
                       '\n'
                       'QMenuBar::item:selected { /* when selected using mouse or keyboard */\n'
                       '    background:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 '
                       'rgba(0, 137, 255, 255), stop:0.0909091 rgba(0, 0, 0, 255));\n'
                       '}\n'
                       '\n'
                       'QMenuBar::item:pressed {\n'
                       '    background:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 '
                       'rgba(0, 137, 255, 255), stop:0.0909091 rgba(0, 0, 0, 255));\n'
                       '}\n'
                       '\n'
                       'QMenu {\n'
                       '    background-color:rgb(25, 25, 25);\n'
                       '    border: 1px rgb(0, 170, 255);\n'
                       '\tcolor: rgb(255, 255, 255);\n'
                       '}\n'
                       '\n'
                       'QMenu::item {\n'
                       '    background-color: transparent;\n'
                       '\tcolor: rgb(255, 255, 255);\n'
                       '}\n'
                       '\n'
                       'QMenu::item:selected { /* when user selects item using mouse or keyboard */\n'
                       '    background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, '
                       'stop:0 rgba(0, 137, 255, 255), stop:0.0909091 rgba(25, 25, 25, 255))\n'
                       '}\n'
                       '\n'
                       '\n'
                       'QStatusBar {\n'
                       '    color: rgb(0, 0, 0);\n'
                       '    background: rgb(0, 0, 0);\n'
                       '}\n'
                       '\n'
                       'QStatusBar::item {\n'
                       '\tborder-right-color:2px rgb(0, 170, 255);\n'
                       '\tborder-left-color:2px rgb(0, 170, 255);\n'
                       '\tborder-bottom-color:2px rgb(0, 170, 255);\n'
                       '    border-radius: 3px;\n'
                       '}')
        
        QTabWidget = ('QTabWidget::pane {\n'
                      '    border: 0px solid #C2C7CB;\n'
                      '}\n'
                      '\n'
                      'QTabBar::tab {\n'
                      '    background: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, '
                      'stop:0.545455 rgba(0, 0, 0, 255), stop:0.823864 rgba(33, 33, 33, 255), '
                      'stop:1 rgba(67, 67, 67, 255));\n'
                      '\tcolor:#FFFFFF;\n'
                      '\tfont-size: 12px;\n'
                      '    border-bottom-color: #000000;\n'
                      '    border-top-left-radius: 6px;\n'
                      '\tborder-top-right-radius: 6px;\t\n'
                      '    min-width: 30ex;\n'
                      '    padding-left:5 px;\n'
                      '\tpadding-right: 5px;\n'
                      '\tpadding-bottom: 4px;\n'
                      '}\n'
                      '\n'
                      'QTabBar::tab:selected, QTabBar::tab:hover {\n'
                      '   background-color:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, '
                      'stop:0 rgba(0, 146, 255, 255), stop:0.102273 rgba(0, 0, 0, 255), '
                      'stop:0.522727 rgba(0, 0, 0, 255), stop:0.892045 rgba(0, 0, 0, 255), stop:1 '
                      'rgba(0, 149, 255, 255));\n'
                      '}\n'
                      '\n'
                      'QTabBar::tab:selected {\n'
                      '   background-color:qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, '
                      'stop:0 rgba(0, 146, 255, 255), stop:0.102273 rgba(0, 0, 0, 255), '
                      'stop:0.522727 rgba(0, 0, 0, 255), stop:0.892045 rgba(0, 0, 0, 255), stop:1 '
                      'rgba(0, 149, 255, 255));\n'
                      '}\n')
        
        QScrollArea = "background-color: rgb(0, 0, 0)"
        
        QLabel = ('background-color: rgb(0, 0, 0, );\n'
                  'color: rgb(255, 255, 255);')
        
        QGraphicsView = "background-color: rgb(0, 0, 0)"
                
        QTableView = ('QTableView {\n'
                    '\tbackground-color: rgb(0, 0, 0);\n'
                    '\talternate-background-color: rgb(50, 50, 50);\n'
                    '\tcolor: rgb(255, 255, 255);\t\t\t\n'
                    '\tbackground-attachment: scroll;\n'
                    '}\n'
                    '\n'
                    '\n'
                    'QTableCornerButton::section{\n'
                    'background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, stop:0 '
                    'rgba(0, 146, 255, 255), stop:0.0511364 rgba(0, 24, 43, 255), stop:0.522727 '
                    'rgba(0, 0, 0, 255), stop:0.948864 rgba(0, 30, 52, 255), stop:1 rgba(0, 149, '
                    '255, 255));\n'
                    '}\n'
                    '\n'
                    'QTableView::item:alternate {\n'
                    '    background: rgb(50, 50, 50);\n'
                    '}\n'
                    '\n'
                    'QTableView::item:selected {\n'
                    '\tbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, '
                    'stop:0.903409 rgba(0, 0, 0, 255), stop:1 rgba(0, 149, 255, 255))\n'
                    '}\n'
                    '\n'
                    'QTableView::item:selected:!active {\n'
                    '\tcolor: rgb(255, 255, 255);\n'
                    '\tbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, '
                    'stop:0.903409 rgba(0, 0, 0, 255), stop:1 rgba(0, 149, 255, 255));\n'
                    '}\n'
                    '\n'
                    'QTableView::item:selected:active {\n'
                    '\tcolor: rgb(255, 255, 255);\n'
                    '\tbackground-color:qlineargradient(spread:pad, x1:1, y1:0, x2:1, y2:1, '
                    'stop:0.903409 rgba(0, 0, 0, 255), stop:1 rgba(0, 149, 255, 255));\n'
                    '}\n'
                    '\n'
                    'QHeaderView::section {\n'
                    '    background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, '
                    'stop:0 rgba(0, 146, 255, 255), stop:0.0511364 rgba(0, 24, 43, 255), '
                    'stop:0.522727 rgba(0, 0, 0, 255), stop:0.948864 rgba(0, 30, 52, 255), stop:1 '
                    'rgba(0, 149, 255, 255));\n'
                    '    color: white;\n'
                    '    padding-left: 4px;\n'
                    '\tborder: 1px solid rgb(0, 0, 0)\n'
                    '}\n'
                    '\n'
                    '\n'
                    'QHeaderView::section:checked\n'
                    ' {\n'
                    '    background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:1, '
                    'stop:0 rgba(0, 146, 255, 255), stop:0.0511364 rgba(0, 24, 43, 255), '
                    'stop:0.522727 rgba(0, 0, 0, 255), stop:0.948864 rgba(0, 30, 52, 255), stop:1 '
                    'rgba(0, 149, 255, 255));\n'
                    '    color: white;\n'
                    '    padding-left: 4px;\n'
                    '\tborder: 1px solid rgb(0, 0, 0)\n'
                    '}\n')

        QTreeView = ""
        
        QDial = 'background-color: rgb(0, 170, 255)'
        
        QScrollBar = ""
        
        QSlider = ('QSlider{\n'
                   'background-color: rgb(0, 0, 0);\n'
                   'border: 2px solid rgb(113, 113, 113);\n'
                   'border-width: 2px;\n'
                   'border-radius: 12px;\n'
                   '}\n'
                   'QSlider::handle:vertical {\n'
                   '    background: rgb(0, 170, 255);\n'
                   '    border: 2px solid rgb(113, 113, 113);\n'
                   '        border-width: 1px;\n'
                   '        border-radius: 4px;\n'
                   '        margin: 0 -4px\n'
                   '}\n'
                   'QSlider::add-page:vertical {\n'
                   '    border-bottom: 2px solid rgb(113, 113, 113);\n'
                   '        background: rgb(0, 170, 255);\n'
                   '}\n'
                   '\n'
                   'QSlider::sub-page:vertical {\n'
                   '    border-top: 2px solid rgb(113, 113, 113);\n'
                   '        background:rgb(0, 0, 0);\n'
                   '}\n'
                   'QSlider::handle:horizontal {\n'
                   '    background: rgb(0, 170, 255);\n'
                   '    border: 2px solid rgb(113, 113, 113);\n'
                   '        border-width: 1px;\n'
                   '        border-radius: 4px;\n'
                   '        margin: 0 -4px\n'
                   '}\n'
                   'QSlider::add-page:horizontal {\n'
                   '    border-bottom: 2px solid rgb(113, 113, 113);\n'
                   '        background: rgb(0, 170, 255);\n'
                   '}\n'
                   '\n'
                   'QSlider::sub-page:horizontal {\n'
                   '    border-top: 2px solid rgb(113, 113, 113);\n'
                   '        background:rgb(0, 0, 0);\n'
                   '}\n')
                          
        QLineEdit = ('QLineEdit {\n'
                     '    border: 2px solid gray;\n'
                     '    border-radius: 10px;\n'
                     '    padding: 0 8px;\n'
                     '    background: rgb(0, 0, 0);\n'
                     '    selection-background-color: darkgray;\n'
                     '}')
        
        QPushButton = ('QPushButton {\n'
                       '    background-color: rgb(0, 0, 0);\n'
                       '    border-style: outset;\n'
                       '    border-width: 1px;\n'
                       '    border-radius: 10px;\n'
                       '    border-color: rgb(0, 0, 0);\n'
                       '    font: bold 10px;\n'
                       '}\n'
                       'QPushButton {\n'
                       '    border-style: solid;\n'
                       '\tborder-color: rgb(65, 65, 65);\n'
                       '\tcolor: rgb(255, 255, 255);\n'
                       '}\n'
                       '\n'
                       'QPushButton:pressed {\n'
                       '\tbackground-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                       'fx:0.5, fy:0.5, stop:0.948864 rgba(0, 0, 0, 255), stop:1 rgba(0, 149, 255, '
                       '255))\n'
                       '}')
                       
        QPushButton_enable = ('QPushButton {\n'
                              '\tbackground-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, '
                              'stop:0.306818 rgba(0, 25, 6, 255), stop:0.681818 rgba(0, 88, 21, 255), '
                              'stop:1 rgba(0, 196, 47, 255));\n'
                              '    border-style: outset;\n'
                              '    border-width: 1px;\n'
                              '    border-radius: 4px;\n'
                              '    border-color: rgb(0, 0, 0);\n'
                              '}\n'
                              'QPushButton::pressed {\n'
                              '\tbackground-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, '
                              'stop:1 rgba(0, 196, 47, 255));\n'
                              '    border-style: outset;\n'
                              '    border-width: 1px;\n'
                              '    border-radius: 4px;\n'
                              '    border-color: rgb(0, 0, 0);\n'
                              '}\n'
                              'QPushButton::checked {\n'
                              '\tbackground-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, '
                              'stop:1 rgba(0, 196, 47, 255));\n'
                              '    border-style: outset;\n'
                              '    border-width: 1px;\n'
                              '    border-radius: 4px;\n'
                              '    border-color: rgb(0, 0, 0);\n'
                              '}')

        QPushButton_disable = ('QPushButton {\n'
                               '\tbackground-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, '
                               'stop:0.306818 rgba(25, 0, 0, 255), stop:0.681818 rgba(88, 0, 0, 255), stop:1 '
                               'rgba(196, 0, 0, 255));\n'
                               '    border-style: outset;\n'
                               '    border-width: 1px;\n'
                               '    border-radius: 4px;\n'
                               '    border-color: rgb(0, 0, 0);\n'
                               '}\n'
                               'QPushButton::pressed {\n'
                               '\tbackground-color: rgb(202, 0, 0);\n'
                               '    border-style: outset;\n'
                               '    border-width: 1px;\n'
                               '    border-radius: 4px;\n'
                               '    border-color: rgb(0, 0, 0);\n'
                               '}\n'
                               'QPushButton::checked {\n'
                               '\tbackground-color: rgb(202, 0, 0);\n'
                               '    border-style: outset;\n'
                               '    border-width: 1px;\n'
                               '    border-radius: 4px;\n'
                               '    border-color: rgb(0, 0, 0);\n'
                               '}')
        
        QLCDNumber = ('QLCDNumber{\n'
                      'background-color: rgb(0, 0, 0);\n'
                      'border: 2px solid rgb(113, 113, 113);\n'
                      'border-width: 2px;\n'
                      'border-radius: 10px;\n'
                      'color: rgb(255, 255, 255);\n'
                      '}')
        
        QComboBox = ('color: rgb(255, 255, 255);\n'
                     'background-color: rgb(0, 0, 0);\n'
                     'border-color: 2px rgb(0, 0, 0);')
        
        QCheckBox = ('QCheckBox {\n'
                     '    spacing: 5px;\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator {\n'
                     '    width: 13px;\n'
                     '    height: 13px;\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:unchecked {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(255, 0, 0, 255), stop:0.869318 rgba(0, 0, '
                     '0, 0))\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:unchecked:hover {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(255, 0, 0, 255), stop:0.869318 rgba(0, 0, '
                     '0, 0))\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:unchecked:pressed {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(255, 0, 0, 255), stop:0.869318 rgba(0, 0, '
                     '0, 0))\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:checked {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 255, 7, 255), stop:0.869318 rgba(0, 0, '
                     '0, 0));\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:checked:hover {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 255, 7, 255), stop:0.869318 rgba(0, 0, '
                     '0, 0));\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:checked:pressed {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 255, 7, 255), stop:0.869318 rgba(0, 0, '
                     '0, 0));\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:indeterminate:hover {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 137, 255, 255), stop:0.869318 rgba(0, '
                     '0, 0, 0));\n'
                     '}\n'
                     '\n'
                     'QCheckBox::indicator:indeterminate:pressed {\n'
                     'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                     'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 137, 255, 255), stop:0.869318 rgba(0, '
                     '0, 0, 0));\n'
                     '}\n')
        
        QRadioButton = ('QRadioButton {\n'
                        '    spacing: 5px;\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator {\n'
                        '    width: 13px;\n'
                        '    height: 13px;\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:unchecked {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(255, 0, 0, 255), stop:0.869318 rgba(0, 0, '
                        '0, 0))\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:unchecked:hover {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(255, 0, 0, 255), stop:0.869318 rgba(0, 0, '
                        '0, 0))\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:unchecked:pressed {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(255, 0, 0, 255), stop:0.869318 rgba(0, 0, '
                        '0, 0))\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:checked {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 255, 7, 255), stop:0.869318 rgba(0, 0, '
                        '0, 0));\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:checked:hover {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 255, 7, 255), stop:0.869318 rgba(0, 0, '
                        '0, 0));\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:checked:pressed {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 255, 7, 255), stop:0.869318 rgba(0, 0, '
                        '0, 0));\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:indeterminate:hover {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 137, 255, 255), stop:0.869318 rgba(0, '
                        '0, 0, 0));\n'
                        '}\n'
                        '\n'
                        'QRadioButton::indicator:indeterminate:pressed {\n'
                        'background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, '
                        'fx:0.5, fy:0.5, stop:0.840909 rgba(0, 137, 255, 255), stop:0.869318 rgba(0, '
                        '0, 0, 0));\n'
                        '}\n')
        
        QDefault = ('background-color: rgb(0, 0, 0, );\n'
                    'color: rgb(255, 255, 255);')
        
        QContextMenu = ('\n'
                        '    QMenu {\n'
                        '        background-color:rgb(25, 25, 25);\n'
                        '        border: 1px rgb(0, 170, 255);\n'
                        '            color: rgb(255, 255, 255);\n'
                        '    }\n'
                        '    \n'
                        '    QMenu::item {\n'
                        '        background-color: transparent;\n'
                        '            color: rgb(255, 255, 255);\n'
                        '    }\n'
                        '    \n'
                        '    QMenu::item:selected { /* when user selects item using mouse or keyboard '
                        '*/\n'
                        '        background-color:qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, '
                        'stop:0 rgba(0, 137, 255, 255), stop:0.0909091 rgba(25, 25, 25, 255))\n'
                        '    }\n')
        
        QLabel_Title = ('color: rgb(255, 255, 255);\n'
                        'background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 '
                        'rgba(0, 0, 0, 255), stop:0.443182 rgba(33, 33, 33, 255), stop:1 rgba(67, 67, '
                        '67, 255));\n'
                        'border-radius: 6px;')
        
        self.theme_dict = {"QMenuBar": QMenuBar,
                           "QTabWidget": QTabWidget,
                           "QScrollArea": QScrollArea,
                           "QLabel": QLabel,
                           "QLabel_Title": QLabel_Title,
                           "QGraphicsView": QGraphicsView,
                           "QTableView": QTableView,
                           "QTreeView": QTreeView,
                           "QDial": QDial,
                           "QScrollBar": QScrollBar,
                           "QSlider": QSlider,
                           "QLineEdit": QLineEdit,
                           "QPushButton": QPushButton,
                           "QPushButton_enable": QPushButton_enable,
                           "QPushButton_disable": QPushButton_disable,
                           "QLCDNumber": QLCDNumber,
                           "QComboBox": QComboBox,
                           "QCheckBox": QCheckBox,
                           "QRadioButton": QRadioButton,
                           "QContextMenu": QContextMenu,
                           "QDefault": QDefault,}               
