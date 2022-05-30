import os
from pathlib import PurePath

from PySide6 import QtCore, QtGui, QtWidgets
from pytest_cases import get_case_id


def IDGen(case_fun) -> str:
    return "#%s#" % get_case_id(case_fun)


def get_qt_application() -> QtWidgets.QApplication:
    if not QtWidgets.QApplication.instance():
        _qt_application = QtWidgets.QApplication()
    else:
        _qt_application = QtWidgets.QApplication.instance()

    return _qt_application


def screenshot_widget(widget: QtWidgets.QWidget, name: str):
    pixmap = QtGui.QPixmap(widget.rect().size())
    painter = QtGui.QPainter(pixmap)
    painter.save()
    widget.setScreen(QtWidgets.QApplication.screens()[0])
    widget.render(painter, QtCore.QPoint(), widget.rect())
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'pytest_qt_apollo', 'output')):
        os.mkdir(os.path.join(os.path.dirname(__file__), 'pytest_qt_apollo', 'output'))
    pixmap.save(os.path.join(os.path.dirname(__file__), 'pytest_qt_apollo', 'output', name + '.png'))
    painter.end()
