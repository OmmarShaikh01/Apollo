import os
import random
import shutil
import uuid
from pathlib import PurePath

from PySide6 import QtCore, QtGui, QtWidgets
from pytest_cases import get_case_id

from apollo.media import Stream


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
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "pytest_qt_apollo", "output")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "pytest_qt_apollo", "output"))
    pixmap.save(
        os.path.join(os.path.dirname(__file__), "pytest_qt_apollo", "output", name + ".png")
    )
    painter.end()


def get_library_table(rows: int = 1111):
    table = []
    for row_index in range(rows):
        row = []
        for col_index, (col, _type) in enumerate(Stream.TAG_FRAMES_FIELDS):
            if col == "FILEID":
                row.append(str(uuid.uuid4()))
            elif col == "SONGLEN":
                row.append(random.randint(30, 240))
            elif _type == "STRING":
                row.append(f"TESTING_{col}_{row_index}")
            elif _type == "INTEGER":
                row.append(row_index)
            elif _type == "BOOLEAN":
                row.append(True)
            else:
                continue
        table.append(row)
    return table


LIBRARY_TABLE = get_library_table()
