# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'temp.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TrackDelegate_Mid_Frame = QFrame(self.centralwidget)
        self.TrackDelegate_Mid_Frame.setObjectName("TrackDelegate_Mid_Frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TrackDelegate_Mid_Frame.sizePolicy().hasHeightForWidth())
        self.TrackDelegate_Mid_Frame.setSizePolicy(sizePolicy)
        self.TrackDelegate_Mid_Frame.setMinimumSize(QSize(0, 72))
        self.TrackDelegate_Mid_Frame.setMaximumSize(QSize(16777215, 72))
        self.TrackDelegate_Mid_Frame.setFrameShape(QFrame.StyledPanel)
        self.TrackDelegate_Mid_Frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.TrackDelegate_Mid_Frame)
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.TrackDelegate_Mid_Cover_pixmap = QLabel(self.TrackDelegate_Mid_Frame)
        self.TrackDelegate_Mid_Cover_pixmap.setObjectName("TrackDelegate_Mid_Cover_pixmap")
        self.TrackDelegate_Mid_Cover_pixmap.setMinimumSize(QSize(64, 64))
        self.TrackDelegate_Mid_Cover_pixmap.setMaximumSize(QSize(64, 64))
        self.TrackDelegate_Mid_Cover_pixmap.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.TrackDelegate_Mid_Cover_pixmap)

        self.frame_2 = QFrame(self.TrackDelegate_Mid_Frame)
        self.frame_2.setObjectName("frame_2")
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QFrame.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.TrackDelegate_Mid_title_label = QLabel(self.frame_2)
        self.TrackDelegate_Mid_title_label.setObjectName("TrackDelegate_Mid_title_label")
        sizePolicy.setHeightForWidth(
            self.TrackDelegate_Mid_title_label.sizePolicy().hasHeightForWidth()
        )
        self.TrackDelegate_Mid_title_label.setSizePolicy(sizePolicy)
        self.TrackDelegate_Mid_title_label.setMinimumSize(QSize(0, 24))
        self.TrackDelegate_Mid_title_label.setMaximumSize(QSize(16777215, 24))
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(8)
        font.setBold(False)
        self.TrackDelegate_Mid_title_label.setFont(font)

        self.gridLayout.addWidget(self.TrackDelegate_Mid_title_label, 0, 0, 1, 1)

        self.TrackDelegate_Mid_album_label = QLabel(self.frame_2)
        self.TrackDelegate_Mid_album_label.setObjectName("TrackDelegate_Mid_album_label")
        sizePolicy.setHeightForWidth(
            self.TrackDelegate_Mid_album_label.sizePolicy().hasHeightForWidth()
        )
        self.TrackDelegate_Mid_album_label.setSizePolicy(sizePolicy)
        self.TrackDelegate_Mid_album_label.setMinimumSize(QSize(0, 24))
        self.TrackDelegate_Mid_album_label.setMaximumSize(QSize(16777215, 24))
        self.TrackDelegate_Mid_album_label.setFont(font)

        self.gridLayout.addWidget(self.TrackDelegate_Mid_album_label, 0, 1, 1, 1)

        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName("frame_3")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_3)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.TrackDelegate_Mid_artist_label = QLabel(self.frame_3)
        self.TrackDelegate_Mid_artist_label.setObjectName("TrackDelegate_Mid_artist_label")
        sizePolicy1.setHeightForWidth(
            self.TrackDelegate_Mid_artist_label.sizePolicy().hasHeightForWidth()
        )
        self.TrackDelegate_Mid_artist_label.setSizePolicy(sizePolicy1)
        self.TrackDelegate_Mid_artist_label.setFont(font)

        self.gridLayout_2.addWidget(self.TrackDelegate_Mid_artist_label, 0, 0, 1, 3)

        self.TrackDelegate_Mid_misc3_label = QLabel(self.frame_3)
        self.TrackDelegate_Mid_misc3_label.setObjectName("TrackDelegate_Mid_misc3_label")
        self.TrackDelegate_Mid_misc3_label.setMinimumSize(QSize(0, 0))
        self.TrackDelegate_Mid_misc3_label.setMaximumSize(QSize(16777215, 16777215))
        self.TrackDelegate_Mid_misc3_label.setFont(font)

        self.gridLayout_2.addWidget(self.TrackDelegate_Mid_misc3_label, 1, 2, 1, 1)

        self.TrackDelegate_Mid_misc2_label = QLabel(self.frame_3)
        self.TrackDelegate_Mid_misc2_label.setObjectName("TrackDelegate_Mid_misc2_label")
        self.TrackDelegate_Mid_misc2_label.setMinimumSize(QSize(0, 0))
        self.TrackDelegate_Mid_misc2_label.setMaximumSize(QSize(16777215, 16777215))
        self.TrackDelegate_Mid_misc2_label.setFont(font)

        self.gridLayout_2.addWidget(self.TrackDelegate_Mid_misc2_label, 1, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 3, 1, 1)

        self.TrackDelegate_Mid_misc1_label = QLabel(self.frame_3)
        self.TrackDelegate_Mid_misc1_label.setObjectName("TrackDelegate_Mid_misc1_label")
        self.TrackDelegate_Mid_misc1_label.setMinimumSize(QSize(0, 0))
        self.TrackDelegate_Mid_misc1_label.setMaximumSize(QSize(16777215, 16777215))
        self.TrackDelegate_Mid_misc1_label.setFont(font)

        self.gridLayout_2.addWidget(self.TrackDelegate_Mid_misc1_label, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 2, 0, 1, 4)

        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 1, 1, 1, 1)

        self.horizontalLayout_2.addWidget(self.frame_2)

        self.TrackDelegate_Mid_isLiked_pixmap = QLabel(self.TrackDelegate_Mid_Frame)
        self.TrackDelegate_Mid_isLiked_pixmap.setObjectName("TrackDelegate_Mid_isLiked_pixmap")
        self.TrackDelegate_Mid_isLiked_pixmap.setMinimumSize(QSize(32, 0))
        self.TrackDelegate_Mid_isLiked_pixmap.setMaximumSize(QSize(32, 16777215))

        self.horizontalLayout_2.addWidget(self.TrackDelegate_Mid_isLiked_pixmap)

        self.TrackDelegate_Mid_time_label = QLabel(self.TrackDelegate_Mid_Frame)
        self.TrackDelegate_Mid_time_label.setObjectName("TrackDelegate_Mid_time_label")
        self.TrackDelegate_Mid_time_label.setMinimumSize(QSize(64, 0))
        self.TrackDelegate_Mid_time_label.setMaximumSize(QSize(64, 16777215))
        self.TrackDelegate_Mid_time_label.setFont(font)
        self.TrackDelegate_Mid_time_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.TrackDelegate_Mid_time_label)

        self.verticalLayout.addWidget(self.TrackDelegate_Mid_Frame)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.TrackDelegate_Mid_Cover_pixmap.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_title_label.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_album_label.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_artist_label.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_misc3_label.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_misc2_label.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_misc1_label.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_isLiked_pixmap.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.TrackDelegate_Mid_time_label.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )

    # retranslateUi
