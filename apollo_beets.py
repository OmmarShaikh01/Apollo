from utils import *
from lib_up import Library_database_mang, Column_lut
from add_new_play_DB_ui import Ui_add_play_db
from file_explorer import FileBrowser
from lib_up import muta_dict_init
from file_properties_ui import Ui_MainWindow

from PyQt5 import QtGui, QtSql, QtCore, QtWidgets
import mutagen
from  anytree import Node

import sys, threading, re, logging, queue, json, shutil


import json

from PyQt5 import QtWidgets, QtCore


class QJsonTreeItem(object):
    
    """Python adaptation of https://github.com/dridk/QJsonModel
    Supports Python 2 and 3 with PySide, PySide2, PyQt4 or PyQt5.
    Requires https://github.com/mottosso/Qt.py
    Usage:
        Use it like you would the C++ version.
        >>> import qjsonmodel
        >>> model = qjsonmodel.QJsonModel()
        >>> model.load({"key": "value"})
    Test:
        Run the provided example to sanity check your Python,
        dependencies and Qt binding.
        $ python qjsonmodel.py
    Changes:
        This module differs from the C++ version in the following ways.
        1. Setters and getters are replaced by Python properties
        2. Objects are sorted by default, disabled via load(sort=False)
        3. load() takes a Python dictionary as opposed to
           a string or file handle.
            - To load from a string, use built-in `json.loads()`
                >>> import json
                >>> document = json.loads("{'key': 'value'}")
                >>> model.load(document)
            - To load from a file, use `with open(fname)`
                  >>> import json
                  >>> with open("file.json") as f:
                  ...    document = json.load(f)
                  ...    model.load(document)
    """    
    
    def __init__(self, parent=None):
        self._parent = parent

        self._key = ""
        self._value = ""
        self._type = None
        self._children = list()

    def appendChild(self, item):
        self._children.append(item)

    def child(self, row):
        return self._children[row]

    def parent(self):
        return self._parent

    def childCount(self):
        return len(self._children)

    def row(self):
        return (
            self._parent._children.index(self)
            if self._parent else 0
        )

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, typ):
        self._type = typ

    @classmethod
    def load(self, value, parent=None, sort=True):
        rootItem = QJsonTreeItem(parent)
        rootItem.key = "root"

        if isinstance(value, dict):
            items = (
                sorted(value.items())
                if sort else value.items()
            )

            for key, value in items:
                child = self.load(value, rootItem)
                child.key = key
                child.type = type(value)
                rootItem.appendChild(child)

        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = self.load(value, rootItem)
                child.key = str(index)
                child.type = type(value)
                rootItem.appendChild(child)

        else:
            rootItem.value = value
            rootItem.type = type(value)

        return rootItem


class QJsonModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(QJsonModel, self).__init__(parent)

        self._rootItem = QJsonTreeItem()
        self._headers = ("Folders", "Files")

    def load(self, document):
        """Load from dictionary
        Arguments:
            document (dict): JSON-compatible dictionary
        """

        assert isinstance(document, (dict, list, tuple)), (
            "`document` must be of dict, list or tuple, "
            "not %s" % type(document)
        )

        self.beginResetModel()

        self._rootItem = QJsonTreeItem.load(document)
        self._rootItem.type = type(document)

        self.endResetModel()

        return True

    def json(self, root=None):
        """Serialise model as JSON-compliant dictionary
        Arguments:
            root (QJsonTreeItem, optional): Serialise from here
                defaults to the the top-level item
        Returns:
            model as dict
        """

        root = root or self._rootItem
        return self.genJson(root)

    def data(self, index, role):
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == QtCore.Qt.DisplayRole:
            if index.column() == 0:
                return item.key

            if index.column() == 1:
                return item.value

        elif role == QtCore.Qt.EditRole:
            if index.column() == 1:
                return item.value

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            if index.column() == 1:
                item = index.internalPointer()
                item.value = str(value)
                self.dataChanged.emit(index, index, [QtCore.Qt.EditRole])
                return True
        return False

    def headerData(self, section, orientation, role):
        if role != QtCore.Qt.DisplayRole:
            return None

        if orientation == QtCore.Qt.Horizontal:
            return self._headers[section]

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def flags(self, index):
        flags = super(QJsonModel, self).flags(index)

        if index.column() == 1:
            return QtCore.Qt.ItemIsEditable | flags
        else:
            return flags

    def genJson(self, item):
        nchild = item.childCount()

        if item.type is dict:
            document = {}
            for i in range(nchild):
                ch = item.child(i)
                document[ch.key] = self.genJson(ch)
            return document

        elif item.type == list:
            document = []
            for i in range(nchild):
                ch = item.child(i)
                document.append(self.genJson(ch))
            return document

        else:
            return item.value
