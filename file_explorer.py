from PyQt5 import QtWidgets
from PyQt5  import QtGui
from PyQt5  import QtCore
import re, os, json, tinytag, sys, time

try:
    from . import file_explorer_ui
except:
    import file_explorer_ui
    
class FileBrowser(file_explorer_ui.Ui_MainWindow_file_exp, QtWidgets.QMainWindow):
    def __init__(self, *args):
        super(FileBrowser, self).__init__()
        sys.path.append(os.path.split(os.getcwd())[0])
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()
        self.context_list_view()
        self.buttonBox.accepted.connect(self.scan_folder_ok)
        self.buttonBox.rejected.connect(self.cancle)
        self.pushButton.pressed.connect(self.folder_scanner)
      
        
    def music_metadata_reader(self, filename):
        def file_parser(direct, file):
            path = (direct+"/"+file)
            tag = tinytag.TinyTag.get(path)
            tag = tag.as_dict()
            del tag["comment"]
            tag["date_added"] = time.ctime()
            tag["file_format"] = os.path.splitext(path)[1]
            return {"file_path":direct + '/' + file,"meta_data":tag}
        
        
        with open(filename) as json_file:
            data = json.load(json_file)["music_files"]
            list_data = []
            for dictonary in data:
                for item,direct in zip(dictonary.values(),dictonary.keys()) :
                    for file in item:
                        list_data.append(file_parser(direct, file))
        

        with open("resources\\settings\\Music_library_data.txt", 'w') as json_file:
            json.dump(list_data, json_file, indent = 2)
            json_file.close()
        

    def folder_scanner(self):
        self.progressBar_file_add.setProperty("value",0)
        self.scan_folder_ok() 
        with open('resources\\settings\\config.txt') as json_file:
            data = json.load(json_file)
            stringlist = data["file_path"]
            format_accepted = set([key for (key,value) in data["file_format_selected"].items() if value[0] == 1 ])
            all_items = []; temp = []; temp1 = []
        for path in stringlist:                
            file_bulk = os.walk(path)
            self.label_12.setText("Scanning Library")
            for (directoy, sub_dir, files)in file_bulk:
                temp = []
                for item in files:
                    if format_accepted.intersection(set(re.findall('\..{3,5}$', item))) != set():
                        temp.append(item)
                if  directoy.replace("\\", '/') not in temp1 and temp != []:       
                    temp1.append(directoy)
                    all_items.append({directoy : temp})
        
        self.progressBar_file_add.setProperty("value",100)    
        self.settings_file_update(all_items, flag="music_files", owr=True, filename = "resources\\settings\\music_listing.txt")
        self.music_metadata_reader(filename = "resources\\settings\\music_listing.txt")
        self.label_12.setText("Scanning Library Completed")
        self.cancle()
            
        
    def update_check_box(self):
        index = self.listView.currentIndex()
        row, col = index.row(), index.column()
        item = self.model_list.itemFromIndex(index)
        if item == None:
            return ""            
        if item.checkState() == 0:    
            check = QtCore.Qt.Checked
        else:
            check = QtCore.Qt.Unchecked
            
        item.setCheckState(check)
        item.setEditable(False)
        self.model_list.setItem(row, col, item)
        self.listView.setModel(self.model_list)
       
        
    def scan_folder_ok(self):
        index = 0
        string = []
        while self.model_list.item(index) != None:
            checked_file = self.model_list.item(index)
            if checked_file.checkState() != 0:
                data = self.model_list.data(checked_file.index())
                string.append(data)
            index = index + 1
        self.settings_file_update(string, flag="file_path", owr=True)
                
    def populate(self):
        path = r""
        self.model = QtWidgets.QFileSystemModel()
        self.model_list = QtGui.QStandardItemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)


    def context_menu(self):    
        menu = QtWidgets.QMenu()
        open = menu.addAction("Add Folder to library")
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())
    
    
    def context_list_view(self):         
        # this writes the list view and updates it
        # accordingly " as add a folder " is clicked
        with open('resources\\settings\\config.txt') as json_file:
            data = json.load(json_file)
            stringlist = data["file_path"]
            self.model_list.clear()
            if stringlist is not None:
                for i in range(len(stringlist)):
                    item = QtGui.QStandardItem(stringlist[i])
                    item.setCheckable(True)
                    check = QtCore.Qt.Checked 
                    item.setCheckState(check)
                    item.setEditable(False)
                    self.model_list.appendRow(item)
        self.listView.setModel(self.model_list)
        self.listView.clicked['QModelIndex'].connect(self.update_check_box)     
    
    
    def settings_file_update(self, string, flag = None, owr = False, emp = False, filename = 'resources\\settings\\config.txt'):
        with open(filename) as json_file:
            data = json.load(json_file)
            if string not in data[flag] and not (owr):
                data[flag].append(string)
            if string not in data[flag] and (owr):
                if not emp:
                    data[flag] = string            
    
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent =2)
            json_file.close()
        self.context_list_view()
        

    def open_file(self):
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        if  re.findall('\.[A-Za-z]{0,5}$', file_path) != []:
            self.label_12.setText('Select a folder')
        else:
            self.label_12.setText(file_path)
            self.settings_file_update(file_path, "file_path")
    
            
    def cancle(self):
        self.close()
    
    
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    file_browser_app = FileBrowser()
    file_browser_app.show()
    app.exec_()

