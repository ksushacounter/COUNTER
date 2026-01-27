# -*- coding: utf-8 -*-
import os
import sys

################################################################################
## Form generated from reading UI file 'MessageWidget.ui'
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
    QFrame,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_MessageWidget(object):
    def setupUi(self, MessageWidget):
        if not MessageWidget.objectName():
            MessageWidget.setObjectName("MessageWidget")
        MessageWidget.resize(810, 380)
        MessageWidget.setMinimumSize(QSize(810, 380))
        icon = QIcon()
        icon_path = "./cratonml_gui/icons/icon.png"
        if getattr(sys, "frozen", False):
            icon_path = os.path.join(sys._MEIPASS, icon_path)
        icon.addFile(
            "{path}".format(path=icon_path), QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        MessageWidget.setWindowIcon(icon)
        MessageWidget.setStyleSheet("")
        self.verticalLayout_2 = QVBoxLayout(MessageWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.MFrame = QFrame(MessageWidget)
        self.MFrame.setObjectName("MFrame")
        self.MFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.MFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.MFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MessageTextEdit = QTextEdit(self.MFrame)
        self.MessageTextEdit.setObjectName("MessageTextEdit")
        self.MessageTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.MessageTextEdit)

        self.verticalLayout_2.addWidget(self.MFrame)

        self.retranslateUi(MessageWidget)

        QMetaObject.connectSlotsByName(MessageWidget)

    # setupUi

    def retranslateUi(self, MessageWidget):
        MessageWidget.setWindowTitle(
            QCoreApplication.translate(
                "MessageWidget",
                "\u0416\u0443\u0440\u043d\u0430\u043b \u0441\u043e\u0431\u044b\u0442\u0438\u0439",
                None,
            )
        )

    # retranslateUi
