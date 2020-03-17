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
        MainWindow_file_exp.setAutoFillBackground(True)
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
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setMouseTracking(False)
        self.treeView.setAutoFillBackground(True)
        self.treeView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.treeView.setFrameShadow(QtWidgets.QFrame.Sunken)
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
        self.gridLayout.addWidget(self.treeView, 0, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 1, -1, -1)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.outputlabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.outputlabel.setFont(font)
        self.outputlabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outputlabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.outputlabel.setText("")
        self.outputlabel.setScaledContents(True)
        self.outputlabel.setObjectName("outputlabel")
        self.horizontalLayout.addWidget(self.outputlabel)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMaximumSize(QtCore.QSize(74, 16777215))
        self.pushButton.setCheckable(False)
        self.pushButton.setAutoDefault(False)
        self.pushButton.setDefault(False)
        self.pushButton.setFlat(False)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 2)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setAutoFillBackground(True)
        self.listView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.listView.setAlternatingRowColors(True)
        self.listView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 0, 0, 1, 1)
        self.progressBar_file_add = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_file_add.setEnabled(True)
        self.progressBar_file_add.setProperty("value", 0)
        self.progressBar_file_add.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_file_add.setInvertedAppearance(False)
        self.progressBar_file_add.setObjectName("progressBar_file_add")
        self.gridLayout.addWidget(self.progressBar_file_add, 2, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
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
