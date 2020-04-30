from PyQt5 import QtCore,QtWidgets,QtGui 
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler , FileSystemEventHandler
from anytree import Node, RenderTree, cachedsearch

from beets_tools_ui import Ui_MainWindow as _Beets
import subprocess as sp
import sys, time, os, re, logging, threading, json, anytree
  
    
class Beets_UI_wrapper(_Beets, QtWidgets.QMainWindow):
    """"""
    def __init__(self):
        """Constructor"""
        super(Beets_UI_wrapper, self).__init__()
        self.setupUi(self)        
        self.beets_path = 'E:\\python_virtual_env_for_Qt\\Scripts\\beet.exe'
        self.config_yaml = 'C:\\Users\\OMMAR\\Desktop\\Apollo\\beets\\config.yaml'
        self.sub_window_declaration()
        self.action_declaration()
        self.variable_declaration()
    
    def variable_declaration(self):
        self.dir_path_set = set([])
        self.path_depth = {}
        self.root_path = Node('Root')
    
    def action_declaration(self):
        self.add_toolb.pressed.connect(lambda: (self.file_broser_win.show()))
        self.remove_toolb.pressed.connect(lambda: (self.open_file('remove')))
        self.rescan_toolb.pressed.connect(lambda: ((threading.Thread(target = self.directory_scanner, args = ())).start()))
        self.list_files.pressed.connect(self.files_added_lister)
    
    def files_added_lister(self):
        self.status_log.clear()
        commands = [self.beets_path,'list']
        commands.extend(list(self.dir_path_set))
        with sp.Popen(commands, stdout = sp.PIPE, stderr = sp.PIPE, encoding = 'utf-8', universal_newlines = True) as proc:   
            out, err = proc.communicate()
            data = f"Output:{out}\nError:{err}"
            self.status_log.append(data)         
    
    
    def directory_scanner(self):
        self.status_log.append('Scanning Files')
        self.rescan_toolb.setEnabled(False)
        commands = [self.beets_path,'import', '-C', '-W', '-A']
        commands.extend(list(self.dir_path_set))
        with sp.Popen(commands, stdout = sp.PIPE, stderr = sp.PIPE, universal_newlines = True) as proc:   
            out, err = proc.communicate()
            data = f"Output:{out}\nError:{err}"
            self.status_log.append(data)         
        self.status_log.append('Scanning Files Completed')
        self.rescan_toolb.setEnabled(True)
    
    def path_tree(self, path, flag = False):
        root = self.root_path
        path = path.replace('/', '\\')
        for (direc, subdirec, _ ) in os.walk(path):
            item = direc.split('\\')
            par = root
            for i in item:
                if i not in [i.name for i in par.children]:
                    par = Node(i, par)
                if i in [i.name for i in par.children]:
                    try:
                        par = [j for j in par.children if i == j.name][0]
                    except:
                        pass

        if flag:
            for pre, fill, node in RenderTree(root):
                print("%s%s" % (pre, node.name))

    
    def sub_direc_rem(self, paths):
        aa = []
        paths = [(i.replace("/","\\")) for i in paths]
        for i in paths:
            for (direc, subdirec, _ ) in os.walk(i):
                direc = (direc.replace("/","\\"))
                for j in subdirec:
                    if (f'{direc}\\{j}') in paths:
                        aa.append((f'{direc}\\{j}'))
        return ((set(paths)).difference(set(aa)))    
    
    
    def open_file(self, flag):
        #try:
            
        model = QtGui.QStandardItemModel()
        if flag == 'add':
            index = self.file_broser_win.file_browser_tree.currentIndex()
            file_path = self.file_brow_model.filePath(index)
            self.dir_path_set.add(file_path)            
            self.path_tree(file_path)
            self.dir_path_set = (self.sub_direc_rem(self.dir_path_set))
        
        if flag == 'remove':
            index = (self.dir_paths_lis.currentIndex()).data()
            self.dir_path_set.remove(index)
            self.root_path = Node('Root')
            for i in self.dir_path_set:
                self.path_tree(i)
            
        [model.appendRow(QtGui.QStandardItem(str(i))) for i in self.dir_path_set]
        model.sort(0)
        self.dir_paths_lis.setModel(model)
    

