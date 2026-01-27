# -*- coding: utf-8 -*-
import os
import sys

################################################################################
## Form generated from reading UI file 'DataSelectWidget.ui'
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
    QAbstractItemView,
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class Ui_DataSelectWidget(object):
    def setupUi(self, DataSelectWidget):
        if not DataSelectWidget.objectName():
            DataSelectWidget.setObjectName("DataSelectWidget")
        DataSelectWidget.resize(810, 380)
        DataSelectWidget.setMinimumSize(QSize(810, 380))
        icon = QIcon()
        icon_path = "./cratonml_gui/icons/icon.png"
        if getattr(sys, "frozen", False):
            icon_path = os.path.join(sys._MEIPASS, icon_path)
        icon.addFile(
            "{path}".format(path=icon_path), QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        DataSelectWidget.setWindowIcon(icon)
        DataSelectWidget.setStyleSheet("")
        self.verticalLayout_2 = QVBoxLayout(DataSelectWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.DSFrame = QFrame(DataSelectWidget)
        self.DSFrame.setObjectName("DSFrame")
        self.DSFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.DSFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.DSFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.AllDataGB = QGroupBox(self.DSFrame)
        self.AllDataGB.setObjectName("AllDataGB")
        self.horizontalLayout_3 = QHBoxLayout(self.AllDataGB)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.AllDataLW = QListWidget(self.AllDataGB)
        self.AllDataLW.setObjectName("AllDataLW")
        self.AllDataLW.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.AllDataLW.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.AllDataLW.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.AllDataLW.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )

        self.horizontalLayout_3.addWidget(self.AllDataLW)

        self.horizontalLayout_2.addWidget(self.AllDataGB)

        self.BtnsFrame = QFrame(self.DSFrame)
        self.BtnsFrame.setObjectName("BtnsFrame")
        self.BtnsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.BtnsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.BtnsFrame)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_19.addItem(self.verticalSpacer_4)

        self.AddDataBtn = QPushButton(self.BtnsFrame)
        self.AddDataBtn.setObjectName("AddDataBtn")

        self.verticalLayout_19.addWidget(self.AddDataBtn)

        self.ClearDataBtn = QPushButton(self.BtnsFrame)
        self.ClearDataBtn.setObjectName("ClearDataBtn")

        self.verticalLayout_19.addWidget(self.ClearDataBtn)

        self.VisibilityCheckBox = QCheckBox(self.BtnsFrame)
        self.VisibilityCheckBox.setObjectName("VisibilityCheckBox")

        self.verticalLayout_19.addWidget(self.VisibilityCheckBox)

        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_19.addItem(self.verticalSpacer_5)

        self.horizontalLayout_2.addWidget(self.BtnsFrame)

        self.SelectedDataGB = QGroupBox(self.DSFrame)
        self.SelectedDataGB.setObjectName("SelectedDataGB")
        self.horizontalLayout = QHBoxLayout(self.SelectedDataGB)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SelectedDataLW = QListWidget(self.SelectedDataGB)
        self.SelectedDataLW.setObjectName("SelectedDataLW")
        self.SelectedDataLW.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.SelectedDataLW.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.SelectedDataLW.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.SelectedDataLW.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )

        self.horizontalLayout.addWidget(self.SelectedDataLW)

        self.horizontalLayout_2.addWidget(self.SelectedDataGB)

        self.verticalLayout_2.addWidget(self.DSFrame)

        self.ButtonsFrame = QFrame(DataSelectWidget)
        self.ButtonsFrame.setObjectName("ButtonsFrame")
        self.ButtonsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.ButtonsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.ButtonsFrame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.FaciesFrame = QFrame(self.ButtonsFrame)
        self.FaciesFrame.setObjectName("FaciesFrame")
        self.FaciesFrame.setEnabled(True)
        self.FaciesFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.FaciesFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.FaciesFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.FaciesLabel = QLabel(self.FaciesFrame)
        self.FaciesLabel.setObjectName("FaciesLabel")

        self.horizontalLayout_5.addWidget(self.FaciesLabel)

        self.FaciesCB = QComboBox(self.FaciesFrame)
        self.FaciesCB.setObjectName("FaciesCB")

        self.horizontalLayout_5.addWidget(self.FaciesCB)

        self.horizontalLayout_4.addWidget(self.FaciesFrame)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.OkBtn = QPushButton(self.ButtonsFrame)
        self.OkBtn.setObjectName("OkBtn")

        self.horizontalLayout_4.addWidget(self.OkBtn)

        self.CancelBtn = QPushButton(self.ButtonsFrame)
        self.CancelBtn.setObjectName("CancelBtn")

        self.horizontalLayout_4.addWidget(self.CancelBtn)

        self.ApplyBtn = QPushButton(self.ButtonsFrame)
        self.ApplyBtn.setObjectName("ApplyBtn")

        self.horizontalLayout_4.addWidget(self.ApplyBtn)

        self.verticalLayout_2.addWidget(self.ButtonsFrame)

        self.retranslateUi(DataSelectWidget)

        QMetaObject.connectSlotsByName(DataSelectWidget)

    # setupUi

    def retranslateUi(self, DataSelectWidget):
        DataSelectWidget.setWindowTitle(
            QCoreApplication.translate("DataSelectWidget", "Select Data", None)
        )
        self.AllDataGB.setTitle(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u0412\u0445\u043e\u0434\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435",
                None,
            )
        )
        self.AddDataBtn.setText(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c",
                None,
            )
        )
        self.ClearDataBtn.setText(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u041e\u0447\u0438\u0441\u0442\u0438\u0442\u044c",
                None,
            )
        )
        self.VisibilityCheckBox.setText(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u0422\u043e\u043b\u044c\u043a\u043e \u0432\u0438\u0434\u0438\u043c\u044b\u0435",
                None,
            )
        )
        self.SelectedDataGB.setTitle(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435",
                None,
            )
        )
        self.FaciesLabel.setText(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u0421\u0447\u0438\u0442\u0430\u0442\u044c \u043a\u0430\u043a \u0444\u0430\u0446\u0438\u044e",
                None,
            )
        )
        self.OkBtn.setText(
            QCoreApplication.translate("DataSelectWidget", "\u041e\u043a", None)
        )
        self.CancelBtn.setText(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u041e\u0442\u043c\u0435\u043d\u0438\u0442\u044c",
                None,
            )
        )
        self.ApplyBtn.setText(
            QCoreApplication.translate(
                "DataSelectWidget",
                "\u041f\u0440\u0438\u043c\u0435\u043d\u0438\u0442\u044c",
                None,
            )
        )

    # retranslateUi
