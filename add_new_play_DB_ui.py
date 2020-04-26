# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\add_new_play_DB.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_add_play_db(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui_add_play_db, self).__init__()
        self.setupUi(self)
        
    def setupUi(self, add_play_db):
        add_play_db.setObjectName("add_play_db")
        add_play_db.resize(377, 154)
        add_play_db.setMinimumSize(QtCore.QSize(377, 154))
        add_play_db.setMaximumSize(QtCore.QSize(377, 154))
        self.centralwidget = QtWidgets.QWidget(add_play_db)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 2, 3, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setMaxLength(50)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 3, 0, 1, 3)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        add_play_db.setCentralWidget(self.centralwidget)

        self.retranslateUi(add_play_db)
        QtCore.QMetaObject.connectSlotsByName(add_play_db)

    def retranslateUi(self, add_play_db):
        _translate = QtCore.QCoreApplication.translate
        add_play_db.setWindowTitle(_translate("add_play_db", "MainWindow"))
        self.label.setText(_translate("add_play_db", "Add New Playlist"))
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    add_play_db = QtWidgets.QMainWindow()
    ui = Ui_add_play_db()
    ui.show()
    sys.exit(app.exec_())
