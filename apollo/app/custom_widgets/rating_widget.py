import math
from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from apollo.app.sub_tabs.utils import drawStars


class TrackRatingWidget(QtWidgets.QWidget):
    """
    Rating Widget, modifies and displays track rating
    """

    RatingChangedSignal = QtCore.Signal(float)

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        """
        Constructor

        Args:
            parent (Optional[QtWidgets.QWidget]): Parent widget
        """
        super().__init__(parent)
        self.setMouseTracking(True)
        self.rating = 0
        self._rating = 0
        self._temp_rating = self._rating

    def setRating(self, rating: Optional[float] = 0):
        """
        Modifies the currently displayed rating

        Args:
            rating (Optional[float]): rating to set
        """
        self._rating = rating
        self.rating = rating
        self.RatingChangedSignal.emit(rating)
        self.update()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.underMouse():
            width = (round(self.mapFromGlobal(QtGui.QCursor.pos()).x() / self.width(), 1) / 2) * 10
            self._rating = width
            self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.underMouse():
            width = (round(self.mapFromGlobal(QtGui.QCursor.pos()).x() / self.width(), 1) / 2) * 10
            self._rating = width
            self.rating = width
            self.update()
            self.RatingChangedSignal.emit(width)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        self._rating = self.rating
        self.update()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        image = QtGui.QImage().scaled(self.width(), self.height())
        image.fill(QtGui.QColor.fromRgb(0, 0, 0, 0))
        painter.drawImage(0, 0, image)
        drawStars(self._rating, painter)
        painter.end()
