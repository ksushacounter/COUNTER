# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabWithSave.ui'
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
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_TabWithSaveWidget(object):
    def setupUi(self, TabWithSaveWidget):
        if not TabWithSaveWidget.objectName():
            TabWithSaveWidget.setObjectName("TabWithSaveWidget")
        TabWithSaveWidget.resize(1057, 734)
        self.verticalLayout = QVBoxLayout(TabWithSaveWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.PlotFrame = QFrame(TabWithSaveWidget)
        self.PlotFrame.setObjectName("PlotFrame")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlotFrame.sizePolicy().hasHeightForWidth())
        self.PlotFrame.setSizePolicy(sizePolicy)
        self.PlotFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.PlotFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.PlotFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.PlotLayout = QVBoxLayout()
        self.PlotLayout.setObjectName("PlotLayout")

        self.verticalLayout_4.addLayout(self.PlotLayout)

        self.verticalLayout.addWidget(self.PlotFrame)

        self.SaveFrame = QFrame(TabWithSaveWidget)
        self.SaveFrame.setObjectName("SaveFrame")
        self.SaveFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.SaveFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.SaveFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SaveNameLabel = QLabel(self.SaveFrame)
        self.SaveNameLabel.setObjectName("SaveNameLabel")

        self.horizontalLayout.addWidget(self.SaveNameLabel)

        self.SaveNameLE = QLineEdit(self.SaveFrame)
        self.SaveNameLE.setObjectName("SaveNameLE")

        self.horizontalLayout.addWidget(self.SaveNameLE)

        self.SaveMapBtn = QPushButton(self.SaveFrame)
        self.SaveMapBtn.setObjectName("SaveMapBtn")

        self.horizontalLayout.addWidget(self.SaveMapBtn)

        self.verticalLayout.addWidget(self.SaveFrame)

        self.retranslateUi(TabWithSaveWidget)

        QMetaObject.connectSlotsByName(TabWithSaveWidget)

    # setupUi

    def retranslateUi(self, TabWithSaveWidget):
        TabWithSaveWidget.setWindowTitle(
            QCoreApplication.translate("TabWithSaveWidget", "Form", None)
        )
        self.SaveNameLabel.setText(
            QCoreApplication.translate(
                "TabWithSaveWidget",
                "\u0418\u043c\u044f \u0434\u043b\u044f \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f",
                None,
            )
        )
        self.SaveNameLE.setText(
            QCoreApplication.translate("TabWithSaveWidget", "Test", None)
        )
        self.SaveMapBtn.setText(
            QCoreApplication.translate(
                "TabWithSaveWidget",
                "\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c",
                None,
            )
        )

    # retranslateUi
