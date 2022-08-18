import math

from PySide6 import QtCore, QtGui

from apollo.assets import AppIcons


def drawStars(stars: float, painter: QtGui.QPainter):
    """
    Draws the rating stars

    Args:
        stars (float): rating value
        painter (QtGui.QPainter): parent widgets painter
    """

    def paint_star(star: str, _pos: int, _size: int):
        """
        Paints a star pixmap

        Args:
            star (str): location of the image file
            _pos (int): Position to draw star at
            _size (int): Size of the pixmap
        """
        painter.drawPixmap(QtCore.QPoint(_pos, 6), QtGui.QPixmap.fromImage(QtGui.QImage(star)).scaled(_size, _size))

    painter.save()
    size = 24
    if stars == 0:
        for index, pos in enumerate(range(0, (size - 5) * 5, (size - 5))):
            paint_star(AppIcons.STAR_OUTLINE.secondary, pos, size)
    elif stars == 5:
        for index, pos in enumerate(range(0, (size - 5) * 5, (size - 5))):
            paint_star(AppIcons.STAR.secondary, pos, size)
    else:
        for index, pos in enumerate(range(0, (size - 5) * 5, (size - 5))):
            if math.ceil(stars) == (index + 1):
                paint_star(AppIcons.STAR_HALF.secondary, pos, size)
            elif (index + 1) <= math.floor(stars):
                paint_star(AppIcons.STAR.secondary, pos, size)
            else:
                paint_star(AppIcons.STAR_OUTLINE.secondary, pos, size)
    painter.restore()
