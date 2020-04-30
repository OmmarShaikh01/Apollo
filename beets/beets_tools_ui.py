# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beets_tools.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 729)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridFrame = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.gridFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.rescan_toolb = QtWidgets.QToolButton(self.gridFrame)
        self.rescan_toolb.setMinimumSize(QtCore.QSize(54, 0))
        self.rescan_toolb.setObjectName("rescan_toolb")
        self.gridLayout_3.addWidget(self.rescan_toolb, 3, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 3, 0, 1, 1)
        self.add_toolb = QtWidgets.QToolButton(self.gridFrame)
        self.add_toolb.setMinimumSize(QtCore.QSize(54, 0))
        self.add_toolb.setObjectName("add_toolb")
        self.gridLayout_3.addWidget(self.add_toolb, 3, 3, 1, 1)
        self.line = QtWidgets.QFrame(self.gridFrame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 4, 0, 1, 5)
        self.dir_paths_lis = QtWidgets.QListView(self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dir_paths_lis.sizePolicy().hasHeightForWidth())
        self.dir_paths_lis.setSizePolicy(sizePolicy)
        self.dir_paths_lis.setMinimumSize(QtCore.QSize(0, 183))
        self.dir_paths_lis.setObjectName("dir_paths_lis")
        self.gridLayout_3.addWidget(self.dir_paths_lis, 0, 0, 3, 5)
        self.remove_toolb = QtWidgets.QToolButton(self.gridFrame)
        self.remove_toolb.setMinimumSize(QtCore.QSize(54, 0))
        self.remove_toolb.setObjectName("remove_toolb")
        self.gridLayout_3.addWidget(self.remove_toolb, 3, 2, 1, 1)
        self.list_files = QtWidgets.QToolButton(self.gridFrame)
        self.list_files.setMinimumSize(QtCore.QSize(54, 0))
        self.list_files.setObjectName("list_files")
        self.gridLayout_3.addWidget(self.list_files, 3, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_3, 0, 0, 1, 2)
        self.stackedWidget = QtWidgets.QStackedWidget(self.gridFrame)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.page)
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(self.page)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 1, 0, 1, 1)
        self.status_log = QtWidgets.QTextBrowser(self.page)
        self.status_log.setObjectName("status_log")
        self.gridLayout_5.addWidget(self.status_log, 2, 0, 1, 1)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.stackedWidget, 1, 0, 1, 2)
        self.gridLayout_2.addWidget(self.gridFrame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.rescan_toolb.setText(_translate("MainWindow", "Scan"))
        self.add_toolb.setText(_translate("MainWindow", "Add"))
        self.remove_toolb.setText(_translate("MainWindow", "Remove"))
        self.list_files.setText(_translate("MainWindow", "List Files Added"))
        self.label.setText(_translate("MainWindow", "Import Log"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
