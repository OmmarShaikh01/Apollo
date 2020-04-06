# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\preferences.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_preferences_window(object):
    def setupUi(self, preferences_window):
        preferences_window.setObjectName("preferences_window")
        preferences_window.setWindowModality(QtCore.Qt.ApplicationModal)
        preferences_window.setEnabled(True)
        preferences_window.resize(700, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(preferences_window.sizePolicy().hasHeightForWidth())
        preferences_window.setSizePolicy(sizePolicy)
        preferences_window.setMinimumSize(QtCore.QSize(700, 700))
        preferences_window.setMaximumSize(QtCore.QSize(700, 700))
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        preferences_window.setFont(font)
        preferences_window.setAutoFillBackground(False)
        preferences_window.setStyleSheet("background-color: #24292E ;\n"
        "font-family: Arial, Helvetica, sans-serif;\n"
        "font-size: 14px;\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "font-weight: normal;\n"
        "text-decoration: none;\n"
        "font-style: normal;\n"
        "font-variant: normal;\n"
        "text-transform: none;\n"
        "pressed:{\n"
        "    background-color: rgb(224, 0, 0);\n"
        "    border-style: inset;\n"
        "}")
        preferences_window.setDocumentMode(True)
        self.main_widget = QtWidgets.QWidget(preferences_window)
        self.main_widget.setMouseTracking(True)
        self.main_widget.setAutoFillBackground(False)
        self.main_widget.setStyleSheet("")
        self.main_widget.setObjectName("main_widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout_2.setContentsMargins(4, 0, 4, 4)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.main_frame = QtWidgets.QFrame(self.main_widget)
        self.main_frame.setMouseTracking(True)
        self.main_frame.setObjectName("main_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.main_frame)
        self.gridLayout.setContentsMargins(6, 1, 6, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.main_grid_2 = QtWidgets.QFrame(self.main_frame)
        self.main_grid_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_grid_2.setObjectName("main_grid_2")
        self.main_grid = QtWidgets.QGridLayout(self.main_grid_2)
        self.main_grid.setContentsMargins(0, 0, 0, 0)
        self.main_grid.setSpacing(0)
        self.main_grid.setObjectName("main_grid")
        self.horizontalFrame = QtWidgets.QFrame(self.main_grid_2)
        self.horizontalFrame.setStyleSheet("background-color: #24292E;")
        self.horizontalFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.apply_button = QtWidgets.QPushButton(self.horizontalFrame)
        self.apply_button.setAutoFillBackground(False)
        self.apply_button.setStyleSheet("QPushButton {\n"
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
        self.apply_button.setFlat(True)
        self.apply_button.setObjectName("apply_button")
        self.horizontalLayout.addWidget(self.apply_button)
        self.save_button = QtWidgets.QPushButton(self.horizontalFrame)
        self.save_button.setAutoFillBackground(False)
        self.save_button.setStyleSheet("QPushButton {\n"
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
        self.save_button.setFlat(True)
        self.save_button.setObjectName("save_button")
        self.horizontalLayout.addWidget(self.save_button)
        self.close_button = QtWidgets.QPushButton(self.horizontalFrame)
        self.close_button.setAutoFillBackground(False)
        self.close_button.setStyleSheet("QPushButton {\n"
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
        self.close_button.setFlat(True)
        self.close_button.setObjectName("close_button")
        self.horizontalLayout.addWidget(self.close_button)
        self.main_grid.addWidget(self.horizontalFrame, 1, 0, 1, 3)
        self.verticalFrame = QtWidgets.QFrame(self.main_grid_2)
        self.verticalFrame.setMinimumSize(QtCore.QSize(170, 0))
        self.verticalFrame.setMaximumSize(QtCore.QSize(170, 16777215))
        self.verticalFrame.setStyleSheet("background-color: rgb(47, 54, 67);")
        self.verticalFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.verticalFrame.setObjectName("verticalFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.general_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.general_btn.setFont(font)
        self.general_btn.setAutoFillBackground(False)
        self.general_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.general_btn.setCheckable(False)
        self.general_btn.setAutoRepeat(False)
        self.general_btn.setAutoExclusive(True)
        self.general_btn.setAutoRepeatDelay(300)
        self.general_btn.setAutoRepeatInterval(100)
        self.general_btn.setFlat(False)
        self.general_btn.setObjectName("general_btn")
        self.verticalLayout.addWidget(self.general_btn)
        self.now_playing_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.now_playing_btn.setFont(font)
        self.now_playing_btn.setAutoFillBackground(False)
        self.now_playing_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.now_playing_btn.setCheckable(False)
        self.now_playing_btn.setAutoRepeat(False)
        self.now_playing_btn.setAutoExclusive(True)
        self.now_playing_btn.setAutoRepeatDelay(300)
        self.now_playing_btn.setAutoRepeatInterval(0)
        self.now_playing_btn.setFlat(False)
        self.now_playing_btn.setObjectName("now_playing_btn")
        self.verticalLayout.addWidget(self.now_playing_btn)
        self.layout_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.layout_btn.setFont(font)
        self.layout_btn.setAutoFillBackground(False)
        self.layout_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.layout_btn.setCheckable(False)
        self.layout_btn.setAutoRepeat(True)
        self.layout_btn.setAutoExclusive(True)
        self.layout_btn.setAutoRepeatDelay(300)
        self.layout_btn.setAutoRepeatInterval(0)
        self.layout_btn.setFlat(False)
        self.layout_btn.setObjectName("layout_btn")
        self.verticalLayout.addWidget(self.layout_btn)
        self.library_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.library_btn.setFont(font)
        self.library_btn.setAutoFillBackground(False)
        self.library_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.library_btn.setCheckable(False)
        self.library_btn.setAutoRepeat(False)
        self.library_btn.setAutoExclusive(True)
        self.library_btn.setAutoRepeatDelay(300)
        self.library_btn.setAutoRepeatInterval(0)
        self.library_btn.setFlat(False)
        self.library_btn.setObjectName("library_btn")
        self.verticalLayout.addWidget(self.library_btn)
        self.tags_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.tags_btn.setFont(font)
        self.tags_btn.setAutoFillBackground(False)
        self.tags_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.tags_btn.setCheckable(False)
        self.tags_btn.setAutoRepeat(False)
        self.tags_btn.setAutoExclusive(True)
        self.tags_btn.setAutoRepeatDelay(300)
        self.tags_btn.setAutoRepeatInterval(0)
        self.tags_btn.setFlat(False)
        self.tags_btn.setObjectName("tags_btn")
        self.verticalLayout.addWidget(self.tags_btn)
        self.players_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.players_btn.setFont(font)
        self.players_btn.setAutoFillBackground(False)
        self.players_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.players_btn.setCheckable(False)
        self.players_btn.setAutoRepeat(False)
        self.players_btn.setAutoExclusive(True)
        self.players_btn.setAutoRepeatDelay(300)
        self.players_btn.setAutoRepeatInterval(0)
        self.players_btn.setFlat(False)
        self.players_btn.setObjectName("players_btn")
        self.verticalLayout.addWidget(self.players_btn)
        self.hotkeys_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.hotkeys_btn.setFont(font)
        self.hotkeys_btn.setAutoFillBackground(False)
        self.hotkeys_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.hotkeys_btn.setCheckable(False)
        self.hotkeys_btn.setAutoRepeat(False)
        self.hotkeys_btn.setAutoExclusive(True)
        self.hotkeys_btn.setAutoRepeatDelay(300)
        self.hotkeys_btn.setAutoRepeatInterval(0)
        self.hotkeys_btn.setFlat(False)
        self.hotkeys_btn.setObjectName("hotkeys_btn")
        self.verticalLayout.addWidget(self.hotkeys_btn)
        self.sort_gp_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.sort_gp_btn.setFont(font)
        self.sort_gp_btn.setAutoFillBackground(False)
        self.sort_gp_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.sort_gp_btn.setCheckable(False)
        self.sort_gp_btn.setAutoRepeat(False)
        self.sort_gp_btn.setAutoExclusive(True)
        self.sort_gp_btn.setAutoRepeatDelay(300)
        self.sort_gp_btn.setAutoRepeatInterval(100)
        self.sort_gp_btn.setFlat(False)
        self.sort_gp_btn.setObjectName("sort_gp_btn")
        self.verticalLayout.addWidget(self.sort_gp_btn)
        self.file_con_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.file_con_btn.setFont(font)
        self.file_con_btn.setAutoFillBackground(False)
        self.file_con_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.file_con_btn.setCheckable(False)
        self.file_con_btn.setAutoRepeat(False)
        self.file_con_btn.setAutoExclusive(True)
        self.file_con_btn.setAutoRepeatDelay(300)
        self.file_con_btn.setAutoRepeatInterval(0)
        self.file_con_btn.setFlat(False)
        self.file_con_btn.setObjectName("file_con_btn")
        self.verticalLayout.addWidget(self.file_con_btn)
        self.tools_btn = QtWidgets.QPushButton(self.verticalFrame)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.tools_btn.setFont(font)
        self.tools_btn.setAutoFillBackground(False)
        self.tools_btn.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 6em;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.tools_btn.setCheckable(False)
        self.tools_btn.setAutoRepeat(False)
        self.tools_btn.setAutoExclusive(True)
        self.tools_btn.setAutoRepeatDelay(300)
        self.tools_btn.setAutoRepeatInterval(100)
        self.tools_btn.setFlat(False)
        self.tools_btn.setObjectName("tools_btn")
        self.verticalLayout.addWidget(self.tools_btn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.main_grid.addWidget(self.verticalFrame, 0, 0, 1, 1)
        self.all_tabs_stacked = QtWidgets.QStackedWidget(self.main_grid_2)
        self.all_tabs_stacked.setEnabled(True)
        self.all_tabs_stacked.setStyleSheet(" QScrollBar:vertical {\n"
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
        " }")
        self.all_tabs_stacked.setObjectName("all_tabs_stacked")
        self.general_tab = QtWidgets.QWidget()
        self.general_tab.setObjectName("general_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.general_tab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.misc_box = QtWidgets.QGroupBox(self.general_tab)
        self.misc_box.setMinimumSize(QtCore.QSize(0, 200))
        self.misc_box.setMaximumSize(QtCore.QSize(16777215, 280))
        self.misc_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.misc_box.setFlat(True)
        self.misc_box.setCheckable(False)
        self.misc_box.setObjectName("misc_box")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.misc_box)
        self.gridLayout_10.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.verticalFrame_2 = QtWidgets.QFrame(self.misc_box)
        self.verticalFrame_2.setObjectName("verticalFrame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalFrame_2)
        self.verticalLayout_3.setContentsMargins(0, 6, 0, 0)
        self.verticalLayout_3.setSpacing(4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.checkBox_10 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_10.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_10.setObjectName("checkBox_10")
        self.verticalLayout_3.addWidget(self.checkBox_10)
        self.checkBox_11 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_11.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_11.setObjectName("checkBox_11")
        self.verticalLayout_3.addWidget(self.checkBox_11)
        self.checkBox_71 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_71.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_71.setObjectName("checkBox_71")
        self.verticalLayout_3.addWidget(self.checkBox_71)
        self.checkBox_12 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_12.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_12.setObjectName("checkBox_12")
        self.verticalLayout_3.addWidget(self.checkBox_12)
        self.checkBox_72 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_72.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_72.setObjectName("checkBox_72")
        self.verticalLayout_3.addWidget(self.checkBox_72)
        self.checkBox_73 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_73.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_73.setObjectName("checkBox_73")
        self.verticalLayout_3.addWidget(self.checkBox_73)
        self.checkBox_74 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_74.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_74.setObjectName("checkBox_74")
        self.verticalLayout_3.addWidget(self.checkBox_74)
        self.checkBox_13 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_13.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_13.setObjectName("checkBox_13")
        self.verticalLayout_3.addWidget(self.checkBox_13)
        self.checkBox_75 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_75.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_75.setObjectName("checkBox_75")
        self.verticalLayout_3.addWidget(self.checkBox_75)
        self.checkBox_76 = QtWidgets.QCheckBox(self.verticalFrame_2)
        self.checkBox_76.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_76.setObjectName("checkBox_76")
        self.verticalLayout_3.addWidget(self.checkBox_76)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.gridLayout_10.addWidget(self.verticalFrame_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.misc_box, 3, 0, 1, 1)
        self.application_box = QtWidgets.QGroupBox(self.general_tab)
        self.application_box.setMaximumSize(QtCore.QSize(16777215, 150))
        self.application_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.application_box.setFlat(True)
        self.application_box.setCheckable(False)
        self.application_box.setObjectName("application_box")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.application_box)
        self.gridLayout_9.setContentsMargins(10, 6, 0, 0)
        self.gridLayout_9.setHorizontalSpacing(0)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.application_box)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBox_startup_mode = QtWidgets.QComboBox(self.application_box)
        self.comboBox_startup_mode.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_startup_mode.setObjectName("comboBox_startup_mode")
        self.comboBox_startup_mode.addItem("")
        self.comboBox_startup_mode.addItem("")
        self.comboBox_startup_mode.addItem("")
        self.comboBox_startup_mode.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox_startup_mode)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.checkBoxsplash_screen = QtWidgets.QCheckBox(self.application_box)
        self.checkBoxsplash_screen.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBoxsplash_screen.setTristate(False)
        self.checkBoxsplash_screen.setObjectName("checkBoxsplash_screen")
        self.verticalLayout_2.addWidget(self.checkBoxsplash_screen)
        self.checkBox_min_totask = QtWidgets.QCheckBox(self.application_box)
        self.checkBox_min_totask.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_min_totask.setObjectName("checkBox_min_totask")
        self.verticalLayout_2.addWidget(self.checkBox_min_totask)
        self.checkBox_play_str = QtWidgets.QCheckBox(self.application_box)
        self.checkBox_play_str.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_play_str.setObjectName("checkBox_play_str")
        self.verticalLayout_2.addWidget(self.checkBox_play_str)
        self.checkBox_chkOnsstr = QtWidgets.QCheckBox(self.application_box)
        self.checkBox_chkOnsstr.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_chkOnsstr.setObjectName("checkBox_chkOnsstr")
        self.verticalLayout_2.addWidget(self.checkBox_chkOnsstr)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.gridLayout_9.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.application_box, 1, 0, 1, 1)
        self.file_types_box = QtWidgets.QGroupBox(self.general_tab)
        self.file_types_box.setMaximumSize(QtCore.QSize(16777215, 280))
        self.file_types_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.file_types_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.file_types_box.setFlat(True)
        self.file_types_box.setCheckable(False)
        self.file_types_box.setObjectName("file_types_box")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.file_types_box)
        self.gridLayout_8.setContentsMargins(10, 6, 0, 0)
        self.gridLayout_8.setSpacing(0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_44 = QtWidgets.QGridLayout()
        self.gridLayout_44.setObjectName("gridLayout_44")
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_44.addItem(spacerItem4, 1, 0, 1, 1)
        self.listView_num_each_fl_type = QtWidgets.QListView(self.file_types_box)
        self.listView_num_each_fl_type.setObjectName("listView_num_each_fl_type")
        self.gridLayout_44.addWidget(self.listView_num_each_fl_type, 0, 1, 1, 1)
        self.verticalFrame_3 = QtWidgets.QFrame(self.file_types_box)
        self.verticalFrame_3.setMaximumSize(QtCore.QSize(16777215, 170))
        self.verticalFrame_3.setObjectName("verticalFrame_3")
        self.gridLayout_45 = QtWidgets.QGridLayout(self.verticalFrame_3)
        self.gridLayout_45.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_45.setHorizontalSpacing(0)
        self.gridLayout_45.setVerticalSpacing(2)
        self.gridLayout_45.setObjectName("gridLayout_45")
        self.checkBox_wav = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_wav.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_wav.setObjectName("checkBox_wav")
        self.gridLayout_45.addWidget(self.checkBox_wav, 7, 0, 1, 1)
        self.checkBox_aiff = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_aiff.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_aiff.setObjectName("checkBox_aiff")
        self.gridLayout_45.addWidget(self.checkBox_aiff, 1, 0, 1, 1)
        self.checkBox_ogg = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_ogg.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_ogg.setObjectName("checkBox_ogg")
        self.gridLayout_45.addWidget(self.checkBox_ogg, 5, 0, 1, 1)
        self.checkBox_mp3 = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_mp3.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_mp3.setObjectName("checkBox_mp3")
        self.gridLayout_45.addWidget(self.checkBox_mp3, 4, 0, 1, 1)
        self.checkBox_alac = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_alac.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_alac.setObjectName("checkBox_alac")
        self.gridLayout_45.addWidget(self.checkBox_alac, 2, 0, 1, 1)
        self.checkBox_acc = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_acc.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_acc.setObjectName("checkBox_acc")
        self.gridLayout_45.addWidget(self.checkBox_acc, 0, 0, 1, 1)
        self.checkBox_wma = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_wma.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_wma.setObjectName("checkBox_wma")
        self.gridLayout_45.addWidget(self.checkBox_wma, 6, 0, 1, 1)
        self.checkBox_flac = QtWidgets.QCheckBox(self.verticalFrame_3)
        self.checkBox_flac.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_flac.setObjectName("checkBox_flac")
        self.gridLayout_45.addWidget(self.checkBox_flac, 3, 0, 1, 1)
        self.gridLayout_44.addWidget(self.verticalFrame_3, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.apply_button_3 = QtWidgets.QPushButton(self.file_types_box)
        self.apply_button_3.setAutoFillBackground(False)
        self.apply_button_3.setStyleSheet("QPushButton {\n"
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
        self.apply_button_3.setFlat(True)
        self.apply_button_3.setObjectName("apply_button_3")
        self.horizontalLayout_3.addWidget(self.apply_button_3)
        self.apply_button_2 = QtWidgets.QPushButton(self.file_types_box)
        self.apply_button_2.setAutoFillBackground(False)
        self.apply_button_2.setStyleSheet("QPushButton {\n"
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
        self.apply_button_2.setFlat(True)
        self.apply_button_2.setObjectName("apply_button_2")
        self.horizontalLayout_3.addWidget(self.apply_button_2)
        self.gridLayout_44.addLayout(self.horizontalLayout_3, 1, 1, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_44, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.file_types_box, 2, 0, 1, 1)
        self.all_tabs_stacked.addWidget(self.general_tab)
        self.now_playing_tab = QtWidgets.QWidget()
        self.now_playing_tab.setObjectName("now_playing_tab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.now_playing_tab)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.playing_track_Box = QtWidgets.QGroupBox(self.now_playing_tab)
        self.playing_track_Box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.playing_track_Box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.playing_track_Box.setFlat(True)
        self.playing_track_Box.setCheckable(False)
        self.playing_track_Box.setObjectName("playing_track_Box")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.playing_track_Box)
        self.gridLayout_11.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_11.setSpacing(0)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout_22 = QtWidgets.QGridLayout()
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.label_7 = QtWidgets.QLabel(self.playing_track_Box)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_18.addWidget(self.label_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.playing_track_Box)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        self.comboBox_13 = QtWidgets.QComboBox(self.playing_track_Box)
        self.comboBox_13.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.horizontalLayout_6.addWidget(self.comboBox_13)
        self.verticalLayout_18.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_9 = QtWidgets.QLabel(self.playing_track_Box)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_7.addWidget(self.label_9)
        self.comboBox_12 = QtWidgets.QComboBox(self.playing_track_Box)
        self.comboBox_12.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox_12)
        self.verticalLayout_18.addLayout(self.horizontalLayout_7)
        self.label_10 = QtWidgets.QLabel(self.playing_track_Box)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_18.addWidget(self.label_10)
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.radioButton_16 = QtWidgets.QRadioButton(self.playing_track_Box)
        self.radioButton_16.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_16.setObjectName("radioButton_16")
        self.verticalLayout_19.addWidget(self.radioButton_16)
        self.radioButton_17 = QtWidgets.QRadioButton(self.playing_track_Box)
        self.radioButton_17.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_17.setObjectName("radioButton_17")
        self.verticalLayout_19.addWidget(self.radioButton_17)
        self.radioButton_18 = QtWidgets.QRadioButton(self.playing_track_Box)
        self.radioButton_18.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_18.setChecked(True)
        self.radioButton_18.setObjectName("radioButton_18")
        self.verticalLayout_19.addWidget(self.radioButton_18)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_19.addItem(spacerItem5)
        self.verticalLayout_18.addLayout(self.verticalLayout_19)
        self.gridLayout_22.addLayout(self.verticalLayout_18, 0, 0, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_22, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.playing_track_Box, 0, 0, 1, 1)
        self.shuffle_box = QtWidgets.QGroupBox(self.now_playing_tab)
        self.shuffle_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.shuffle_box.setFlat(True)
        self.shuffle_box.setCheckable(False)
        self.shuffle_box.setObjectName("shuffle_box")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.shuffle_box)
        self.gridLayout_21.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_21.setSpacing(0)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.radioButton = QtWidgets.QRadioButton(self.shuffle_box)
        self.radioButton.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout_4.addWidget(self.radioButton)
        self.radioButton_4 = QtWidgets.QRadioButton(self.shuffle_box)
        self.radioButton_4.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_4.setObjectName("radioButton_4")
        self.verticalLayout_4.addWidget(self.radioButton_4)
        self.radioButton_3 = QtWidgets.QRadioButton(self.shuffle_box)
        self.radioButton_3.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout_4.addWidget(self.radioButton_3)
        self.radioButton_5 = QtWidgets.QRadioButton(self.shuffle_box)
        self.radioButton_5.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_5.setObjectName("radioButton_5")
        self.verticalLayout_4.addWidget(self.radioButton_5)
        self.radioButton_2 = QtWidgets.QRadioButton(self.shuffle_box)
        self.radioButton_2.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout_4.addWidget(self.radioButton_2)
        self.gridLayout_21.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.shuffle_box, 1, 0, 1, 1)
        self.playback_box = QtWidgets.QGroupBox(self.now_playing_tab)
        self.playback_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.playback_box.setFlat(True)
        self.playback_box.setCheckable(False)
        self.playback_box.setObjectName("playback_box")
        self.gridLayout_20 = QtWidgets.QGridLayout(self.playback_box)
        self.gridLayout_20.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_20.setSpacing(0)
        self.gridLayout_20.setObjectName("gridLayout_20")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.playback_box)
        self.scrollArea_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 500, 249))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_4)
        self.gridLayout_12.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_12.setSpacing(0)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.checkBox_14 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_14.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_14.setObjectName("checkBox_14")
        self.horizontalLayout_12.addWidget(self.checkBox_14)
        self.comboBox_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_4)
        self.comboBox_2.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_12.addWidget(self.comboBox_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.checkBox_15 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_15.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_15.setObjectName("checkBox_15")
        self.horizontalLayout_13.addWidget(self.checkBox_15)
        self.label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_13.addWidget(self.label_3)
        self.pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 4px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_13.addWidget(self.pushButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.checkBox_16 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_16.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_16.setObjectName("checkBox_16")
        self.horizontalLayout_14.addWidget(self.checkBox_16)
        self.label_4 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_14.addWidget(self.label_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.pushButton_2.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_2.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 4px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_14.addWidget(self.pushButton_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.checkBox_17 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_17.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_17.setObjectName("checkBox_17")
        self.horizontalLayout_15.addWidget(self.checkBox_17)
        self.verticalLayout_5.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.checkBox_18 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_18.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_18.setObjectName("checkBox_18")
        self.horizontalLayout_16.addWidget(self.checkBox_18)
        self.verticalLayout_5.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.checkBox_19 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_19.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_19.setObjectName("checkBox_19")
        self.horizontalLayout_17.addWidget(self.checkBox_19)
        self.verticalLayout_5.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.checkBox_20 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_20.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_20.setObjectName("checkBox_20")
        self.horizontalLayout_18.addWidget(self.checkBox_20)
        self.verticalLayout_5.addLayout(self.horizontalLayout_18)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.checkBox_21 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents_4)
        self.checkBox_21.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_21.setText("")
        self.checkBox_21.setObjectName("checkBox_21")
        self.horizontalLayout_19.addWidget(self.checkBox_21)
        self.verticalLayout_5.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_12 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_20.addWidget(self.label_12)
        self.lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_20.addWidget(self.lineEdit)
        self.label_13 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_20.addWidget(self.label_13)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_20.addWidget(self.lineEdit_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_14 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_21.addWidget(self.label_14)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_21.addWidget(self.lineEdit_3)
        self.label_15 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_21.addWidget(self.label_15)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_21.addWidget(self.lineEdit_4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_21)
        self.gridLayout_12.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_4)
        self.gridLayout_20.addWidget(self.scrollArea_4, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.playback_box, 2, 0, 1, 1)
        self.all_tabs_stacked.addWidget(self.now_playing_tab)
        self.layout_tab = QtWidgets.QWidget()
        self.layout_tab.setObjectName("layout_tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layout_tab)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.all_tabs_stacked.addWidget(self.layout_tab)
        self.library_tab = QtWidgets.QWidget()
        self.library_tab.setObjectName("library_tab")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.library_tab)
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_13.setSpacing(0)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.musi_library_box = QtWidgets.QGroupBox(self.library_tab)
        self.musi_library_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.musi_library_box.setFlat(True)
        self.musi_library_box.setCheckable(False)
        self.musi_library_box.setObjectName("musi_library_box")
        self.gridLayout_24 = QtWidgets.QGridLayout(self.musi_library_box)
        self.gridLayout_24.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_24.setSpacing(0)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.gridLayout_23 = QtWidgets.QGridLayout()
        self.gridLayout_23.setHorizontalSpacing(0)
        self.gridLayout_23.setVerticalSpacing(4)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.checkBox_22 = QtWidgets.QCheckBox(self.musi_library_box)
        self.checkBox_22.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_22.setObjectName("checkBox_22")
        self.gridLayout_23.addWidget(self.checkBox_22, 2, 0, 1, 1)
        self.checkBox_23 = QtWidgets.QCheckBox(self.musi_library_box)
        self.checkBox_23.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_23.setObjectName("checkBox_23")
        self.gridLayout_23.addWidget(self.checkBox_23, 0, 0, 1, 1)
        self.checkBox_24 = QtWidgets.QCheckBox(self.musi_library_box)
        self.checkBox_24.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_24.setObjectName("checkBox_24")
        self.gridLayout_23.addWidget(self.checkBox_24, 1, 0, 1, 1)
        self.pushButton1 = QtWidgets.QPushButton(self.musi_library_box)
        self.pushButton1.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 4em;\n"
        "padding: 4px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton1.setObjectName("pushButton1")
        self.gridLayout_23.addWidget(self.pushButton1, 0, 1, 1, 1)
        self.checkBox_25 = QtWidgets.QCheckBox(self.musi_library_box)
        self.checkBox_25.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_25.setObjectName("checkBox_25")
        self.gridLayout_23.addWidget(self.checkBox_25, 3, 0, 1, 1)
        self.gridLayout_24.addLayout(self.gridLayout_23, 0, 0, 1, 1)
        self.gridLayout_13.addWidget(self.musi_library_box, 0, 0, 1, 1)
        self.mon_files_box = QtWidgets.QGroupBox(self.library_tab)
        self.mon_files_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.mon_files_box.setFlat(True)
        self.mon_files_box.setCheckable(False)
        self.mon_files_box.setObjectName("mon_files_box")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.mon_files_box)
        self.verticalLayout_8.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.checkBox_26 = QtWidgets.QCheckBox(self.mon_files_box)
        self.checkBox_26.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_26.setObjectName("checkBox_26")
        self.horizontalLayout_22.addWidget(self.checkBox_26)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.mon_files_box)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_22.addWidget(self.lineEdit_5)
        self.verticalLayout_6.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.checkBox_27 = QtWidgets.QCheckBox(self.mon_files_box)
        self.checkBox_27.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_27.setObjectName("checkBox_27")
        self.horizontalLayout_23.addWidget(self.checkBox_27)
        self.pushButton_21 = QtWidgets.QPushButton(self.mon_files_box)
        self.pushButton_21.setStyleSheet("QPushButton {\n"
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
        self.pushButton_21.setObjectName("pushButton_21")
        self.horizontalLayout_23.addWidget(self.pushButton_21)
        self.pushButton_3 = QtWidgets.QPushButton(self.mon_files_box)
        self.pushButton_3.setStyleSheet("QPushButton {\n"
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
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_23.addWidget(self.pushButton_3)
        self.verticalLayout_6.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.listWidget = QtWidgets.QListWidget(self.mon_files_box)
        self.listWidget.setMaximumSize(QtCore.QSize(16777215, 200))
        self.listWidget.setObjectName("listWidget")
        self.horizontalLayout_24.addWidget(self.listWidget)
        self.verticalLayout_6.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.radioButton_6 = QtWidgets.QRadioButton(self.mon_files_box)
        self.radioButton_6.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_6.setObjectName("radioButton_6")
        self.horizontalLayout_25.addWidget(self.radioButton_6)
        self.checkBox_28 = QtWidgets.QCheckBox(self.mon_files_box)
        self.checkBox_28.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_28.setObjectName("checkBox_28")
        self.horizontalLayout_25.addWidget(self.checkBox_28)
        self.verticalLayout_6.addLayout(self.horizontalLayout_25)
        self.gridLayout_25 = QtWidgets.QGridLayout()
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.radioButton_7 = QtWidgets.QRadioButton(self.mon_files_box)
        self.radioButton_7.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_7.setObjectName("radioButton_7")
        self.gridLayout_25.addWidget(self.radioButton_7, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.mon_files_box)
        self.label_16.setObjectName("label_16")
        self.gridLayout_25.addWidget(self.label_16, 0, 0, 1, 1)
        self.radioButton_8 = QtWidgets.QRadioButton(self.mon_files_box)
        self.radioButton_8.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_8.setObjectName("radioButton_8")
        self.gridLayout_25.addWidget(self.radioButton_8, 0, 2, 1, 1)
        self.radioButton_9 = QtWidgets.QRadioButton(self.mon_files_box)
        self.radioButton_9.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_9.setObjectName("radioButton_9")
        self.gridLayout_25.addWidget(self.radioButton_9, 0, 3, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.checkBox_29 = QtWidgets.QCheckBox(self.mon_files_box)
        self.checkBox_29.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_29.setObjectName("checkBox_29")
        self.verticalLayout_7.addWidget(self.checkBox_29)
        self.checkBox_30 = QtWidgets.QCheckBox(self.mon_files_box)
        self.checkBox_30.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_30.setObjectName("checkBox_30")
        self.verticalLayout_7.addWidget(self.checkBox_30)
        self.gridLayout_25.addLayout(self.verticalLayout_7, 1, 1, 1, 3)
        self.verticalLayout_6.addLayout(self.gridLayout_25)
        self.verticalLayout_8.addLayout(self.verticalLayout_6)
        self.gridLayout_13.addWidget(self.mon_files_box, 1, 0, 1, 1)
        self.playlist_box = QtWidgets.QGroupBox(self.library_tab)
        self.playlist_box.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.playlist_box.setFlat(True)
        self.playlist_box.setCheckable(False)
        self.playlist_box.setObjectName("playlist_box")
        self.gridLayout_27 = QtWidgets.QGridLayout(self.playlist_box)
        self.gridLayout_27.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_27.setSpacing(0)
        self.gridLayout_27.setObjectName("gridLayout_27")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_17 = QtWidgets.QLabel(self.playlist_box)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_26.addWidget(self.label_17)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.playlist_box)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_26.addWidget(self.lineEdit_6)
        self.verticalLayout_9.addLayout(self.horizontalLayout_26)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.checkBox_31 = QtWidgets.QCheckBox(self.playlist_box)
        self.checkBox_31.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_31.setObjectName("checkBox_31")
        self.verticalLayout_10.addWidget(self.checkBox_31)
        self.checkBox_32 = QtWidgets.QCheckBox(self.playlist_box)
        self.checkBox_32.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_32.setObjectName("checkBox_32")
        self.verticalLayout_10.addWidget(self.checkBox_32)
        self.checkBox_33 = QtWidgets.QCheckBox(self.playlist_box)
        self.checkBox_33.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_33.setObjectName("checkBox_33")
        self.verticalLayout_10.addWidget(self.checkBox_33)
        self.verticalLayout_9.addLayout(self.verticalLayout_10)
        self.gridLayout_26 = QtWidgets.QGridLayout()
        self.gridLayout_26.setObjectName("gridLayout_26")
        self.comboBox_5 = QtWidgets.QComboBox(self.playlist_box)
        self.comboBox_5.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.gridLayout_26.addWidget(self.comboBox_5, 0, 2, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.playlist_box)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout_26.addWidget(self.lineEdit_7, 0, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.playlist_box)
        self.label_18.setObjectName("label_18")
        self.gridLayout_26.addWidget(self.label_18, 0, 0, 1, 1)
        self.gridLayout_28 = QtWidgets.QGridLayout()
        self.gridLayout_28.setObjectName("gridLayout_28")
        self.checkBox_34 = QtWidgets.QCheckBox(self.playlist_box)
        self.checkBox_34.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_34.setObjectName("checkBox_34")
        self.gridLayout_28.addWidget(self.checkBox_34, 0, 0, 1, 1)
        self.checkBox_35 = QtWidgets.QCheckBox(self.playlist_box)
        self.checkBox_35.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_35.setObjectName("checkBox_35")
        self.gridLayout_28.addWidget(self.checkBox_35, 2, 0, 1, 1)
        self.checkBox_36 = QtWidgets.QCheckBox(self.playlist_box)
        self.checkBox_36.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_36.setObjectName("checkBox_36")
        self.gridLayout_28.addWidget(self.checkBox_36, 1, 0, 1, 1)
        self.gridLayout_26.addLayout(self.gridLayout_28, 1, 1, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_26)
        self.gridLayout_27.addLayout(self.verticalLayout_9, 0, 0, 1, 1)
        self.gridLayout_13.addWidget(self.playlist_box, 2, 0, 1, 1)
        self.all_tabs_stacked.addWidget(self.library_tab)
        self.tag_tab = QtWidgets.QWidget()
        self.tag_tab.setObjectName("tag_tab")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.tag_tab)
        self.gridLayout_14.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_14.setSpacing(0)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.scrollArea = QtWidgets.QScrollArea(self.tag_tab)
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setStyleSheet(" QScrollBar:vertical {\n"
        "     border:1px solid black;\n"
        "     background: #32CC99;\n"
        "     width: 10px;\n"
        "     margin: 0px 0 0px 0;\n"
        " }\n"
        " QScrollBar::handle:vertical {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 2px;\n"
        "border-color: #000000;\n"
        "padding: 2px;\n"
        "     min-height: 20px;\n"
        " }\n"
        "\n"
        " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
        "     background:#24292E;\n"
        " }\n"
        " QScrollBar::add-line:vertical {\n"
        "none\n"
        " }\n"
        "\n"
        " QScrollBar::sub-line:vertical {\n"
        "none\n"
        " }\n"
        " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
        "none\n"
        " }\n"
        "\n"
        "")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 188, 940))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.groupBox_13 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_13.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_13.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_13.setFlat(True)
        self.groupBox_13.setCheckable(False)
        self.groupBox_13.setObjectName("groupBox_13")
        self.gridLayout_7.addWidget(self.groupBox_13, 3, 0, 1, 1)
        self.groupBox_16 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_16.setMinimumSize(QtCore.QSize(0, 270))
        self.groupBox_16.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_16.setFlat(True)
        self.groupBox_16.setCheckable(False)
        self.groupBox_16.setObjectName("groupBox_16")
        self.gridLayout_36 = QtWidgets.QGridLayout(self.groupBox_16)
        self.gridLayout_36.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_36.setHorizontalSpacing(0)
        self.gridLayout_36.setVerticalSpacing(2)
        self.gridLayout_36.setObjectName("gridLayout_36")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setSpacing(4)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.gridLayout_33 = QtWidgets.QGridLayout()
        self.gridLayout_33.setHorizontalSpacing(0)
        self.gridLayout_33.setVerticalSpacing(2)
        self.gridLayout_33.setObjectName("gridLayout_33")
        self.comboBox_6 = QtWidgets.QComboBox(self.groupBox_16)
        self.comboBox_6.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_6.setObjectName("comboBox_6")
        self.gridLayout_33.addWidget(self.comboBox_6, 0, 1, 1, 1)
        self.checkBox_46 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_46.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_46.setObjectName("checkBox_46")
        self.gridLayout_33.addWidget(self.checkBox_46, 2, 1, 1, 1)
        self.checkBox_47 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_47.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_47.setObjectName("checkBox_47")
        self.gridLayout_33.addWidget(self.checkBox_47, 3, 1, 1, 1)
        self.checkBox_48 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_48.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_48.setObjectName("checkBox_48")
        self.gridLayout_33.addWidget(self.checkBox_48, 1, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.groupBox_16)
        self.label_25.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_25.setObjectName("label_25")
        self.gridLayout_33.addWidget(self.label_25, 0, 0, 1, 1)
        self.verticalLayout_15.addLayout(self.gridLayout_33)
        self.gridLayout_34 = QtWidgets.QGridLayout()
        self.gridLayout_34.setHorizontalSpacing(0)
        self.gridLayout_34.setVerticalSpacing(2)
        self.gridLayout_34.setObjectName("gridLayout_34")
        self.comboBox_7 = QtWidgets.QComboBox(self.groupBox_16)
        self.comboBox_7.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_7.setObjectName("comboBox_7")
        self.gridLayout_34.addWidget(self.comboBox_7, 0, 1, 1, 1)
        self.checkBox_49 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_49.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_49.setObjectName("checkBox_49")
        self.gridLayout_34.addWidget(self.checkBox_49, 2, 1, 1, 1)
        self.checkBox_50 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_50.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_50.setObjectName("checkBox_50")
        self.gridLayout_34.addWidget(self.checkBox_50, 3, 1, 1, 1)
        self.checkBox_51 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_51.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_51.setObjectName("checkBox_51")
        self.gridLayout_34.addWidget(self.checkBox_51, 1, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.groupBox_16)
        self.label_26.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_26.setObjectName("label_26")
        self.gridLayout_34.addWidget(self.label_26, 0, 0, 1, 1)
        self.verticalLayout_15.addLayout(self.gridLayout_34)
        self.gridLayout_35 = QtWidgets.QGridLayout()
        self.gridLayout_35.setHorizontalSpacing(0)
        self.gridLayout_35.setVerticalSpacing(2)
        self.gridLayout_35.setObjectName("gridLayout_35")
        self.comboBox_8 = QtWidgets.QComboBox(self.groupBox_16)
        self.comboBox_8.setObjectName("comboBox_8")
        self.gridLayout_35.addWidget(self.comboBox_8, 0, 1, 1, 1)
        self.checkBox_52 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_52.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_52.setObjectName("checkBox_52")
        self.gridLayout_35.addWidget(self.checkBox_52, 2, 1, 1, 1)
        self.checkBox_53 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_53.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_53.setObjectName("checkBox_53")
        self.gridLayout_35.addWidget(self.checkBox_53, 3, 1, 1, 1)
        self.checkBox_54 = QtWidgets.QCheckBox(self.groupBox_16)
        self.checkBox_54.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_54.setObjectName("checkBox_54")
        self.gridLayout_35.addWidget(self.checkBox_54, 1, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.groupBox_16)
        self.label_27.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_27.setObjectName("label_27")
        self.gridLayout_35.addWidget(self.label_27, 0, 0, 1, 1)
        self.verticalLayout_15.addLayout(self.gridLayout_35)
        self.gridLayout_36.addLayout(self.verticalLayout_15, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_16, 2, 0, 1, 1)
        self.groupBox_18 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_18.setMinimumSize(QtCore.QSize(0, 270))
        self.groupBox_18.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_18.setFlat(True)
        self.groupBox_18.setCheckable(False)
        self.groupBox_18.setObjectName("groupBox_18")
        self.gridLayout_32 = QtWidgets.QGridLayout(self.groupBox_18)
        self.gridLayout_32.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_32.setHorizontalSpacing(0)
        self.gridLayout_32.setObjectName("gridLayout_32")
        self.gridLayout_31 = QtWidgets.QGridLayout()
        self.gridLayout_31.setHorizontalSpacing(0)
        self.gridLayout_31.setVerticalSpacing(4)
        self.gridLayout_31.setObjectName("gridLayout_31")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_21 = QtWidgets.QLabel(self.groupBox_18)
        self.label_21.setObjectName("label_21")
        self.verticalLayout_11.addWidget(self.label_21)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.groupBox_18)
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.verticalLayout_11.addWidget(self.lineEdit_13)
        self.gridLayout_31.addLayout(self.verticalLayout_11, 2, 0, 1, 1)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_22 = QtWidgets.QLabel(self.groupBox_18)
        self.label_22.setObjectName("label_22")
        self.verticalLayout_12.addWidget(self.label_22)
        self.lineEdit_14 = QtWidgets.QLineEdit(self.groupBox_18)
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.verticalLayout_12.addWidget(self.lineEdit_14)
        self.gridLayout_31.addLayout(self.verticalLayout_12, 3, 0, 1, 1)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_23 = QtWidgets.QLabel(self.groupBox_18)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_13.addWidget(self.label_23)
        self.checkBox_42 = QtWidgets.QCheckBox(self.groupBox_18)
        self.checkBox_42.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_42.setObjectName("checkBox_42")
        self.verticalLayout_13.addWidget(self.checkBox_42)
        self.checkBox_43 = QtWidgets.QCheckBox(self.groupBox_18)
        self.checkBox_43.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_43.setObjectName("checkBox_43")
        self.verticalLayout_13.addWidget(self.checkBox_43)
        self.checkBox_44 = QtWidgets.QCheckBox(self.groupBox_18)
        self.checkBox_44.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_44.setObjectName("checkBox_44")
        self.verticalLayout_13.addWidget(self.checkBox_44)
        self.checkBox_45 = QtWidgets.QCheckBox(self.groupBox_18)
        self.checkBox_45.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_45.setObjectName("checkBox_45")
        self.verticalLayout_13.addWidget(self.checkBox_45)
        self.gridLayout_31.addLayout(self.verticalLayout_13, 0, 0, 1, 1)
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.label_24 = QtWidgets.QLabel(self.groupBox_18)
        self.label_24.setObjectName("label_24")
        self.verticalLayout_14.addWidget(self.label_24)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.groupBox_18)
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.verticalLayout_14.addWidget(self.lineEdit_15)
        self.gridLayout_31.addLayout(self.verticalLayout_14, 1, 0, 1, 1)
        self.gridLayout_32.addLayout(self.gridLayout_31, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_18, 1, 0, 1, 1)
        self.groupBox_12 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_12.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox_12.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_12.setFlat(True)
        self.groupBox_12.setCheckable(False)
        self.groupBox_12.setObjectName("groupBox_12")
        self.gridLayout_30 = QtWidgets.QGridLayout(self.groupBox_12)
        self.gridLayout_30.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_30.setSpacing(0)
        self.gridLayout_30.setObjectName("gridLayout_30")
        self.gridLayout_29 = QtWidgets.QGridLayout()
        self.gridLayout_29.setObjectName("gridLayout_29")
        self.checkBox_37 = QtWidgets.QCheckBox(self.groupBox_12)
        self.checkBox_37.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_37.setObjectName("checkBox_37")
        self.gridLayout_29.addWidget(self.checkBox_37, 3, 0, 1, 1)
        self.checkBox_38 = QtWidgets.QCheckBox(self.groupBox_12)
        self.checkBox_38.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_38.setObjectName("checkBox_38")
        self.gridLayout_29.addWidget(self.checkBox_38, 2, 0, 1, 1)
        self.checkBox_40 = QtWidgets.QCheckBox(self.groupBox_12)
        self.checkBox_40.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_40.setObjectName("checkBox_40")
        self.gridLayout_29.addWidget(self.checkBox_40, 1, 0, 1, 1)
        self.checkBox_39 = QtWidgets.QCheckBox(self.groupBox_12)
        self.checkBox_39.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_39.setObjectName("checkBox_39")
        self.gridLayout_29.addWidget(self.checkBox_39, 5, 0, 1, 1)
        self.lineEdit_9 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.gridLayout_29.addWidget(self.lineEdit_9, 2, 1, 1, 1)
        self.checkBox_41 = QtWidgets.QCheckBox(self.groupBox_12)
        self.checkBox_41.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_41.setObjectName("checkBox_41")
        self.gridLayout_29.addWidget(self.checkBox_41, 4, 0, 1, 1)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.gridLayout_29.addWidget(self.lineEdit_8, 1, 1, 1, 1)
        self.lineEdit_10 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.gridLayout_29.addWidget(self.lineEdit_10, 3, 1, 1, 1)
        self.lineEdit_12 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.gridLayout_29.addWidget(self.lineEdit_12, 5, 1, 1, 1)
        self.lineEdit_11 = QtWidgets.QLineEdit(self.groupBox_12)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.gridLayout_29.addWidget(self.lineEdit_11, 4, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.groupBox_12)
        self.label_19.setMaximumSize(QtCore.QSize(4412, 18))
        self.label_19.setObjectName("label_19")
        self.gridLayout_29.addWidget(self.label_19, 0, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.groupBox_12)
        self.label_20.setMaximumSize(QtCore.QSize(4412, 18))
        self.label_20.setObjectName("label_20")
        self.gridLayout_29.addWidget(self.label_20, 0, 1, 1, 1)
        self.gridLayout_30.addLayout(self.gridLayout_29, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBox_12, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_14.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.all_tabs_stacked.addWidget(self.tag_tab)
        self.player_tab = QtWidgets.QWidget()
        self.player_tab.setObjectName("player_tab")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.player_tab)
        self.gridLayout_15.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_15.setSpacing(0)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.groupBox_5 = QtWidgets.QGroupBox(self.player_tab)
        self.groupBox_5.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_5.setFlat(True)
        self.groupBox_5.setCheckable(False)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_41 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_41.setContentsMargins(10, 0, 0, 0)
        self.gridLayout_41.setSpacing(0)
        self.gridLayout_41.setObjectName("gridLayout_41")
        self.gridLayout_40 = QtWidgets.QGridLayout()
        self.gridLayout_40.setObjectName("gridLayout_40")
        self.gridLayout_39 = QtWidgets.QGridLayout()
        self.gridLayout_39.setVerticalSpacing(9)
        self.gridLayout_39.setObjectName("gridLayout_39")
        self.label_29 = QtWidgets.QLabel(self.groupBox_5)
        self.label_29.setObjectName("label_29")
        self.gridLayout_39.addWidget(self.label_29, 0, 0, 1, 1)
        self.comboBox_10 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_10.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_10.setObjectName("comboBox_10")
        self.gridLayout_39.addWidget(self.comboBox_10, 0, 1, 1, 1)
        self.checkBox_66 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_66.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_66.setObjectName("checkBox_66")
        self.gridLayout_39.addWidget(self.checkBox_66, 1, 1, 1, 1)
        self.comboBox_11 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_11.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_11.setObjectName("comboBox_11")
        self.gridLayout_39.addWidget(self.comboBox_11, 5, 1, 1, 1)
        self.checkBox_67 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_67.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_67.setObjectName("checkBox_67")
        self.gridLayout_39.addWidget(self.checkBox_67, 7, 1, 1, 1)
        self.checkBox_68 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_68.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_68.setObjectName("checkBox_68")
        self.gridLayout_39.addWidget(self.checkBox_68, 6, 1, 1, 1)
        self.checkBox_69 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_69.setObjectName("checkBox_69")
        self.gridLayout_39.addWidget(self.checkBox_69, 4, 1, 1, 1)
        self.checkBox_70 = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_70.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_70.setObjectName("checkBox_70")
        self.gridLayout_39.addWidget(self.checkBox_70, 4, 1, 1, 1)
        self.horizontalSlider = QtWidgets.QSlider(self.groupBox_5)
        self.horizontalSlider.setStyleSheet("QSlider::handle:horizontal {\n"
        "    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n"
        "    border: 1px solid #5c5c5c;\n"
        "    width: 18px;\n"
        "    margin: -2px 0; /* handle is placed by default on the contents rect of the groove. Expand outside the groove */\n"
        "    border-radius: 3px;\n"
        "}\n"
        "\n"
        "QSlider::add-page:horizonta {\n"
        "    \n"
        "    background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "}\n"
        "\n"
        "QSlider::sub-page:horizonta{\n"
        "background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.0909091 rgba(59, 78, 97, 255), stop:0.255682 rgba(40, 88, 135, 255), stop:0.619318 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "}")
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.gridLayout_39.addWidget(self.horizontalSlider, 3, 1, 1, 1)
        self.gridLayout_40.addLayout(self.gridLayout_39, 1, 0, 1, 1)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_28 = QtWidgets.QLabel(self.groupBox_5)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_27.addWidget(self.label_28)
        self.comboBox_9 = QtWidgets.QComboBox(self.groupBox_5)
        self.comboBox_9.setStyleSheet("QComboBox {\n"
        "    border: 1px solid gray;\n"
        "    border-radius: 3px;\n"
        "    padding: 1px 18px 1px 3px;\n"
        "    min-width: 6em;\n"
        "}\n"
        "\n"
        "QComboBox:editable {\n"
        "background-color: rgb(47, 54, 67);\n"
        "}\n"
        "\n"
        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "/* QComboBox gets the \"on\" state when the popup is open */\n"
        "QComboBox:!editable:on, QComboBox::drop-down:editable:one {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.08, y1:0, x2:1, y2:0, stop:0 rgba(47, 54, 67, 255), stop:0.454545 rgba(68, 85, 117, 255), stop:0.755682 rgba(69, 94, 142, 255), stop:1 rgba(83, 117, 182, 255));\n"
        "}\n"
        "\n"
        "QComboBox:on { /* shift the text when the popup opens */\n"
        "    padding-top:1px;\n"
        "    padding-left: 1px;\n"
        "}\n"
        "\n"
        "QComboBox::drop-down {\n"
        "    subcontrol-origin: padding;\n"
        "    subcontrol-position: top right;\n"
        "    width: 15px;\n"
        "    border-left-width: 1px;\n"
        "    border-left-color: darkgray;\n"
        "    border-left-style: solid; /* just a single line */\n"
        "    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
        "    border-bottom-right-radius: 3px;\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow {\n"
        "   \n"
        "    background-color: qconicalgradient(cx:0.5, cy:0.523, angle:269.5, stop:0.375 rgba(255, 0, 0, 0), stop:0.375957 rgba(255, 0, 0, 0), stop:0.375982 rgba(21, 0, 0, 255), stop:0.5 rgba(75, 75, 75, 255), stop:0.619318 rgba(0, 0, 0, 255), stop:0.625 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
        "    top: 1px;\n"
        "    left: 1px;\n"
        "}")
        self.comboBox_9.setObjectName("comboBox_9")
        self.horizontalLayout_27.addWidget(self.comboBox_9)
        self.pushButton_6 = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_6.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 4em;\n"
        "padding:4px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_27.addWidget(self.pushButton_6)
        self.gridLayout_40.addLayout(self.horizontalLayout_27, 0, 0, 1, 1)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_30 = QtWidgets.QLabel(self.groupBox_5)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_28.addWidget(self.label_30)
        self.radioButton_10 = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_10.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_10.setObjectName("radioButton_10")
        self.horizontalLayout_28.addWidget(self.radioButton_10)
        self.radioButton_11 = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_11.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_11.setObjectName("radioButton_11")
        self.horizontalLayout_28.addWidget(self.radioButton_11)
        self.radioButton_12 = QtWidgets.QRadioButton(self.groupBox_5)
        self.radioButton_12.setStyleSheet("QRadioButton::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::unchecked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(255, 0, 0, 255), stop:0.943182 rgba(255, 0, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "\n"
        "QRadioButton::indicator::checked {\n"
        "background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(0, 0, 0, 255), stop:0.505682 rgba(25, 0, 0, 255), stop:0.693182 rgba(36, 255, 0, 255), stop:0.943182 rgba(25, 255, 0, 255), stop:1 rgba(255, 255, 255, 0));\n"
        "}\n"
        "")
        self.radioButton_12.setObjectName("radioButton_12")
        self.horizontalLayout_28.addWidget(self.radioButton_12)
        self.gridLayout_40.addLayout(self.horizontalLayout_28, 3, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_40.addItem(spacerItem6, 2, 0, 1, 1)
        self.gridLayout_41.addLayout(self.gridLayout_40, 0, 0, 1, 1)
        self.gridLayout_15.addWidget(self.groupBox_5, 0, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.player_tab)
        self.groupBox_4.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setCheckable(False)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_38 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_38.setObjectName("gridLayout_38")
        self.gridLayout_37 = QtWidgets.QGridLayout()
        self.gridLayout_37.setObjectName("gridLayout_37")
        self.checkBox_55 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_55.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_55.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_55.setObjectName("checkBox_55")
        self.gridLayout_37.addWidget(self.checkBox_55, 0, 0, 1, 1)
        self.checkBox_56 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_56.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_56.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_56.setObjectName("checkBox_56")
        self.gridLayout_37.addWidget(self.checkBox_56, 8, 0, 1, 1)
        self.checkBox_57 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_57.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_57.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_57.setObjectName("checkBox_57")
        self.gridLayout_37.addWidget(self.checkBox_57, 9, 0, 1, 1)
        self.checkBox_58 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_58.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_58.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_58.setObjectName("checkBox_58")
        self.gridLayout_37.addWidget(self.checkBox_58, 7, 0, 1, 1)
        self.checkBox_59 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_59.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_59.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_59.setObjectName("checkBox_59")
        self.gridLayout_37.addWidget(self.checkBox_59, 3, 0, 1, 1)
        self.checkBox_60 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_60.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_60.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_60.setObjectName("checkBox_60")
        self.gridLayout_37.addWidget(self.checkBox_60, 5, 0, 1, 1)
        self.checkBox_61 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_61.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_61.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_61.setObjectName("checkBox_61")
        self.gridLayout_37.addWidget(self.checkBox_61, 6, 0, 1, 1)
        self.checkBox_62 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_62.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_62.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_62.setObjectName("checkBox_62")
        self.gridLayout_37.addWidget(self.checkBox_62, 4, 0, 1, 1)
        self.checkBox_63 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_63.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_63.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_63.setObjectName("checkBox_63")
        self.gridLayout_37.addWidget(self.checkBox_63, 2, 0, 1, 1)
        self.checkBox_64 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_64.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_64.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_64.setObjectName("checkBox_64")
        self.gridLayout_37.addWidget(self.checkBox_64, 1, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_4.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 4em;\n"
        "padding:4px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_37.addWidget(self.pushButton_4, 9, 1, 1, 1)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.gridLayout_37.addWidget(self.lineEdit_16, 8, 1, 1, 1)
        self.lineEdit_17 = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.gridLayout_37.addWidget(self.lineEdit_17, 7, 1, 1, 1)
        self.checkBox_65 = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_65.setMinimumSize(QtCore.QSize(300, 0))
        self.checkBox_65.setStyleSheet("QCheckBox {\n"
        "    spacing: 5px;\n"
        "}\n"
        "QCheckBox::indicator {\n"
        "    width: 13px;\n"
        "    height: 13px;\n"
        "}\n"
        "QCheckBox::indicator:unchecked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}\n"
        "QCheckBox::indicator:checked {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(0, 255, 18, 255), stop:0.306818 rgba(10, 171, 24, 255), stop:0.636364 rgba(25, 173, 41, 255), stop:0.994318 rgba(33, 104, 47, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 1em;\n"
        "padding: 1px;\n"
        "}")
        self.checkBox_65.setObjectName("checkBox_65")
        self.gridLayout_37.addWidget(self.checkBox_65, 10, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton_5.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 4em;\n"
        "padding:4px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_37.addWidget(self.pushButton_5, 10, 1, 1, 1)
        self.gridLayout_38.addLayout(self.gridLayout_37, 0, 0, 1, 1)
        self.gridLayout_15.addWidget(self.groupBox_4, 1, 0, 1, 1)
        self.all_tabs_stacked.addWidget(self.player_tab)
        self.hotkeys_tab = QtWidgets.QWidget()
        self.hotkeys_tab.setObjectName("hotkeys_tab")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.hotkeys_tab)
        self.gridLayout_16.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_16.setSpacing(0)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.groupBox_21 = QtWidgets.QGroupBox(self.hotkeys_tab)
        self.groupBox_21.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_21.setFlat(True)
        self.groupBox_21.setCheckable(False)
        self.groupBox_21.setObjectName("groupBox_21")
        self.gridLayout_43 = QtWidgets.QGridLayout(self.groupBox_21)
        self.gridLayout_43.setObjectName("gridLayout_43")
        self.gridLayout_42 = QtWidgets.QGridLayout()
        self.gridLayout_42.setObjectName("gridLayout_42")
        self.lineEdit_18 = QtWidgets.QLineEdit(self.groupBox_21)
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.gridLayout_42.addWidget(self.lineEdit_18, 2, 1, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.groupBox_21)
        self.label_31.setObjectName("label_31")
        self.gridLayout_42.addWidget(self.label_31, 2, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.groupBox_21)
        self.pushButton_7.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 4em;\n"
        "padding:4px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_42.addWidget(self.pushButton_7, 2, 2, 1, 1)
        self.label_32 = QtWidgets.QLabel(self.groupBox_21)
        self.label_32.setObjectName("label_32")
        self.gridLayout_42.addWidget(self.label_32, 1, 0, 1, 4)
        self.pushButton_8 = QtWidgets.QPushButton(self.groupBox_21)
        self.pushButton_8.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(36, 41, 46, 255), stop:0.653409 rgba(59, 78, 97, 255), stop:0.761364 rgba(40, 88, 135, 255), stop:0.892045 rgba(31, 112, 194, 255), stop:1 rgba(47, 139, 230, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "min-width: 4em;\n"
        "padding:4px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_42.addWidget(self.pushButton_8, 2, 3, 1, 1)
        self.listView_2 = QtWidgets.QListView(self.groupBox_21)
        self.listView_2.setObjectName("listView_2")
        self.gridLayout_42.addWidget(self.listView_2, 0, 0, 1, 4)
        self.gridLayout_43.addLayout(self.gridLayout_42, 0, 0, 1, 1)
        self.gridLayout_16.addWidget(self.groupBox_21, 0, 0, 1, 1)
        self.all_tabs_stacked.addWidget(self.hotkeys_tab)
        self.sorting_grouping_tab = QtWidgets.QWidget()
        self.sorting_grouping_tab.setObjectName("sorting_grouping_tab")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.sorting_grouping_tab)
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_17.setSpacing(0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.groupBox_22 = QtWidgets.QGroupBox(self.sorting_grouping_tab)
        self.groupBox_22.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_22.setFlat(True)
        self.groupBox_22.setCheckable(False)
        self.groupBox_22.setObjectName("groupBox_22")
        self.gridLayout_17.addWidget(self.groupBox_22, 1, 0, 1, 1)
        self.groupBox_23 = QtWidgets.QGroupBox(self.sorting_grouping_tab)
        self.groupBox_23.setStyleSheet("background-color: #24292E ;\n"
        "font: 10pt \"MS Shell Dlg 2\";\n"
        "letter-spacing: 2px;\n"
        "word-spacing: 1.4px;\n"
        "color: #D0D4D9;\n"
        "")
        self.groupBox_23.setFlat(True)
        self.groupBox_23.setCheckable(False)
        self.groupBox_23.setObjectName("groupBox_23")
        self.gridLayout_17.addWidget(self.groupBox_23, 0, 0, 1, 1)
        self.all_tabs_stacked.addWidget(self.sorting_grouping_tab)
        self.file_cov_tab = QtWidgets.QWidget()
        self.file_cov_tab.setObjectName("file_cov_tab")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.file_cov_tab)
        self.gridLayout_18.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_18.setSpacing(0)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.all_tabs_stacked.addWidget(self.file_cov_tab)
        self.tool_tab = QtWidgets.QWidget()
        self.tool_tab.setObjectName("tool_tab")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.tool_tab)
        self.gridLayout_19.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_19.setSpacing(0)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.all_tabs_stacked.addWidget(self.tool_tab)
        self.main_grid.addWidget(self.all_tabs_stacked, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.main_grid_2, 1, 0, 1, 1)
        self.title_bar_2 = QtWidgets.QWidget(self.main_frame)
        self.title_bar_2.setMinimumSize(QtCore.QSize(0, 30))
        self.title_bar_2.setMaximumSize(QtCore.QSize(16777215, 35))
        self.title_bar_2.setObjectName("title_bar_2")
        self.title_bar = QtWidgets.QHBoxLayout(self.title_bar_2)
        self.title_bar.setContentsMargins(0, 0, 0, 0)
        self.title_bar.setSpacing(0)
        self.title_bar.setObjectName("title_bar")
        self.title_bar_label = QtWidgets.QLabel(self.title_bar_2)
        font = QtGui.QFont()
        font.setFamily("Arial,Helvetica,sans-serif")
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.title_bar_label.setFont(font)
        self.title_bar_label.setObjectName("title_bar_label")
        self.title_bar.addWidget(self.title_bar_label)
        self.label = QtWidgets.QLabel(self.title_bar_2)
        self.label.setMinimumSize(QtCore.QSize(575, 0))
        self.label.setText("")
        self.label.setObjectName("label")
        self.title_bar.addWidget(self.label)
        self.close_window_button = QtWidgets.QPushButton(self.title_bar_2)
        self.close_window_button.setMinimumSize(QtCore.QSize(0, 25))
        self.close_window_button.setMaximumSize(QtCore.QSize(25, 25))
        self.close_window_button.setAutoFillBackground(False)
        self.close_window_button.setStyleSheet("QPushButton {\n"
        "background-color: qlineargradient(spread:reflect, x1:0.54, y1:1, x2:0.534, y2:0, stop:0 rgba(255, 0, 0, 255), stop:0.528409 rgba(173, 25, 25, 255), stop:1 rgba(187, 60, 60, 255));\n"
        "border-style: outset;\n"
        "border-width: 1px;\n"
        "border-radius: 6px;\n"
        "border-color: #000000;\n"
        "padding: 6px;\n"
        "}\n"
        "QPushButton:pressed {\n"
        "       background-color: rgb(47, 54, 67);\n"
        "    border-style: inset;\n"
        "}")
        self.close_window_button.setText("")
        self.close_window_button.setIconSize(QtCore.QSize(30, 30))
        self.close_window_button.setObjectName("close_window_button")
        self.title_bar.addWidget(self.close_window_button)
        self.gridLayout.addWidget(self.title_bar_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.main_frame, 0, 0, 1, 1)
        preferences_window.setCentralWidget(self.main_widget)

        self.retranslateUi(preferences_window)
        self.all_tabs_stacked.setCurrentIndex(0)
        self.close_window_button.clicked.connect(preferences_window.close)
        self.close_button.clicked.connect(preferences_window.close)
        QtCore.QMetaObject.connectSlotsByName(preferences_window)

    def retranslateUi(self, preferences_window):
        _translate = QtCore.QCoreApplication.translate
        preferences_window.setWindowTitle(_translate("preferences_window", "Preferences"))
        self.apply_button.setText(_translate("preferences_window", "Apply"))
        self.save_button.setText(_translate("preferences_window", "Save"))
        self.close_button.setText(_translate("preferences_window", "Close"))
        self.general_btn.setText(_translate("preferences_window", "General"))
        self.now_playing_btn.setText(_translate("preferences_window", "Now Playing"))
        self.layout_btn.setText(_translate("preferences_window", "Layout"))
        self.library_btn.setText(_translate("preferences_window", "Library"))
        self.tags_btn.setText(_translate("preferences_window", "Tags"))
        self.players_btn.setText(_translate("preferences_window", "Players"))
        self.hotkeys_btn.setText(_translate("preferences_window", "Hotkeys"))
        self.sort_gp_btn.setText(_translate("preferences_window", "Sorting/Grouping"))
        self.file_con_btn.setText(_translate("preferences_window", "File Converters"))
        self.tools_btn.setText(_translate("preferences_window", "Tools"))
        self.misc_box.setTitle(_translate("preferences_window", "Miscellaneous"))
        self.checkBox_10.setText(_translate("preferences_window", "Warn When Duplicate Tracks are Added to Playlist"))
        self.checkBox_11.setText(_translate("preferences_window", "Warn When Files Are Not Recognized"))
        self.checkBox_71.setText(_translate("preferences_window", "Confirm When Tags Are Modified"))
        self.checkBox_12.setText(_translate("preferences_window", "Confirm Permanant File Deletion"))
        self.checkBox_72.setText(_translate("preferences_window", "Confirm Removal of File from Playlist"))
        self.checkBox_73.setText(_translate("preferences_window", "Confirm When Modifing Artwork"))
        self.checkBox_74.setText(_translate("preferences_window", "Confirm Removal Of Dead Links From Library"))
        self.checkBox_13.setText(_translate("preferences_window", "Confirm When Switcing Between Audio Devices"))
        self.checkBox_75.setText(_translate("preferences_window", "Confirm When New Items are Added to the library"))
        self.checkBox_76.setText(_translate("preferences_window", "Confirm When New Auto Playlist is Generated"))
        self.application_box.setTitle(_translate("preferences_window", "Application"))
        self.label_2.setText(_translate("preferences_window", "Startup Mode"))
        self.comboBox_startup_mode.setItemText(0, _translate("preferences_window", "Main Player"))
        self.comboBox_startup_mode.setItemText(1, _translate("preferences_window", "Taskbar"))
        self.comboBox_startup_mode.setItemText(2, _translate("preferences_window", "Mini Player"))
        self.comboBox_startup_mode.setItemText(3, _translate("preferences_window", "Compact Player"))
        self.checkBoxsplash_screen.setText(_translate("preferences_window", "Display Splash Screen"))
        self.checkBox_min_totask.setText(_translate("preferences_window", "Minimize to Taskbar"))
        self.checkBox_play_str.setText(_translate("preferences_window", "Play on Startup"))
        self.checkBox_chkOnsstr.setText(_translate("preferences_window", "Check for Updates on Startup"))
        self.file_types_box.setTitle(_translate("preferences_window", "File Types"))
        self.checkBox_wav.setText(_translate("preferences_window", ".wav ( Waveform Audio File )"))
        self.checkBox_aiff.setText(_translate("preferences_window", ".aiff ( Audio Interchange File Format )"))
        self.checkBox_ogg.setText(_translate("preferences_window", ".ogg ( Ogg )"))
        self.checkBox_mp3.setText(_translate("preferences_window", ".mp3 ( MPEG Audio Layer-3 )"))
        self.checkBox_alac.setText(_translate("preferences_window", ".alac ( Apple Lossless Audio Codec )"))
        self.checkBox_acc.setText(_translate("preferences_window", ".aac ( Advanced Audio Coding )"))
        self.checkBox_wma.setText(_translate("preferences_window", ".wma ( Windows Media Audio )"))
        self.checkBox_flac.setText(_translate("preferences_window", ".flac ( Free Lossless Audio Codec )"))
        self.apply_button_3.setText(_translate("preferences_window", "Select All"))
        self.apply_button_2.setText(_translate("preferences_window", "Select None"))
        self.playing_track_Box.setTitle(_translate("preferences_window", "Playing Track List"))
        self.label_7.setText(_translate("preferences_window", "Action When Track is Double-clicked"))
        self.label_8.setText(_translate("preferences_window", "Playing Track"))
        self.comboBox_13.setItemText(0, _translate("preferences_window", "Play Now"))
        self.comboBox_13.setItemText(1, _translate("preferences_window", "Queue Next"))
        self.comboBox_13.setItemText(2, _translate("preferences_window", "Queue Last"))
        self.label_9.setText(_translate("preferences_window", "Playback Stopped"))
        self.comboBox_12.setItemText(0, _translate("preferences_window", "Play Now"))
        self.comboBox_12.setItemText(1, _translate("preferences_window", "Queue Next"))
        self.comboBox_12.setItemText(2, _translate("preferences_window", "Queue Last"))
        self.label_10.setText(_translate("preferences_window", "Play Now action"))
        self.radioButton_16.setText(_translate("preferences_window", "Clear List and Play Selected Track Only"))
        self.radioButton_17.setText(_translate("preferences_window", "Clear List and Play Album Only"))
        self.radioButton_18.setText(_translate("preferences_window", "Clear List and Play All Tracks"))
        self.shuffle_box.setTitle(_translate("preferences_window", "Shuffle Settings"))
        self.radioButton.setText(_translate("preferences_window", "Random"))
        self.radioButton_4.setText(_translate("preferences_window", "Random By Album"))
        self.radioButton_3.setText(_translate("preferences_window", "Recently added Random"))
        self.radioButton_5.setText(_translate("preferences_window", "Most Played "))
        self.radioButton_2.setText(_translate("preferences_window", "Rating"))
        self.playback_box.setTitle(_translate("preferences_window", "Playback"))
        self.checkBox_14.setText(_translate("preferences_window", "Switch Player to While Playing"))
        self.comboBox_2.setItemText(0, _translate("preferences_window", "Normal Player"))
        self.comboBox_2.setItemText(1, _translate("preferences_window", "Compact Player"))
        self.comboBox_2.setItemText(2, _translate("preferences_window", "Task Bar"))
        self.comboBox_2.setItemText(3, _translate("preferences_window", "Mini Player"))
        self.checkBox_15.setText(_translate("preferences_window", "Show in Taskbar As"))
        self.pushButton.setText(_translate("preferences_window", "..."))
        self.checkBox_16.setText(_translate("preferences_window", "Show in Player As"))
        self.pushButton_2.setText(_translate("preferences_window", "..."))
        self.checkBox_17.setText(_translate("preferences_window", "Highlight Track in Platlist"))
        self.checkBox_18.setText(_translate("preferences_window", "Highlight Track In Main Player"))
        self.checkBox_19.setText(_translate("preferences_window", "Playback Follows Cursor"))
        self.checkBox_20.setText(_translate("preferences_window", "Show Taskbar Popups"))
        self.label_12.setText(_translate("preferences_window", "Skip 1 Track: Less Than"))
        self.label_13.setText(_translate("preferences_window", "% of Track is Played or Seconds is "))
        self.label_14.setText(_translate("preferences_window", "Play 1 Track: More Than"))
        self.label_15.setText(_translate("preferences_window", "% of Track is Played or Seconds is "))
        self.musi_library_box.setTitle(_translate("preferences_window", "Music Library"))
        self.checkBox_22.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_23.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_24.setText(_translate("preferences_window", "CheckBox"))
        self.pushButton1.setText(_translate("preferences_window", "PushButton"))
        self.checkBox_25.setText(_translate("preferences_window", "CheckBox"))
        self.mon_files_box.setTitle(_translate("preferences_window", "Monitored Files"))
        self.checkBox_26.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_27.setText(_translate("preferences_window", "CheckBox"))
        self.pushButton_21.setText(_translate("preferences_window", "PushButton"))
        self.pushButton_3.setText(_translate("preferences_window", "PushButton"))
        self.radioButton_6.setText(_translate("preferences_window", "RadioButton"))
        self.checkBox_28.setText(_translate("preferences_window", "CheckBox"))
        self.radioButton_7.setText(_translate("preferences_window", "RadioButton"))
        self.label_16.setText(_translate("preferences_window", "TextLabel"))
        self.radioButton_8.setText(_translate("preferences_window", "RadioButton"))
        self.radioButton_9.setText(_translate("preferences_window", "RadioButton"))
        self.checkBox_29.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_30.setText(_translate("preferences_window", "CheckBox"))
        self.playlist_box.setTitle(_translate("preferences_window", "Playlists"))
        self.label_17.setText(_translate("preferences_window", "TextLabel"))
        self.checkBox_31.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_32.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_33.setText(_translate("preferences_window", "CheckBox"))
        self.comboBox_5.setItemText(0, _translate("preferences_window", ".json"))
        self.comboBox_5.setItemText(1, _translate("preferences_window", ".csv"))
        self.comboBox_5.setItemText(2, _translate("preferences_window", ".xml"))
        self.label_18.setText(_translate("preferences_window", "TextLabel"))
        self.checkBox_34.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_35.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_36.setText(_translate("preferences_window", "CheckBox"))
        self.groupBox_13.setTitle(_translate("preferences_window", "Monitored Files"))
        self.groupBox_16.setTitle(_translate("preferences_window", "Auto Tagging"))
        self.checkBox_46.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_47.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_48.setText(_translate("preferences_window", "CheckBox"))
        self.label_25.setText(_translate("preferences_window", "TextLabel"))
        self.checkBox_49.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_50.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_51.setText(_translate("preferences_window", "CheckBox"))
        self.label_26.setText(_translate("preferences_window", "TextLabel"))
        self.checkBox_52.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_53.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_54.setText(_translate("preferences_window", "CheckBox"))
        self.label_27.setText(_translate("preferences_window", "TextLabel"))
        self.groupBox_18.setTitle(_translate("preferences_window", "Artwork/Lyrics"))
        self.label_21.setText(_translate("preferences_window", "TextLabel"))
        self.label_22.setText(_translate("preferences_window", "TextLabel"))
        self.label_23.setText(_translate("preferences_window", "TextLabel"))
        self.checkBox_42.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_43.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_44.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_45.setText(_translate("preferences_window", "CheckBox"))
        self.label_24.setText(_translate("preferences_window", "TextLabel"))
        self.groupBox_12.setTitle(_translate("preferences_window", "Custom Tags"))
        self.checkBox_37.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_38.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_40.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_39.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_41.setText(_translate("preferences_window", "CheckBox"))
        self.label_19.setText(_translate("preferences_window", "TextLabel"))
        self.label_20.setText(_translate("preferences_window", "TextLabel"))
        self.groupBox_5.setTitle(_translate("preferences_window", "Audio Player"))
        self.label_29.setText(_translate("preferences_window", "TextLabel"))
        self.checkBox_66.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_67.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_68.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_69.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_70.setText(_translate("preferences_window", "CheckBox"))
        self.label_28.setText(_translate("preferences_window", "TextLabel"))
        self.pushButton_6.setText(_translate("preferences_window", "PushButton"))
        self.label_30.setText(_translate("preferences_window", "TextLabel"))
        self.radioButton_10.setText(_translate("preferences_window", "RadioButton"))
        self.radioButton_11.setText(_translate("preferences_window", "RadioButton"))
        self.radioButton_12.setText(_translate("preferences_window", "RadioButton"))
        self.groupBox_4.setTitle(_translate("preferences_window", "Audio Effects"))
        self.checkBox_55.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_56.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_57.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_58.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_59.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_60.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_61.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_62.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_63.setText(_translate("preferences_window", "CheckBox"))
        self.checkBox_64.setText(_translate("preferences_window", "CheckBox"))
        self.pushButton_4.setText(_translate("preferences_window", "PushButton"))
        self.checkBox_65.setText(_translate("preferences_window", "CheckBox"))
        self.pushButton_5.setText(_translate("preferences_window", "PushButton"))
        self.groupBox_21.setTitle(_translate("preferences_window", "Hotkeys"))
        self.label_31.setText(_translate("preferences_window", "TextLabel"))
        self.pushButton_7.setText(_translate("preferences_window", "PushButton"))
        self.label_32.setText(_translate("preferences_window", "TextLabel"))
        self.pushButton_8.setText(_translate("preferences_window", "PushButton"))
        self.groupBox_22.setTitle(_translate("preferences_window", "Grouping"))
        self.groupBox_23.setTitle(_translate("preferences_window", "Sorting"))
        self.title_bar_label.setText(_translate("preferences_window", "Preferences"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    preferences_window = QtWidgets.QMainWindow()
    ui = Ui_preferences_window()
    ui.setupUi(preferences_window)
    preferences_window.show()
    sys.exit(app.exec_())