################################################################################ 
################################################################################        
    
    
    def sub_window_declaration(self):
        self.file_broser_win = File_browser()
        self.sub_window_action_declaration()
   
    
    def sub_window_action_declaration(self):
        self.file_broser_win.file_browser_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.file_broser_win.file_browser_tree.customContextMenuRequested.connect(self.context_menu_dec)
        self.file_broser_win.buttonBox.accepted.connect(lambda: self.file_broser_win.close())
        self.file_broser_win.buttonBox.rejected.connect(lambda: self.file_broser_win.close())
        self.populate()
   
    def populate(self):
        path = r""
        self.file_brow_model = QtWidgets.QFileSystemModel()
        self.file_brow_model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDotAndDotDot)
        self.file_brow_model.setRootPath((QtCore.QDir.rootPath()))
        self.file_broser_win.file_browser_tree.setModel(self.file_brow_model)
        self.file_broser_win.file_browser_tree.setRootIndex(self.file_brow_model.index(path))
        self.file_broser_win.file_browser_tree.setSortingEnabled(True)


    def context_menu_dec(self):    
        self.contex_menu = QtWidgets.QMenu()
        (self.contex_menu.addAction("Add Folder to library")).triggered.connect(lambda: (self.open_file('add')))
        cursor = QtGui.QCursor()
        self.contex_menu.exec_(cursor.pos())


################################################################################ 
################################################################################

class File_browser(QtWidgets.QMainWindow):
    """"""
    def __init__(self):
        """Constructor"""
        super(File_browser, self).__init__()
        self.setupUi(self)
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(640, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.file_browser_tree = QtWidgets.QTreeView(self.centralwidget)
        self.file_browser_tree.setFrameShape(QtWidgets.QFrame.Box)
        self.file_browser_tree.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.file_browser_tree.setUniformRowHeights(True)
        self.file_browser_tree.setWordWrap(True)
        self.file_browser_tree.setObjectName("file_browser_tree")
        self.file_browser_tree.header().setCascadingSectionResizes(True)
        self.file_browser_tree.header().setDefaultSectionSize(200)
        self.file_browser_tree.header().setMinimumSectionSize(50)
        self.gridLayout.addWidget(self.file_browser_tree, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
    
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))    


################################################################################ 
################################################################################

class LoggingEventHandler(FileSystemEventHandler):
    
    def on_moved(self, event):
        super(LoggingEventHandler, self).on_moved(event)
        what = 'directory' if event.is_directory else 'file'
        print(f"Moved {what}: from {event.src_path} to {event.src_path}")
        self.file_path, self.action = event.src_path, 'moved'
    
    def on_created(self, event):
        super(LoggingEventHandler, self).on_created(event)
        what = 'directory' if event.is_directory else 'file'
        print(f"Created {what}: {event.src_path}")
        self.file_path, self.action = event.src_path, 'created'
   
    def on_deleted(self, event):
        super(LoggingEventHandler, self).on_deleted(event)
        what = 'directory' if event.is_directory else 'file'
        print(f"Deleted {what}: {event.src_path}")
        self.file_path, self.action = event.src_path, 'deleted'
    
    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)
        what = 'directory' if event.is_directory else 'file'
        print(f"Modified {what}: {event.src_path}")
        self.file_path, self.action = event.src_path, 'modified'


################################################################################ 
################################################################################

class Beets_modle_wrapper():
    """"""

    def __init__(self, *args):
        """Constructor"""
        self.variable_declaration()
        self.library_man()
    
    def variable_declaration(self):
        self.beets_library_object = B_library
        self.beets_importer_object = B_importer
        self.beets_random_object = B_random
        self.beets_vfs_object = B_vfs
   
   
    def library_man(self):
        pass
   
################################################################################ 
################################################################################  
if __name__ == "__main__":
    obj = Beets_modle_wrapper()