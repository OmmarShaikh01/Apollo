from PySide6 import QtWidgets
from pytest_cases import get_case_id


def IDGen(case_fun) -> str:
    return "#%s#" % get_case_id(case_fun)


def get_qt_application() -> QtWidgets.QApplication:
    if not QtWidgets.QApplication.instance():
        _qt_application = QtWidgets.QApplication()
    else:
        _qt_application = QtWidgets.QApplication.instance()

    return _qt_application
