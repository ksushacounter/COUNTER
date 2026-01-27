# -*- coding: utf-8 -*-
import os
import sys

################################################################################
## Form generated from reading UI file 'Main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class Ui_Main(object):
    def setupUi(self, Main):
        if not Main.objectName():
            Main.setObjectName("Main")
        Main.resize(1720, 842)
        Main.setMinimumSize(QSize(1720, 790))
        icon = QIcon()
        icon_path = "./cratonml_gui/icons/icon.png"
        if getattr(sys, "frozen", False):
            icon_path = os.path.join(sys._MEIPASS, icon_path)
        icon.addFile(
            "{path}".format(path=icon_path), QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        Main.setWindowIcon(icon)
        Main.setStyleSheet("")
        self.verticalLayout = QVBoxLayout(Main)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MainLayout = QVBoxLayout()
        self.MainLayout.setObjectName("MainLayout")
        self.MainTabWidget = QTabWidget(Main)
        self.MainTabWidget.setObjectName("MainTabWidget")
        self.MainTabWidget.setMinimumSize(QSize(1153, 730))

        self.MainLayout.addWidget(self.MainTabWidget)

        self.verticalLayout.addLayout(self.MainLayout)

        self.ThemeLayout = QHBoxLayout()
        self.ThemeLayout.setObjectName("ThemeLayout")
        self.label = QLabel(Main)
        self.label.setObjectName("label")
        self.label.setMinimumSize(QSize(60, 0))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ThemeLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.ThemeLayout.addItem(self.horizontalSpacer)

        self.UpdateBtn = QPushButton(Main)
        self.UpdateBtn.setObjectName("UpdateBtn")

        self.ThemeLayout.addWidget(self.UpdateBtn)

        self.verticalLayout.addLayout(self.ThemeLayout)

        self.retranslateUi(Main)

        self.MainTabWidget.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(Main)

    # setupUi

    def retranslateUi(self, Main):
        Main.setWindowTitle(QCoreApplication.translate("Main", "MLToolBox", None))
        self.label.setText(
            QCoreApplication.translate(
                "Main", "\u0412\u0435\u0440\u0441\u0438\u044f 1.5.0.2", None
            )
        )
        self.UpdateBtn.setText(
            QCoreApplication.translate(
                "Main", "\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None
            )
        )

    # retranslateUi
