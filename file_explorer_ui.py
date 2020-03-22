# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\file_explorer.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_file_exp(object):
    def setupUi(self, MainWindow_file_exp):
        MainWindow_file_exp.setObjectName("MainWindow_file_exp")
        MainWindow_file_exp.setEnabled(True)
        MainWindow_file_exp.resize(739, 553)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow_file_exp.sizePolicy().hasHeightForWidth())
        MainWindow_file_exp.setSizePolicy(sizePolicy)
        MainWindow_file_exp.setMaximumSize(QtCore.QSize(6120, 3000))
        MainWindow_file_exp.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/file_explorer/icons8-sound-wave-32.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow_file_exp.setWindowIcon(icon)
        MainWindow_file_exp.setWindowOpacity(1.0)
        MainWindow_file_exp.setAutoFillBackground(False)
        MainWindow_file_exp.setStyleSheet("background-color: #24292E ;\n"
"font-family: Arial, Helvetica, sans-serif;\n"
"font-size: 14px;\n"
"letter-spacing: 2px;\n"
"word-spacing: 1.4px;\n"
"color: #D0D4D9;\n"
"font-weight: normal;\n"
"text-decoration: none;\n"
"font-style: normal;\n"
"font-variant: normal;\n"
"text-transform: none;")
        MainWindow_file_exp.setIconSize(QtCore.QSize(24, 24))
        MainWindow_file_exp.setDocumentMode(False)
        MainWindow_file_exp.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow_file_exp.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow_file_exp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(10, 2, 10, 6)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.grid = QtWidgets.QFrame(self.centralwidget)
        self.grid.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.grid.setObjectName("grid")
        self.gridLayout = QtWidgets.QGridLayout(self.grid)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 1, -1, -1)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_12 = QtWidgets.QLabel(self.grid)
        self.label_12.setText("")
        self.label_12.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout.addWidget(self.label_12)
        self.pushButton = QtWidgets.QPushButton(self.grid)
        self.pushButton.setMaximumSize(QtCore.QSize(74, 16777215))
        self.pushButton.setStyleSheet("\n"
"QPushButton {\n"
"background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 6px;\n"
"border-color: #000000;\n"
"min-width: 4em;\n"
"padding: 6px;\n"
"}\n"
"QPushButton:pressed {\n"
"       background-color: rgb(47, 54, 67);\n"
"    border-style: inset;\n"
"}")
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.grid)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setStyleSheet("\n"
"QPushButton {\n"
"background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 6px;\n"
"border-color: #000000;\n"
"min-width: 4em;\n"
"padding: 6px;\n"
"}\n"
"QPushButton:pressed {\n"
"       background-color: rgb(47, 54, 67);\n"
"    border-style: inset;\n"
"}")
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.progressBar_file_add = QtWidgets.QProgressBar(self.grid)
        self.progressBar_file_add.setEnabled(True)
        self.progressBar_file_add.setProperty("value", 0)
        self.progressBar_file_add.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_file_add.setInvertedAppearance(False)
        self.progressBar_file_add.setObjectName("progressBar_file_add")
        self.gridLayout.addWidget(self.progressBar_file_add, 2, 0, 1, 2)
        self.treeView = QtWidgets.QTreeView(self.grid)
        self.treeView.setMouseTracking(False)
        self.treeView.setAutoFillBackground(True)
        self.treeView.setStyleSheet("QTreeView {\n"
"    show-decoration-selected: 1;\n"
"    background-color: rgb(47, 54, 67);\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"     border: 2px solid grey;\n"
"     background: #32CC99;\n"
"     width: 10px;\n"
"     margin: 0px 0 0px 0;\n"
" }\n"
" QScrollBar::handle:vertical {\n"
"background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.130682 rgba(59, 78, 97, 255), stop:0.539773 rgba(40, 88, 135, 255), stop:0.744318 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
"     min-height: 20px;\n"
" }\n"
"\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"none\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"background-color: rgb(36, 41, 46);\n"
" }\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 2px solid grey;\n"
"     background: #32CC99;\n"
"     width: 10px;\n"
"     margin: 0px 0 0px 0;\n"
" }\n"
" QScrollBar::handle:horizontal {\n"
"background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.130682 rgba(59, 78, 97, 255), stop:0.539773 rgba(40, 88, 135, 255), stop:0.744318 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
"     min-height: 20px;\n"
" }\n"
"\n"
" QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
"none\n"
" }\n"
"\n"
" QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
"background-color: rgb(36, 41, 46);\n"
" }\n"
"\n"
"QHeaderView::section { color:white; background-color:#232326; }\n"
"\n"
"QTreeView::item {\n"
"     border: none\n"
"}\n"
"QTreeView::item:hover {  \n"
"    background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.130682 rgba(59, 78, 97, 255), stop:0.539773 rgba(40, 88, 135, 255), stop:0.744318 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
"    border: 1px solid #000000;\n"
"}\n"
"QTreeView::item:selected {\n"
"    border: 1px solid rgb(36, 41, 46);\n"
"}\n"
"\n"
"QTreeView::item:selected:active{ \n"
"    background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
"}\n"
"\n"
"QTreeView::item:selected:!active {\n"
"background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:0, y2:1, stop:0 rgba(36, 41, 46, 255), stop:0.0909091 rgba(59, 78, 97, 255), stop:0.255682 rgba(40, 88, 135, 255), stop:0.619318 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
"}\n"
"")
        self.treeView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.treeView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeView.setDragEnabled(True)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.treeView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.treeView.setAutoExpandDelay(1)
        self.treeView.setIndentation(15)
        self.treeView.setUniformRowHeights(True)
        self.treeView.setSortingEnabled(True)
        self.treeView.setAllColumnsShowFocus(True)
        self.treeView.setWordWrap(True)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setDefaultSectionSize(1)
        self.treeView.header().setHighlightSections(False)
        self.gridLayout.addWidget(self.treeView, 0, 1, 1, 1)
        self.listView = QtWidgets.QListView(self.grid)
        self.listView.setAutoFillBackground(True)
        self.listView.setStyleSheet("background-color: rgb(47, 54, 67);")
        self.listView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listView.setAlternatingRowColors(False)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.grid, 0, 0, 1, 1)
        MainWindow_file_exp.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow_file_exp)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_file_exp)

    def retranslateUi(self, MainWindow_file_exp):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_file_exp.setWindowTitle(_translate("MainWindow_file_exp", "File Explorer"))
        self.pushButton.setText(_translate("MainWindow_file_exp", "Scan"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow_file_exp = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_file_exp()
    ui.setupUi(MainWindow_file_exp)
    MainWindow_file_exp.show()
    sys.exit(app.exec_())
