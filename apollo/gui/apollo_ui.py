# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'apollo.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 745)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(0)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(0)
        self.splitter.setObjectName("splitter")
        self.apollo_TABWG_main = QtWidgets.QTabWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_TABWG_main.sizePolicy().hasHeightForWidth())
        self.apollo_TABWG_main.setSizePolicy(sizePolicy)
        self.apollo_TABWG_main.setTabBarAutoHide(False)
        self.apollo_TABWG_main.setObjectName("apollo_TABWG_main")
        self.apollo_WDG_LBT_frame = QtWidgets.QWidget()
        self.apollo_WDG_LBT_frame.setObjectName("apollo_WDG_LBT_frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.apollo_WDG_LBT_frame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.apollo_VSP_LBT_splitter = QtWidgets.QSplitter(self.apollo_WDG_LBT_frame)
        self.apollo_VSP_LBT_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.apollo_VSP_LBT_splitter.setHandleWidth(0)
        self.apollo_VSP_LBT_splitter.setObjectName("apollo_VSP_LBT_splitter")
        self.apollo_FR_LBT_group = QtWidgets.QFrame(self.apollo_VSP_LBT_splitter)
        self.apollo_FR_LBT_group.setObjectName("apollo_FR_LBT_group")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.apollo_FR_LBT_group)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.apollo_TLB_LBT_grouptool = QtWidgets.QToolButton(self.apollo_FR_LBT_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_TLB_LBT_grouptool.sizePolicy().hasHeightForWidth())
        self.apollo_TLB_LBT_grouptool.setSizePolicy(sizePolicy)
        self.apollo_TLB_LBT_grouptool.setMinimumSize(QtCore.QSize(0, 32))
        self.apollo_TLB_LBT_grouptool.setMaximumSize(QtCore.QSize(16777215, 32))
        self.apollo_TLB_LBT_grouptool.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        self.apollo_TLB_LBT_grouptool.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.apollo_TLB_LBT_grouptool.setObjectName("apollo_TLB_LBT_grouptool")
        self.verticalLayout.addWidget(self.apollo_TLB_LBT_grouptool)
        self.apollo_TBV_LBT_grouptable = QtWidgets.QTableView(self.apollo_FR_LBT_group)
        self.apollo_TBV_LBT_grouptable.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_TBV_LBT_grouptable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.apollo_TBV_LBT_grouptable.setProperty("showDropIndicator", False)
        self.apollo_TBV_LBT_grouptable.setDragDropOverwriteMode(False)
        self.apollo_TBV_LBT_grouptable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.apollo_TBV_LBT_grouptable.setTextElideMode(QtCore.Qt.ElideNone)
        self.apollo_TBV_LBT_grouptable.setShowGrid(False)
        self.apollo_TBV_LBT_grouptable.setSortingEnabled(True)
        self.apollo_TBV_LBT_grouptable.setWordWrap(False)
        self.apollo_TBV_LBT_grouptable.setCornerButtonEnabled(False)
        self.apollo_TBV_LBT_grouptable.setObjectName("apollo_TBV_LBT_grouptable")
        self.apollo_TBV_LBT_grouptable.horizontalHeader().setVisible(False)
        self.apollo_TBV_LBT_grouptable.verticalHeader().setVisible(False)
        self.apollo_TBV_LBT_grouptable.verticalHeader().setDefaultSectionSize(24)
        self.apollo_TBV_LBT_grouptable.verticalHeader().setMinimumSectionSize(24)
        self.verticalLayout.addWidget(self.apollo_TBV_LBT_grouptable)
        self.apollo_FR_LBT_groupsearch = QtWidgets.QFrame(self.apollo_FR_LBT_group)
        self.apollo_FR_LBT_groupsearch.setMinimumSize(QtCore.QSize(0, 32))
        self.apollo_FR_LBT_groupsearch.setMaximumSize(QtCore.QSize(16777215, 32))
        self.apollo_FR_LBT_groupsearch.setObjectName("apollo_FR_LBT_groupsearch")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.apollo_FR_LBT_groupsearch)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.apollo_LEDT_LBT_groupsearch = QtWidgets.QLineEdit(self.apollo_FR_LBT_groupsearch)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_LEDT_LBT_groupsearch.sizePolicy().hasHeightForWidth())
        self.apollo_LEDT_LBT_groupsearch.setSizePolicy(sizePolicy)
        self.apollo_LEDT_LBT_groupsearch.setMinimumSize(QtCore.QSize(0, 24))
        self.apollo_LEDT_LBT_groupsearch.setMaximumSize(QtCore.QSize(16777215, 24))
        self.apollo_LEDT_LBT_groupsearch.setObjectName("apollo_LEDT_LBT_groupsearch")
        self.horizontalLayout.addWidget(self.apollo_LEDT_LBT_groupsearch)
        self.verticalLayout.addWidget(self.apollo_FR_LBT_groupsearch)
        self.apollo_FR_LBT_frame_maintable = QtWidgets.QFrame(self.apollo_VSP_LBT_splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_FR_LBT_frame_maintable.sizePolicy().hasHeightForWidth())
        self.apollo_FR_LBT_frame_maintable.setSizePolicy(sizePolicy)
        self.apollo_FR_LBT_frame_maintable.setObjectName("apollo_FR_LBT_frame_maintable")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.apollo_FR_LBT_frame_maintable)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.apollo_TBV_LBT_maintable = QtWidgets.QTableView(self.apollo_FR_LBT_frame_maintable)
        self.apollo_TBV_LBT_maintable.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_TBV_LBT_maintable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.apollo_TBV_LBT_maintable.setProperty("showDropIndicator", False)
        self.apollo_TBV_LBT_maintable.setDragDropOverwriteMode(False)
        self.apollo_TBV_LBT_maintable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.apollo_TBV_LBT_maintable.setTextElideMode(QtCore.Qt.ElideNone)
        self.apollo_TBV_LBT_maintable.setShowGrid(False)
        self.apollo_TBV_LBT_maintable.setSortingEnabled(True)
        self.apollo_TBV_LBT_maintable.setWordWrap(False)
        self.apollo_TBV_LBT_maintable.setCornerButtonEnabled(False)
        self.apollo_TBV_LBT_maintable.setObjectName("apollo_TBV_LBT_maintable")
        self.apollo_TBV_LBT_maintable.verticalHeader().setVisible(False)
        self.apollo_TBV_LBT_maintable.verticalHeader().setDefaultSectionSize(24)
        self.apollo_TBV_LBT_maintable.verticalHeader().setMinimumSectionSize(24)
        self.verticalLayout_2.addWidget(self.apollo_TBV_LBT_maintable)
        self.apollo_FR_LBT_buttons_maintable = QtWidgets.QFrame(self.apollo_FR_LBT_frame_maintable)
        self.apollo_FR_LBT_buttons_maintable.setMinimumSize(QtCore.QSize(0, 32))
        self.apollo_FR_LBT_buttons_maintable.setMaximumSize(QtCore.QSize(16777215, 32))
        self.apollo_FR_LBT_buttons_maintable.setObjectName("apollo_FR_LBT_buttons_maintable")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.apollo_FR_LBT_buttons_maintable)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.apollo_PSB_LBT_addtrack = QtWidgets.QPushButton(self.apollo_FR_LBT_buttons_maintable)
        self.apollo_PSB_LBT_addtrack.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_LBT_addtrack.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_LBT_addtrack.setFlat(True)
        self.apollo_PSB_LBT_addtrack.setObjectName("apollo_PSB_LBT_addtrack")
        self.horizontalLayout_2.addWidget(self.apollo_PSB_LBT_addtrack)
        self.apollo_PSB_LBT_subtrack = QtWidgets.QPushButton(self.apollo_FR_LBT_buttons_maintable)
        self.apollo_PSB_LBT_subtrack.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_LBT_subtrack.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_LBT_subtrack.setFlat(True)
        self.apollo_PSB_LBT_subtrack.setObjectName("apollo_PSB_LBT_subtrack")
        self.horizontalLayout_2.addWidget(self.apollo_PSB_LBT_subtrack)
        self.apollo_PSB_LBT_options = QtWidgets.QPushButton(self.apollo_FR_LBT_buttons_maintable)
        self.apollo_PSB_LBT_options.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_LBT_options.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_LBT_options.setFlat(True)
        self.apollo_PSB_LBT_options.setObjectName("apollo_PSB_LBT_options")
        self.horizontalLayout_2.addWidget(self.apollo_PSB_LBT_options)
        self.apollo_LEDT_LBT_main_search = QtWidgets.QLineEdit(self.apollo_FR_LBT_buttons_maintable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_LEDT_LBT_main_search.sizePolicy().hasHeightForWidth())
        self.apollo_LEDT_LBT_main_search.setSizePolicy(sizePolicy)
        self.apollo_LEDT_LBT_main_search.setMinimumSize(QtCore.QSize(0, 24))
        self.apollo_LEDT_LBT_main_search.setMaximumSize(QtCore.QSize(16777215, 24))
        self.apollo_LEDT_LBT_main_search.setObjectName("apollo_LEDT_LBT_main_search")
        self.horizontalLayout_2.addWidget(self.apollo_LEDT_LBT_main_search)
        self.apollo_PSB_LBT_tablesearch = QtWidgets.QPushButton(self.apollo_FR_LBT_buttons_maintable)
        self.apollo_PSB_LBT_tablesearch.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_LBT_tablesearch.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_LBT_tablesearch.setFlat(True)
        self.apollo_PSB_LBT_tablesearch.setObjectName("apollo_PSB_LBT_tablesearch")
        self.horizontalLayout_2.addWidget(self.apollo_PSB_LBT_tablesearch)
        self.verticalLayout_2.addWidget(self.apollo_FR_LBT_buttons_maintable)
        self.gridLayout_3.addWidget(self.apollo_VSP_LBT_splitter, 0, 0, 1, 1)
        self.apollo_TABWG_main.addTab(self.apollo_WDG_LBT_frame, "")
        self.apollo_WDG_NPQ_frame = QtWidgets.QWidget()
        self.apollo_WDG_NPQ_frame.setObjectName("apollo_WDG_NPQ_frame")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.apollo_WDG_NPQ_frame)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.apollo_FR_NPQ_footer = QtWidgets.QFrame(self.apollo_WDG_NPQ_frame)
        self.apollo_FR_NPQ_footer.setMinimumSize(QtCore.QSize(0, 32))
        self.apollo_FR_NPQ_footer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_FR_NPQ_footer.setObjectName("apollo_FR_NPQ_footer")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.apollo_FR_NPQ_footer)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setHorizontalSpacing(8)
        self.gridLayout_5.setVerticalSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem = QtWidgets.QSpacerItem(383, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 1, 0, 1, 1)
        self.apollo_PSB_NPQ_pause = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_pause.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_pause.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_pause.setFlat(True)
        self.apollo_PSB_NPQ_pause.setObjectName("apollo_PSB_NPQ_pause")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_pause, 1, 1, 1, 1)
        self.apollo_PSB_NPQ_seekf = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_seekf.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_seekf.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_seekf.setFlat(True)
        self.apollo_PSB_NPQ_seekf.setObjectName("apollo_PSB_NPQ_seekf")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_seekf, 1, 2, 1, 1)
        self.apollo_PSB_NPQ_skipback = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_skipback.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_skipback.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_skipback.setFlat(True)
        self.apollo_PSB_NPQ_skipback.setObjectName("apollo_PSB_NPQ_skipback")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_skipback, 1, 3, 1, 1)
        self.apollo_PSB_NPQ_seekb = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_seekb.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_seekb.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_seekb.setFlat(True)
        self.apollo_PSB_NPQ_seekb.setObjectName("apollo_PSB_NPQ_seekb")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_seekb, 1, 4, 1, 1)
        self.apollo_PSB_NPQ_skipfront = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_skipfront.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_skipfront.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_skipfront.setFlat(True)
        self.apollo_PSB_NPQ_skipfront.setObjectName("apollo_PSB_NPQ_skipfront")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_skipfront, 1, 5, 1, 1)
        self.apollo_PSB_NPQ_stop = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_stop.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_stop.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_stop.setFlat(True)
        self.apollo_PSB_NPQ_stop.setObjectName("apollo_PSB_NPQ_stop")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_stop, 1, 6, 1, 1)
        self.apollo_PSB_NPQ_volume_main = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_volume_main.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_volume_main.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_volume_main.setFlat(True)
        self.apollo_PSB_NPQ_volume_main.setObjectName("apollo_PSB_NPQ_volume_main")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_volume_main, 1, 9, 1, 1)
        self.apollo_PSB_NPQ_play = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_play.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_play.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_play.setFlat(True)
        self.apollo_PSB_NPQ_play.setObjectName("apollo_PSB_NPQ_play")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_play, 1, 7, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(382, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 1, 8, 1, 1)
        self.apollo_PSB_NPQ_playstyle = QtWidgets.QPushButton(self.apollo_FR_NPQ_footer)
        self.apollo_PSB_NPQ_playstyle.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_playstyle.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_NPQ_playstyle.setFlat(True)
        self.apollo_PSB_NPQ_playstyle.setObjectName("apollo_PSB_NPQ_playstyle")
        self.gridLayout_5.addWidget(self.apollo_PSB_NPQ_playstyle, 1, 11, 1, 1)
        self.apollo_HSLD_NPQ_position = QtWidgets.QSlider(self.apollo_FR_NPQ_footer)
        self.apollo_HSLD_NPQ_position.setOrientation(QtCore.Qt.Horizontal)
        self.apollo_HSLD_NPQ_position.setObjectName("apollo_HSLD_NPQ_position")
        self.gridLayout_5.addWidget(self.apollo_HSLD_NPQ_position, 0, 0, 1, 12)
        self.apollo_HSLD_NPQ_volume_main = QtWidgets.QSlider(self.apollo_FR_NPQ_footer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_HSLD_NPQ_volume_main.sizePolicy().hasHeightForWidth())
        self.apollo_HSLD_NPQ_volume_main.setSizePolicy(sizePolicy)
        self.apollo_HSLD_NPQ_volume_main.setMinimumSize(QtCore.QSize(84, 15))
        self.apollo_HSLD_NPQ_volume_main.setOrientation(QtCore.Qt.Horizontal)
        self.apollo_HSLD_NPQ_volume_main.setObjectName("apollo_HSLD_NPQ_volume_main")
        self.gridLayout_5.addWidget(self.apollo_HSLD_NPQ_volume_main, 1, 10, 1, 1)
        self.gridLayout_6.addWidget(self.apollo_FR_NPQ_footer, 1, 0, 1, 1)
        self.apollo_PIXLB_NPQ_albumcover = QtWidgets.QLabel(self.apollo_WDG_NPQ_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.apollo_PIXLB_NPQ_albumcover.sizePolicy().hasHeightForWidth())
        self.apollo_PIXLB_NPQ_albumcover.setSizePolicy(sizePolicy)
        self.apollo_PIXLB_NPQ_albumcover.setMinimumSize(QtCore.QSize(55, 55))
        self.apollo_PIXLB_NPQ_albumcover.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.apollo_PIXLB_NPQ_albumcover.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_PIXLB_NPQ_albumcover.setObjectName("apollo_PIXLB_NPQ_albumcover")
        self.gridLayout_6.addWidget(self.apollo_PIXLB_NPQ_albumcover, 0, 0, 1, 1)
        self.apollo_TABWG_main.addTab(self.apollo_WDG_NPQ_frame, "")
        self.apollo_FR_nowplaying_queue = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_FR_nowplaying_queue.sizePolicy().hasHeightForWidth())
        self.apollo_FR_nowplaying_queue.setSizePolicy(sizePolicy)
        self.apollo_FR_nowplaying_queue.setMinimumSize(QtCore.QSize(300, 0))
        self.apollo_FR_nowplaying_queue.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_FR_nowplaying_queue.setFrameShadow(QtWidgets.QFrame.Raised)
        self.apollo_FR_nowplaying_queue.setObjectName("apollo_FR_nowplaying_queue")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.apollo_FR_nowplaying_queue)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.apollo_TBV_NPQ_maintable = QtWidgets.QTableView(self.apollo_FR_nowplaying_queue)
        self.apollo_TBV_NPQ_maintable.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_TBV_NPQ_maintable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.apollo_TBV_NPQ_maintable.setProperty("showDropIndicator", False)
        self.apollo_TBV_NPQ_maintable.setDragDropOverwriteMode(False)
        self.apollo_TBV_NPQ_maintable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.apollo_TBV_NPQ_maintable.setTextElideMode(QtCore.Qt.ElideNone)
        self.apollo_TBV_NPQ_maintable.setShowGrid(False)
        self.apollo_TBV_NPQ_maintable.setSortingEnabled(True)
        self.apollo_TBV_NPQ_maintable.setWordWrap(False)
        self.apollo_TBV_NPQ_maintable.setCornerButtonEnabled(False)
        self.apollo_TBV_NPQ_maintable.setObjectName("apollo_TBV_NPQ_maintable")
        self.apollo_TBV_NPQ_maintable.verticalHeader().setVisible(False)
        self.apollo_TBV_NPQ_maintable.verticalHeader().setDefaultSectionSize(24)
        self.apollo_TBV_NPQ_maintable.verticalHeader().setMinimumSectionSize(24)
        self.gridLayout_4.addWidget(self.apollo_TBV_NPQ_maintable, 2, 0, 1, 1)
        self.apollo_HDLBD_nowplayong_queue = QtWidgets.QLabel(self.apollo_FR_nowplaying_queue)
        self.apollo_HDLBD_nowplayong_queue.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_HDLBD_nowplayong_queue.setAlignment(QtCore.Qt.AlignCenter)
        self.apollo_HDLBD_nowplayong_queue.setObjectName("apollo_HDLBD_nowplayong_queue")
        self.gridLayout_4.addWidget(self.apollo_HDLBD_nowplayong_queue, 0, 0, 1, 1)
        self.apollo_FR_NPQ_buttons_maintable = QtWidgets.QFrame(self.apollo_FR_nowplaying_queue)
        self.apollo_FR_NPQ_buttons_maintable.setMinimumSize(QtCore.QSize(0, 32))
        self.apollo_FR_NPQ_buttons_maintable.setMaximumSize(QtCore.QSize(16777215, 32))
        self.apollo_FR_NPQ_buttons_maintable.setObjectName("apollo_FR_NPQ_buttons_maintable")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.apollo_FR_NPQ_buttons_maintable)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.apollo_PSB_NPQ_addtrack = QtWidgets.QPushButton(self.apollo_FR_NPQ_buttons_maintable)
        self.apollo_PSB_NPQ_addtrack.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_NPQ_addtrack.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_NPQ_addtrack.setFlat(True)
        self.apollo_PSB_NPQ_addtrack.setObjectName("apollo_PSB_NPQ_addtrack")
        self.horizontalLayout_3.addWidget(self.apollo_PSB_NPQ_addtrack)
        self.apollo_PSB_NPQ_subtrack = QtWidgets.QPushButton(self.apollo_FR_NPQ_buttons_maintable)
        self.apollo_PSB_NPQ_subtrack.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_NPQ_subtrack.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_NPQ_subtrack.setFlat(True)
        self.apollo_PSB_NPQ_subtrack.setObjectName("apollo_PSB_NPQ_subtrack")
        self.horizontalLayout_3.addWidget(self.apollo_PSB_NPQ_subtrack)
        self.apollo_PSB_NPQ_options = QtWidgets.QPushButton(self.apollo_FR_NPQ_buttons_maintable)
        self.apollo_PSB_NPQ_options.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_NPQ_options.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_NPQ_options.setFlat(True)
        self.apollo_PSB_NPQ_options.setObjectName("apollo_PSB_NPQ_options")
        self.horizontalLayout_3.addWidget(self.apollo_PSB_NPQ_options)
        self.apollo_LEDT_NPQ_main_search = QtWidgets.QLineEdit(self.apollo_FR_NPQ_buttons_maintable)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_LEDT_NPQ_main_search.sizePolicy().hasHeightForWidth())
        self.apollo_LEDT_NPQ_main_search.setSizePolicy(sizePolicy)
        self.apollo_LEDT_NPQ_main_search.setMinimumSize(QtCore.QSize(0, 24))
        self.apollo_LEDT_NPQ_main_search.setMaximumSize(QtCore.QSize(16777215, 24))
        self.apollo_LEDT_NPQ_main_search.setObjectName("apollo_LEDT_NPQ_main_search")
        self.horizontalLayout_3.addWidget(self.apollo_LEDT_NPQ_main_search)
        self.apollo_PSB_NPQ_tablesearch = QtWidgets.QPushButton(self.apollo_FR_NPQ_buttons_maintable)
        self.apollo_PSB_NPQ_tablesearch.setMinimumSize(QtCore.QSize(32, 32))
        self.apollo_PSB_NPQ_tablesearch.setMaximumSize(QtCore.QSize(30, 32))
        self.apollo_PSB_NPQ_tablesearch.setFlat(True)
        self.apollo_PSB_NPQ_tablesearch.setObjectName("apollo_PSB_NPQ_tablesearch")
        self.horizontalLayout_3.addWidget(self.apollo_PSB_NPQ_tablesearch)
        self.gridLayout_4.addWidget(self.apollo_FR_NPQ_buttons_maintable, 3, 0, 1, 1)
        self.apollo_FR_footer = QtWidgets.QFrame(self.splitter_2)
        self.apollo_FR_footer.setMinimumSize(QtCore.QSize(0, 55))
        self.apollo_FR_footer.setMaximumSize(QtCore.QSize(16777215, 55))
        self.apollo_FR_footer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_FR_footer.setObjectName("apollo_FR_footer")
        self.gridLayout = QtWidgets.QGridLayout(self.apollo_FR_footer)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(8)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.apollo_PSB_skipback = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_skipback.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_skipback.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_skipback.setFlat(True)
        self.apollo_PSB_skipback.setObjectName("apollo_PSB_skipback")
        self.gridLayout.addWidget(self.apollo_PSB_skipback, 1, 4, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(383, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
        self.apollo_PSB_seekb = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_seekb.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_seekb.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_seekb.setFlat(True)
        self.apollo_PSB_seekb.setObjectName("apollo_PSB_seekb")
        self.gridLayout.addWidget(self.apollo_PSB_seekb, 1, 5, 1, 1)
        self.apollo_PSB_pause = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_pause.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_pause.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_pause.setFlat(True)
        self.apollo_PSB_pause.setObjectName("apollo_PSB_pause")
        self.gridLayout.addWidget(self.apollo_PSB_pause, 1, 2, 1, 1)
        self.apollo_PSB_seekf = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_seekf.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_seekf.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_seekf.setFlat(True)
        self.apollo_PSB_seekf.setObjectName("apollo_PSB_seekf")
        self.gridLayout.addWidget(self.apollo_PSB_seekf, 1, 3, 1, 1)
        self.apollo_PSB_skipfront = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_skipfront.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_skipfront.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_skipfront.setFlat(True)
        self.apollo_PSB_skipfront.setObjectName("apollo_PSB_skipfront")
        self.gridLayout.addWidget(self.apollo_PSB_skipfront, 1, 6, 1, 1)
        self.apollo_PSB_stop = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_stop.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_stop.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_stop.setFlat(True)
        self.apollo_PSB_stop.setObjectName("apollo_PSB_stop")
        self.gridLayout.addWidget(self.apollo_PSB_stop, 1, 7, 1, 1)
        self.apollo_PSB_play = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_play.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_play.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_play.setFlat(True)
        self.apollo_PSB_play.setObjectName("apollo_PSB_play")
        self.gridLayout.addWidget(self.apollo_PSB_play, 1, 8, 1, 1)
        self.apollo_PSB_playstyle = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_playstyle.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_playstyle.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_playstyle.setFlat(True)
        self.apollo_PSB_playstyle.setObjectName("apollo_PSB_playstyle")
        self.gridLayout.addWidget(self.apollo_PSB_playstyle, 1, 12, 1, 1)
        self.apollo_HSLD_position = QtWidgets.QSlider(self.apollo_FR_footer)
        self.apollo_HSLD_position.setOrientation(QtCore.Qt.Horizontal)
        self.apollo_HSLD_position.setObjectName("apollo_HSLD_position")
        self.gridLayout.addWidget(self.apollo_HSLD_position, 0, 1, 1, 12)
        self.apollo_HSLD_volume_main = QtWidgets.QSlider(self.apollo_FR_footer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.apollo_HSLD_volume_main.sizePolicy().hasHeightForWidth())
        self.apollo_HSLD_volume_main.setSizePolicy(sizePolicy)
        self.apollo_HSLD_volume_main.setMinimumSize(QtCore.QSize(84, 15))
        self.apollo_HSLD_volume_main.setOrientation(QtCore.Qt.Horizontal)
        self.apollo_HSLD_volume_main.setObjectName("apollo_HSLD_volume_main")
        self.gridLayout.addWidget(self.apollo_HSLD_volume_main, 1, 11, 1, 1)
        self.apollo_PSB_volume_main = QtWidgets.QPushButton(self.apollo_FR_footer)
        self.apollo_PSB_volume_main.setMinimumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_volume_main.setMaximumSize(QtCore.QSize(40, 40))
        self.apollo_PSB_volume_main.setFlat(True)
        self.apollo_PSB_volume_main.setObjectName("apollo_PSB_volume_main")
        self.gridLayout.addWidget(self.apollo_PSB_volume_main, 1, 10, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(382, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 9, 1, 1)
        self.apollo_PIXLB_albumcover = QtWidgets.QLabel(self.apollo_FR_footer)
        self.apollo_PIXLB_albumcover.setMinimumSize(QtCore.QSize(55, 55))
        self.apollo_PIXLB_albumcover.setMaximumSize(QtCore.QSize(55, 55))
        self.apollo_PIXLB_albumcover.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.apollo_PIXLB_albumcover.setObjectName("apollo_PIXLB_albumcover")
        self.gridLayout.addWidget(self.apollo_PIXLB_albumcover, 0, 0, 2, 1)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.apollo_TABWG_main.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.apollo_TLB_LBT_grouptool.setText(_translate("MainWindow", "..."))
        self.apollo_PSB_LBT_addtrack.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_LBT_subtrack.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_LBT_options.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_LBT_tablesearch.setText(_translate("MainWindow", "OO"))
        self.apollo_TABWG_main.setTabText(self.apollo_TABWG_main.indexOf(self.apollo_WDG_LBT_frame), _translate("MainWindow", "Library"))
        self.apollo_PSB_NPQ_pause.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_seekf.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_skipback.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_seekb.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_skipfront.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_stop.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_volume_main.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_play.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_playstyle.setText(_translate("MainWindow", "OO"))
        self.apollo_PIXLB_NPQ_albumcover.setText(_translate("MainWindow", "TextLabel"))
        self.apollo_TABWG_main.setTabText(self.apollo_TABWG_main.indexOf(self.apollo_WDG_NPQ_frame), _translate("MainWindow", "Now Playing"))
        self.apollo_HDLBD_nowplayong_queue.setText(_translate("MainWindow", "TextLabel"))
        self.apollo_PSB_NPQ_addtrack.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_subtrack.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_options.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_NPQ_tablesearch.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_skipback.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_seekb.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_pause.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_seekf.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_skipfront.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_stop.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_play.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_playstyle.setText(_translate("MainWindow", "OO"))
        self.apollo_PSB_volume_main.setText(_translate("MainWindow", "OO"))
        self.apollo_PIXLB_albumcover.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