class File_manupulator(Ui_MainWindow, QtWidgets.QMainWindow):
    
    def __init__(self, data = []):
        super(File_manupulator, self).__init__()      
        self.setupUi(self)
        self.theme_setter = Theme_manup(self.__dict__)
        self.theme_setter.setTheme(None) # no args = default , None is no theme
        self.ui_init()

        self.internal_states()

        self.file_data = data # list with all data
        self.file_list = []   # list with subset of all data
        self.preview_tree()
        self.Table_model_init()

    def internal_states(self):
        self.dest = self.FO_dest_line_edit.text() if os.path.isdir(self.FO_dest_line_edit.text()) else False
        self.orginize = self.FO_orginize.isChecked() 
        self.auto_tag = self.FO_tagger_check.isChecked()
        if self.FO_copy_rad.isChecked():
            self.mode = "copy"
        if self.FO_move_rad.isChecked():
            self.mode = "move"        
    
    def ui_init(self):
        # sets up the ui and binds the buttons
        self.FO_cbox.addItems(["Artist", "Album", "Genre", "Composer", "Date"])
        self.FO_cbox.setCurrentIndex(0)
        
        self.FO_cbox_2.addItems(["Artist", "Album", "Genre", "Composer", "Date"])
        self.FO_cbox_2.setCurrentIndex(4)
        
        self.FO_cbox_3.addItems(["Artist", "Album", "Genre", "Composer", "Date"])
        self.FO_cbox_3.setCurrentIndex(2)
        
        self.FO_copy_rad
        self.FO_move_rad
        self.FO_preview_push.pressed.connect(lambda: self.preview_tree())
        self.FO_start_push.pressed.connect(lambda: self.file_orginizer(self.directory_tree, self.dest))
        self.FO_cancel_push
    
    def data_format(self):
        # returns the sql data format to pass
        print("artist, album, genre, composer, date, path")
    
    def get_directory_tree(self):
        # returns the directory tree
        print(json.dumps(self.directory_tree, indent = 1))

    def preview_tree(self):
        # runs the preview button function
        if len(set([self.FO_cbox.currentIndex(), 
                    self.FO_cbox_2.currentIndex(), 
                    self.FO_cbox_3.currentIndex()])) == 3:        
            self.path_dict()
            self.directory_tree = self.tree_creator(self.file_list)
            self.Tree_model_init()

    def Table_model_init(self):
        # declares file to impoer table model
        self.table_model = QtGui.QStandardItemModel()
        self.table_model.appendColumn([QtGui.QStandardItem(item[-1]) for item in self.file_list])
        self.file_path_table.setModel(self.table_model)
    
    
    def Tree_model_init(self):
        # declares the tree and load the json directory tree
        self.tree_model = QJsonModel()
        self.tree_model.load(self.directory_tree)
        self.ditect_tree_view.setModel(self.tree_model)    
        self.ditect_tree_view.expandAll()
    
    def path_dict(self):
        # genetates the file list to generate the directpory tree
        self.import_tree_structure_init()
        self.file_list = []
        struct = self.root_tree
        data = self.file_data[1]
        self.file_list = [[data[struct[0]], data[struct[1]], data[struct[2]], data[-1]] for data in self.file_data]

    def tree_creator(self, data):
        main_tree = {}
        level = 0
        while level != 4:
            for i in data:
                if level == 0:
                    main_tree[i[:level + 1][0]] = None
    
                if level == 1:
                    a, b = i[:level + 1]
                    if main_tree[a] == None:
                        main_tree[a] = {b: None}
                    else:
                        main_tree[a][b] = None
                    
                if level == 2:
                    a, b, c = i[:level + 1]
                    if main_tree[a][b] == None:                       
                        main_tree[a][b] = {c: None}
                    else:
                        main_tree[a][b][c] = None
                    
                if level == 3:
                    a, b, c, d = i[:level + 1]
                    if main_tree[a][b][c] == None:
                        main_tree[a][b][c] = [d]
                    else:
                        (main_tree[a][b][c]).extend([d])
            level += 1        
        return main_tree    
        

    def import_tree_structure_init(self, struct = [0, 4, 2]):
        # creates initial directory struct    
        self.root_tree = [self.FO_cbox.currentIndex(), 
                          self.FO_cbox_2.currentIndex(), 
                          self.FO_cbox_3.currentIndex()]


    def isAvaliable(self, path: ""):
        # checks for file
        return os.path.isfile(path)
    
    def flatter(self, a):
        # takes the dictonary and converts it to a flat repr of the directory recursively\
        # and outputs a list
        temp_list = []
        if not isinstance(a, dict):
            return a
        else:
            for k, v in a.items():
                data = self.flatter(v)
                if isinstance(data, list):
                    temp_list.extend([''.join([str(k), '/', str(i)]) for i in data])
                else:
                    temp_list.extend([''.join([str(k), '/', str(data)])])
            return temp_list    
    
    def directory_creator(self, direct_tree, dest, flag = "copy"):
        # in directory
        list_files = self.flatter(direct_tree)
        
        # takes a list and creates the file structure in the file system and moves pr copies the file
        main_dir = dest
        os.chdir(main_dir)    
        for item in list_files:
            try:
                dire = os.getcwd()
                for index, value in enumerate(item.split("/")):
                    if index == 3:
                        try:
                            if flag == "move":
                                shutil.move(value, dire)
                            if flag == "copy":
                                shutil.copyfile(value, dire)
                        except Exception as e:
                            pass
                    else:
                        value = value.translate(str.maketrans({'<': "_",
                                                               '>': "_",
                                                               ':': "_",
                                                               '"': "'",
                                                               '/': "_",
                                                               '\\': "_",
                                                               '|': "_",
                                                               '?': "_",
                                                               '*': "_"})).strip()
                        dire = os.path.join(dire, value)
                        if os.path.isdir(dire):
                            # checks and moves inside
                            os.chdir(dire)
                        else:
                            # creates directory
                            os.mkdir(dire)
                            # checks and moves inside
                            os.chdir(dire)
                # resets to the root
                os.chdir(main_dir)
            except Exception as e:
                print(value, e)
            return True    
    
    def file_orginizer(self, data, dest):
        if self.directory_creator(data, dest, self.mode):
            print("Done")
        
    def load_tags(self, fname):
        self.muta_easy_obj = muta_dict_init(fname)
        self.muta_obj = mutagen.File(fname)
        try:
            pixmap = QtGui.QPixmap()
            self.cover = [(self.muta_obj.get(i)).data for i in self.muta_obj.keys() if  re.search("APIC:", i)].pop()
            pixmap.loadFromData(self.cover)
            self.cover = pixmap.scaled(300, 300)
        except:
            self.cover = pixmap.scaled(300, 300)
        
        try:
            self.lyrics = [(self.muta_obj.get(i)).text for i in self.muta_obj.keys() if  re.search("USLT:", i)].pop()
        except:
            self.lyrics = 'None'

    def data_setter(self):
        self.FO_cover_pixmap.setPixmap(self.cover)
        self.FO_cover_pixmap.setScaledContents(True)
        self.FO_lyrics.setText(self.lyrics)
        self.tagger_table_model = QtGui.QStandardItemModel()
        item_list = [[QtGui.QStandardItem(k.replace("_", ' ').title()), QtGui.QStandardItem(v)]for k, v in self.muta_easy_obj.items()]
        [self.tagger_table_model.appendRow(item) for item in item_list]
        self.tagger_table.setModel(self.tagger_table_model)

    def tagging_loop(self, file_list):
        if self.FO_auto_rad.isChecked():
            for file in file_list:
                self.auto_tagger_auto(file)
                
        if self.FO_verbose_rad.isChecked():
            pass
    
    def auto_tagger_auto(self, file):
        self.load_tags(file)
        [self.muta_easy_obj, self.cover, self.lyrics, self.muta_obj]
    
    def auto_tagger_verbose(self, file):
        self.load_tags(file)
        self.data_setter()
        [self.muta_easy_obj, self.cover, self.lyrics, self.muta_obj]
    
    
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    data = database_connector_sql_exe("SELECT artist, album, genre, composer, date, path FROM library")
    main_app = File_manupulator(data)
    main_app.show()
    app.exec_()    
