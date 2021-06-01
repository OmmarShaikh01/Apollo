# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow_apolloUIMBDx.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 622)
        self.MW_WDG_centeral_widget = QWidget(MainWindow)
        self.MW_WDG_centeral_widget.setObjectName(u"MW_WDG_centeral_widget")
        self.gridLayout_6 = QGridLayout(self.MW_WDG_centeral_widget)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.MW_VSP_mainsplitter = QSplitter(self.MW_WDG_centeral_widget)
        self.MW_VSP_mainsplitter.setObjectName(u"MW_VSP_mainsplitter")
        self.MW_VSP_mainsplitter.setOrientation(Qt.Vertical)
        self.MW_VSP_mainsplitter.setHandleWidth(1)
        self.MW_HSP_subwindows = QSplitter(self.MW_VSP_mainsplitter)
        self.MW_HSP_subwindows.setObjectName(u"MW_HSP_subwindows")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MW_HSP_subwindows.sizePolicy().hasHeightForWidth())
        self.MW_HSP_subwindows.setSizePolicy(sizePolicy)
        self.MW_HSP_subwindows.setOrientation(Qt.Horizontal)
        self.MW_HSP_subwindows.setHandleWidth(2)
        self.SubW_TABWG_MainTab = QTabWidget(self.MW_HSP_subwindows)
        self.SubW_TABWG_MainTab.setObjectName(u"SubW_TABWG_MainTab")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.SubW_TABWG_MainTab.sizePolicy().hasHeightForWidth())
        self.SubW_TABWG_MainTab.setSizePolicy(sizePolicy1)
        self.SubW_TABWG_MainTab.setMinimumSize(QSize(541, 535))
        self.LBT_WDG_main = QWidget()
        self.LBT_WDG_main.setObjectName(u"LBT_WDG_main")
        self.gridLayout_4 = QGridLayout(self.LBT_WDG_main)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.LBT_HSP_main = QSplitter(self.LBT_WDG_main)
        self.LBT_HSP_main.setObjectName(u"LBT_HSP_main")
        self.LBT_HSP_main.setOrientation(Qt.Horizontal)
        self.LBT_HSP_main.setHandleWidth(2)
        self.LBT_FR_grouping = QFrame(self.LBT_HSP_main)
        self.LBT_FR_grouping.setObjectName(u"LBT_FR_grouping")
        self.LBT_FR_grouping.setFrameShape(QFrame.StyledPanel)
        self.LBT_FR_grouping.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.LBT_FR_grouping)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.LBT_FR_search_group = QFrame(self.LBT_FR_grouping)
        self.LBT_FR_search_group.setObjectName(u"LBT_FR_search_group")
        self.LBT_FR_search_group.setMinimumSize(QSize(0, 24))
        self.LBT_FR_search_group.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout_3 = QHBoxLayout(self.LBT_FR_search_group)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.LBT_LEDT_search_group = QLineEdit(self.LBT_FR_search_group)
        self.LBT_LEDT_search_group.setObjectName(u"LBT_LEDT_search_group")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.LBT_LEDT_search_group.sizePolicy().hasHeightForWidth())
        self.LBT_LEDT_search_group.setSizePolicy(sizePolicy2)
        self.LBT_LEDT_search_group.setMinimumSize(QSize(0, 0))
        self.LBT_LEDT_search_group.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout_3.addWidget(self.LBT_LEDT_search_group)

        self.LBT_TLB_search_group = QToolButton(self.LBT_FR_search_group)
        self.LBT_TLB_search_group.setObjectName(u"LBT_TLB_search_group")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.LBT_TLB_search_group.sizePolicy().hasHeightForWidth())
        self.LBT_TLB_search_group.setSizePolicy(sizePolicy3)
        self.LBT_TLB_search_group.setMinimumSize(QSize(0, 0))
        self.LBT_TLB_search_group.setMaximumSize(QSize(24, 24))
        self.LBT_TLB_search_group.setPopupMode(QToolButton.MenuButtonPopup)
        self.LBT_TLB_search_group.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.horizontalLayout_3.addWidget(self.LBT_TLB_search_group)


        self.gridLayout.addWidget(self.LBT_FR_search_group, 0, 0, 1, 1)

        self.LBT_LSV_grouping = QListView(self.LBT_FR_grouping)
        self.LBT_LSV_grouping.setObjectName(u"LBT_LSV_grouping")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.LBT_LSV_grouping.sizePolicy().hasHeightForWidth())
        self.LBT_LSV_grouping.setSizePolicy(sizePolicy4)
        self.LBT_LSV_grouping.setMinimumSize(QSize(256, 480))
        self.LBT_LSV_grouping.setFrameShape(QFrame.NoFrame)
        self.LBT_LSV_grouping.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.LBT_LSV_grouping.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.LBT_LSV_grouping.setGridSize(QSize(0, 0))
        self.LBT_LSV_grouping.setUniformItemSizes(True)

        self.gridLayout.addWidget(self.LBT_LSV_grouping, 1, 0, 1, 1)

        self.LBT_HSP_main.addWidget(self.LBT_FR_grouping)
        self.LBT_FR_maintable = QFrame(self.LBT_HSP_main)
        self.LBT_FR_maintable.setObjectName(u"LBT_FR_maintable")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.LBT_FR_maintable.sizePolicy().hasHeightForWidth())
        self.LBT_FR_maintable.setSizePolicy(sizePolicy5)
        self.LBT_FR_maintable.setFrameShape(QFrame.StyledPanel)
        self.LBT_FR_maintable.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.LBT_FR_maintable)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.LDT_TBV_maintable = QTableView(self.LBT_FR_maintable)
        self.LDT_TBV_maintable.setObjectName(u"LDT_TBV_maintable")
        self.LDT_TBV_maintable.setMinimumSize(QSize(273, 504))
        self.LDT_TBV_maintable.setFrameShape(QFrame.NoFrame)
        self.LDT_TBV_maintable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.LDT_TBV_maintable.setAlternatingRowColors(False)
        self.LDT_TBV_maintable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.LDT_TBV_maintable.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
        self.LDT_TBV_maintable.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.LDT_TBV_maintable.setShowGrid(False)
        self.LDT_TBV_maintable.setSortingEnabled(True)
        self.LDT_TBV_maintable.setCornerButtonEnabled(False)
        self.LDT_TBV_maintable.horizontalHeader().setStretchLastSection(True)
        self.LDT_TBV_maintable.verticalHeader().setVisible(False)
        self.LDT_TBV_maintable.verticalHeader().setMinimumSectionSize(24)
        self.LDT_TBV_maintable.verticalHeader().setDefaultSectionSize(24)

        self.gridLayout_2.addWidget(self.LDT_TBV_maintable, 0, 0, 1, 1)

        self.LBT_HSP_main.addWidget(self.LBT_FR_maintable)

        self.gridLayout_4.addWidget(self.LBT_HSP_main, 0, 0, 1, 1)

        self.SubW_TABWG_MainTab.addTab(self.LBT_WDG_main, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.SubW_TABWG_MainTab.addTab(self.tab_2, "")
        self.MW_HSP_subwindows.addWidget(self.SubW_TABWG_MainTab)
        self.SubW_FR_queue = QFrame(self.MW_HSP_subwindows)
        self.SubW_FR_queue.setObjectName(u"SubW_FR_queue")
        self.SubW_FR_queue.setFrameShape(QFrame.StyledPanel)
        self.SubW_FR_queue.setFrameShadow(QFrame.Raised)
        self.gridLayout_3 = QGridLayout(self.SubW_FR_queue)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(4)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.NPQ_LSV_mainqueue = QListView(self.SubW_FR_queue)
        self.NPQ_LSV_mainqueue.setObjectName(u"NPQ_LSV_mainqueue")
        sizePolicy4.setHeightForWidth(self.NPQ_LSV_mainqueue.sizePolicy().hasHeightForWidth())
        self.NPQ_LSV_mainqueue.setSizePolicy(sizePolicy4)
        self.NPQ_LSV_mainqueue.setMinimumSize(QSize(255, 485))
        self.NPQ_LSV_mainqueue.setFrameShape(QFrame.NoFrame)
        self.NPQ_LSV_mainqueue.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.NPQ_LSV_mainqueue.setSelectionMode(QAbstractItemView.SingleSelection)
        self.NPQ_LSV_mainqueue.setUniformItemSizes(True)
        self.NPQ_LSV_mainqueue.setSelectionRectVisible(True)

        self.gridLayout_3.addWidget(self.NPQ_LSV_mainqueue, 5, 0, 1, 1)

        self.NPQ_FR_search = QFrame(self.SubW_FR_queue)
        self.NPQ_FR_search.setObjectName(u"NPQ_FR_search")
        self.NPQ_FR_search.setMinimumSize(QSize(0, 24))
        self.NPQ_FR_search.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout = QHBoxLayout(self.NPQ_FR_search)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 2, 2, 2)
        self.NPQ_LEDT_search = QLineEdit(self.NPQ_FR_search)
        self.NPQ_LEDT_search.setObjectName(u"NPQ_LEDT_search")
        sizePolicy2.setHeightForWidth(self.NPQ_LEDT_search.sizePolicy().hasHeightForWidth())
        self.NPQ_LEDT_search.setSizePolicy(sizePolicy2)
        self.NPQ_LEDT_search.setMinimumSize(QSize(0, 0))
        self.NPQ_LEDT_search.setMaximumSize(QSize(16777215, 24))

        self.horizontalLayout.addWidget(self.NPQ_LEDT_search)

        self.NPQ_PSB_search = QPushButton(self.NPQ_FR_search)
        self.NPQ_PSB_search.setObjectName(u"NPQ_PSB_search")
        sizePolicy3.setHeightForWidth(self.NPQ_PSB_search.sizePolicy().hasHeightForWidth())
        self.NPQ_PSB_search.setSizePolicy(sizePolicy3)
        self.NPQ_PSB_search.setMinimumSize(QSize(0, 0))
        self.NPQ_PSB_search.setMaximumSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.NPQ_PSB_search)


        self.gridLayout_3.addWidget(self.NPQ_FR_search, 0, 0, 1, 1)

        self.NPQ_HDLB_queue = QLabel(self.SubW_FR_queue)
        self.NPQ_HDLB_queue.setObjectName(u"NPQ_HDLB_queue")
        self.NPQ_HDLB_queue.setMinimumSize(QSize(0, 24))
        self.NPQ_HDLB_queue.setMaximumSize(QSize(16777215, 24))
        self.NPQ_HDLB_queue.setFrameShape(QFrame.StyledPanel)
        self.NPQ_HDLB_queue.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.NPQ_HDLB_queue, 2, 0, 1, 1)

        self.MW_HSP_subwindows.addWidget(self.SubW_FR_queue)
        self.MW_VSP_mainsplitter.addWidget(self.MW_HSP_subwindows)
        self.MW_FR_mainfooter = QFrame(self.MW_VSP_mainsplitter)
        self.MW_FR_mainfooter.setObjectName(u"MW_FR_mainfooter")
        self.MW_FR_mainfooter.setMinimumSize(QSize(0, 64))
        self.MW_FR_mainfooter.setMaximumSize(QSize(16777215, 64))
        self.MW_FR_mainfooter.setFrameShape(QFrame.StyledPanel)
        self.MW_FR_mainfooter.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.MW_FR_mainfooter)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.footer_FR_seekbar = QFrame(self.MW_FR_mainfooter)
        self.footer_FR_seekbar.setObjectName(u"footer_FR_seekbar")
        self.footer_FR_seekbar.setMinimumSize(QSize(0, 16))
        self.footer_FR_seekbar.setMaximumSize(QSize(16777215, 16))
        self.gridLayout_7 = QGridLayout(self.footer_FR_seekbar)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(4)
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setContentsMargins(4, 0, 4, 0)
        self.footer_LAB_seekbar_right = QLabel(self.footer_FR_seekbar)
        self.footer_LAB_seekbar_right.setObjectName(u"footer_LAB_seekbar_right")

        self.gridLayout_7.addWidget(self.footer_LAB_seekbar_right, 0, 2, 1, 1)

        self.footer_LAB_seekbar_left = QLabel(self.footer_FR_seekbar)
        self.footer_LAB_seekbar_left.setObjectName(u"footer_LAB_seekbar_left")

        self.gridLayout_7.addWidget(self.footer_LAB_seekbar_left, 0, 0, 1, 1)

        self.footer_HSLD_seekbar = QSlider(self.footer_FR_seekbar)
        self.footer_HSLD_seekbar.setObjectName(u"footer_HSLD_seekbar")
        self.footer_HSLD_seekbar.setMinimumSize(QSize(0, 16))
        self.footer_HSLD_seekbar.setOrientation(Qt.Horizontal)

        self.gridLayout_7.addWidget(self.footer_HSLD_seekbar, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.footer_FR_seekbar)

        self.footer_FR_bottom = QFrame(self.MW_FR_mainfooter)
        self.footer_FR_bottom.setObjectName(u"footer_FR_bottom")
        self.footer_FR_bottom.setMinimumSize(QSize(0, 16))
        self.footer_FR_bottom.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.footer_FR_bottom)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.footer_FR_label = QFrame(self.footer_FR_bottom)
        self.footer_FR_label.setObjectName(u"footer_FR_label")
        self.footer_FR_label.setMinimumSize(QSize(236, 0))
        self.footer_FR_label.setFrameShape(QFrame.NoFrame)
        self.gridLayout_11 = QGridLayout(self.footer_FR_label)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setContentsMargins(4, 0, 0, 0)
        self.footer_PIXLB_cover = QLabel(self.footer_FR_label)
        self.footer_PIXLB_cover.setObjectName(u"footer_PIXLB_cover")
        self.footer_PIXLB_cover.setMinimumSize(QSize(40, 40))
        self.footer_PIXLB_cover.setMaximumSize(QSize(40, 40))
        self.footer_PIXLB_cover.setFrameShape(QFrame.StyledPanel)

        self.gridLayout_11.addWidget(self.footer_PIXLB_cover, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_8, 0, 1, 1, 1)


        self.horizontalLayout_2.addWidget(self.footer_FR_label)

        self.footer_FR_playback = QFrame(self.footer_FR_bottom)
        self.footer_FR_playback.setObjectName(u"footer_FR_playback")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.footer_FR_playback.sizePolicy().hasHeightForWidth())
        self.footer_FR_playback.setSizePolicy(sizePolicy6)
        self.footer_FR_playback.setFrameShape(QFrame.NoFrame)
        self.gridLayout_5 = QGridLayout(self.footer_FR_playback)
        self.gridLayout_5.setSpacing(4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.footer_PSB_seekb = QPushButton(self.footer_FR_playback)
        self.footer_PSB_seekb.setObjectName(u"footer_PSB_seekb")
        self.footer_PSB_seekb.setMinimumSize(QSize(32, 32))
        self.footer_PSB_seekb.setMaximumSize(QSize(32, 32))
        self.footer_PSB_seekb.setSizeIncrement(QSize(0, 0))

        self.gridLayout_5.addWidget(self.footer_PSB_seekb, 0, 2, 1, 1)

        self.footer_PSB_prev = QPushButton(self.footer_FR_playback)
        self.footer_PSB_prev.setObjectName(u"footer_PSB_prev")
        self.footer_PSB_prev.setMinimumSize(QSize(32, 32))
        self.footer_PSB_prev.setMaximumSize(QSize(32, 32))
        self.footer_PSB_prev.setSizeIncrement(QSize(0, 0))

        self.gridLayout_5.addWidget(self.footer_PSB_prev, 0, 1, 1, 1)

        self.footer_PSB_next = QPushButton(self.footer_FR_playback)
        self.footer_PSB_next.setObjectName(u"footer_PSB_next")
        self.footer_PSB_next.setMinimumSize(QSize(32, 32))
        self.footer_PSB_next.setMaximumSize(QSize(32, 32))
        self.footer_PSB_next.setSizeIncrement(QSize(0, 0))

        self.gridLayout_5.addWidget(self.footer_PSB_next, 0, 7, 1, 1)

        self.footer_PSB_stop = QPushButton(self.footer_FR_playback)
        self.footer_PSB_stop.setObjectName(u"footer_PSB_stop")
        self.footer_PSB_stop.setMinimumSize(QSize(32, 32))
        self.footer_PSB_stop.setMaximumSize(QSize(32, 32))
        self.footer_PSB_stop.setSizeIncrement(QSize(0, 0))

        self.gridLayout_5.addWidget(self.footer_PSB_stop, 0, 3, 1, 1)

        self.footer_PSB_play = QPushButton(self.footer_FR_playback)
        self.footer_PSB_play.setObjectName(u"footer_PSB_play")
        self.footer_PSB_play.setMinimumSize(QSize(40, 40))
        self.footer_PSB_play.setMaximumSize(QSize(40, 40))
        self.footer_PSB_play.setSizeIncrement(QSize(0, 0))

        self.gridLayout_5.addWidget(self.footer_PSB_play, 0, 4, 1, 1)

        self.footer_PSB_pause = QPushButton(self.footer_FR_playback)
        self.footer_PSB_pause.setObjectName(u"footer_PSB_pause")
        self.footer_PSB_pause.setMinimumSize(QSize(32, 32))
        self.footer_PSB_pause.setMaximumSize(QSize(32, 32))
        self.footer_PSB_pause.setSizeIncrement(QSize(0, 0))

        self.gridLayout_5.addWidget(self.footer_PSB_pause, 0, 5, 1, 1)

        self.footer_PSB_seekf = QPushButton(self.footer_FR_playback)
        self.footer_PSB_seekf.setObjectName(u"footer_PSB_seekf")
        self.footer_PSB_seekf.setMinimumSize(QSize(32, 32))
        self.footer_PSB_seekf.setMaximumSize(QSize(32, 32))
        self.footer_PSB_seekf.setSizeIncrement(QSize(0, 0))

        self.gridLayout_5.addWidget(self.footer_PSB_seekf, 0, 6, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_6, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_7, 0, 8, 1, 1)


        self.horizontalLayout_2.addWidget(self.footer_FR_playback)

        self.footer_FR_volume = QFrame(self.footer_FR_bottom)
        self.footer_FR_volume.setObjectName(u"footer_FR_volume")
        self.footer_FR_volume.setFrameShape(QFrame.NoFrame)
        self.gridLayout_10 = QGridLayout(self.footer_FR_volume)
        self.gridLayout_10.setSpacing(4)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(4, 4, 4, 4)
        self.footer_PSB_repeat = QPushButton(self.footer_FR_volume)
        self.footer_PSB_repeat.setObjectName(u"footer_PSB_repeat")
        self.footer_PSB_repeat.setMinimumSize(QSize(32, 32))
        self.footer_PSB_repeat.setMaximumSize(QSize(32, 32))
        self.footer_PSB_repeat.setSizeIncrement(QSize(0, 0))

        self.gridLayout_10.addWidget(self.footer_PSB_repeat, 0, 5, 1, 1)

        self.footer_PSB_volume = QPushButton(self.footer_FR_volume)
        self.footer_PSB_volume.setObjectName(u"footer_PSB_volume")
        self.footer_PSB_volume.setMinimumSize(QSize(32, 32))
        self.footer_PSB_volume.setMaximumSize(QSize(32, 32))
        self.footer_PSB_volume.setSizeIncrement(QSize(0, 0))

        self.gridLayout_10.addWidget(self.footer_PSB_volume, 0, 1, 1, 1)

        self.pushButton_20 = QPushButton(self.footer_FR_volume)
        self.pushButton_20.setObjectName(u"pushButton_20")
        self.pushButton_20.setMinimumSize(QSize(32, 32))
        self.pushButton_20.setMaximumSize(QSize(32, 32))
        self.pushButton_20.setSizeIncrement(QSize(0, 0))

        self.gridLayout_10.addWidget(self.pushButton_20, 0, 6, 1, 1)

        self.footer_PSB_audio_control = QPushButton(self.footer_FR_volume)
        self.footer_PSB_audio_control.setObjectName(u"footer_PSB_audio_control")
        self.footer_PSB_audio_control.setMinimumSize(QSize(32, 32))
        self.footer_PSB_audio_control.setMaximumSize(QSize(32, 32))
        self.footer_PSB_audio_control.setSizeIncrement(QSize(0, 0))

        self.gridLayout_10.addWidget(self.footer_PSB_audio_control, 0, 4, 1, 1)

        self.footer_HSLD_volume = QSlider(self.footer_FR_volume)
        self.footer_HSLD_volume.setObjectName(u"footer_HSLD_volume")
        self.footer_HSLD_volume.setMinimumSize(QSize(0, 24))
        self.footer_HSLD_volume.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.footer_HSLD_volume, 0, 3, 1, 1)


        self.horizontalLayout_2.addWidget(self.footer_FR_volume)


        self.verticalLayout.addWidget(self.footer_FR_bottom)

        self.MW_VSP_mainsplitter.addWidget(self.MW_FR_mainfooter)

        self.gridLayout_6.addWidget(self.MW_VSP_mainsplitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.MW_WDG_centeral_widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.SubW_TABWG_MainTab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LBT_TLB_search_group.setText("")
        self.SubW_TABWG_MainTab.setTabText(self.SubW_TABWG_MainTab.indexOf(self.LBT_WDG_main), QCoreApplication.translate("MainWindow", u"Library", None))
        self.SubW_TABWG_MainTab.setTabText(self.SubW_TABWG_MainTab.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.NPQ_PSB_search.setText("")
        self.NPQ_HDLB_queue.setText(QCoreApplication.translate("MainWindow", u"Now Playing", None))
        self.footer_LAB_seekbar_right.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.footer_LAB_seekbar_left.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.footer_PIXLB_cover.setText("")
        self.footer_PSB_seekb.setText("")
        self.footer_PSB_prev.setText("")
        self.footer_PSB_next.setText("")
        self.footer_PSB_stop.setText("")
        self.footer_PSB_play.setText("")
        self.footer_PSB_pause.setText("")
        self.footer_PSB_seekf.setText("")
        self.footer_PSB_repeat.setText("")
        self.footer_PSB_volume.setText("")
        self.pushButton_20.setText("")
        self.footer_PSB_audio_control.setText("")
    # retranslateUi

