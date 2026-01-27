# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TabMain.ui'
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
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_TabMainWidget(object):
    def setupUi(self, TabMainWidget):
        if not TabMainWidget.objectName():
            TabMainWidget.setObjectName("TabMainWidget")
        TabMainWidget.resize(1654, 1154)
        TabMainWidget.setMinimumSize(QSize(1520, 0))
        self.verticalLayout_6 = QVBoxLayout(TabMainWidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.TabMainFrame = QFrame(TabMainWidget)
        self.TabMainFrame.setObjectName("TabMainFrame")
        self.TabMainFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.horizontalLayout_2 = QHBoxLayout(self.TabMainFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.SettingsFrame = QGroupBox(self.TabMainFrame)
        self.SettingsFrame.setObjectName("SettingsFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SettingsFrame.sizePolicy().hasHeightForWidth()
        )
        self.SettingsFrame.setSizePolicy(sizePolicy)
        self.SettingsFrame.setMinimumSize(QSize(450, 0))
        self.SettingsFrame.setMaximumSize(QSize(450, 16777215))
        self.settingsLayout = QVBoxLayout(self.SettingsFrame)
        self.settingsLayout.setSpacing(1)
        self.settingsLayout.setObjectName("settingsLayout")
        self.settingsLayout.setContentsMargins(1, 1, 1, 1)
        self.SettingsLayout = QVBoxLayout()
        self.SettingsLayout.setSpacing(0)
        self.SettingsLayout.setObjectName("SettingsLayout")

        self.settingsLayout.addLayout(self.SettingsLayout)

        self.horizontalLayout_2.addWidget(self.SettingsFrame)

        self.InputDataHideBtn = QPushButton(self.TabMainFrame)
        self.InputDataHideBtn.setObjectName("InputDataHideBtn")
        self.InputDataHideBtn.setMinimumSize(QSize(0, 100))
        self.InputDataHideBtn.setMaximumSize(QSize(10, 16777215))

        self.horizontalLayout_2.addWidget(self.InputDataHideBtn)

        self.VisualizationFrame = QFrame(self.TabMainFrame)
        self.VisualizationFrame.setObjectName("VisualizationFrame")
        self.VisualizationFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.VisualizationFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.VisualizationFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.PlotFrame = QFrame(self.VisualizationFrame)
        self.PlotFrame.setObjectName("PlotFrame")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.PlotFrame.sizePolicy().hasHeightForWidth())
        self.PlotFrame.setSizePolicy(sizePolicy1)
        self.PlotFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.PlotFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.PlotFrame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.PlotLayout = QGridLayout()
        self.PlotLayout.setObjectName("PlotLayout")

        self.horizontalLayout_3.addLayout(self.PlotLayout)

        self.verticalLayout_4.addWidget(self.PlotFrame)

        self.MessageFrame = QFrame(self.VisualizationFrame)
        self.MessageFrame.setObjectName("MessageFrame")
        self.MessageFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.MessageFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.MessageFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MessageLineEdit = QLineEdit(self.MessageFrame)
        self.MessageLineEdit.setObjectName("MessageLineEdit")
        self.MessageLineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.MessageLineEdit)

        self.OpenMessageWidgetBtn = QPushButton(self.MessageFrame)
        self.OpenMessageWidgetBtn.setObjectName("OpenMessageWidgetBtn")

        self.horizontalLayout.addWidget(self.OpenMessageWidgetBtn)

        self.verticalLayout_4.addWidget(self.MessageFrame)

        self.horizontalLayout_2.addWidget(self.VisualizationFrame)

        self.verticalLayout_6.addWidget(self.TabMainFrame)

        self.retranslateUi(TabMainWidget)

        QMetaObject.connectSlotsByName(TabMainWidget)

    # setupUi

    def retranslateUi(self, TabMainWidget):
        TabMainWidget.setWindowTitle(
            QCoreApplication.translate("TabMainWidget", "Form", None)
        )
        self.SettingsFrame.setTitle(
            QCoreApplication.translate(
                "TabMainWidget",
                "\u0412\u0445\u043e\u0434\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435",
                None,
            )
        )
        self.InputDataHideBtn.setText("")
        self.OpenMessageWidgetBtn.setText(
            QCoreApplication.translate(
                "TabMainWidget",
                "\u0416\u0443\u0440\u043d\u0430\u043b \u0441\u043e\u0431\u044b\u0442\u0438\u0439",
                None,
            )
        )

    # retranslateUi
