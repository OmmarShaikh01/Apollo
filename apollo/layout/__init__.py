import ctypes
from pathlib import PurePath

from PySide6 import QtGui, QtWidgets

from apollo.layout.mainwindow import Ui_MainWindow as _Apollo_MainWindow
from apollo.layout.preferences import Ui_MainWindow as _Preferences_SubWindow
from configs import settings as CONFIG


def set_app_icon(widget: QtWidgets.QMainWindow):
    """
    Sets the title bar icon
    """

    path = PurePath(CONFIG.project_root) / "apollo" / "assets" / "Apollo_App_Icon_Small.svg"
    pixmap = QtGui.QPixmap.fromImage(QtGui.QImage(str(path))).scaled(48, 48)
    widget.setWindowIcon(QtGui.QIcon(pixmap))

    WINDLL = ctypes.windll
    if CONFIG["APOLLO.MAIN.IS_TITLEBAR_DARK"]:
        HWND = widget.winId()
        WINDLL.dwmapi.DwmSetWindowAttribute(
            HWND, 20, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2))
        )


class Apollo_MainWindow_UI(QtWidgets.QMainWindow, _Apollo_MainWindow):
    """
    Apollo_Mainwindow implementation class
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        set_app_icon(self)


class Preferences_SubWindow_UI(QtWidgets.QMainWindow, _Preferences_SubWindow):
    """
    Preferences_SubWindow implementation class
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        set_app_icon(self)
