# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'WLI_Settings.ui'
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
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Ui_WLISettingsWidget(object):
    def setupUi(self, WLISettingsWidget):
        if not WLISettingsWidget.objectName():
            WLISettingsWidget.setObjectName("WLISettingsWidget")
        WLISettingsWidget.resize(467, 1121)
        WLISettingsWidget.setMinimumSize(QSize(450, 0))
        self.verticalLayout_6 = QVBoxLayout(WLISettingsWidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.SettingsFrame = QFrame(WLISettingsWidget)
        self.SettingsFrame.setObjectName("SettingsFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SettingsFrame.sizePolicy().hasHeightForWidth()
        )
        self.SettingsFrame.setSizePolicy(sizePolicy)
        self.SettingsFrame.setMinimumSize(QSize(440, 0))
        self.SettingsFrame.setMaximumSize(QSize(450, 16777215))
        self.SettingsFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.SettingsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.SettingsFrame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.InputDataScrollArea = QScrollArea(self.SettingsFrame)
        self.InputDataScrollArea.setObjectName("InputDataScrollArea")
        self.InputDataScrollArea.setMinimumSize(QSize(420, 0))
        self.InputDataScrollArea.setMaximumSize(QSize(15000, 16777215))
        self.InputDataScrollArea.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.InputDataScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 410, 1228))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.WellGB = QGroupBox(self.scrollAreaWidgetContents)
        self.WellGB.setObjectName("WellGB")
        self.verticalLayout_14 = QVBoxLayout(self.WellGB)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.WellLW = QListWidget(self.WellGB)
        self.WellLW.setObjectName("WellLW")

        self.verticalLayout_14.addWidget(self.WellLW)

        self.WellBtn = QPushButton(self.WellGB)
        self.WellBtn.setObjectName("WellBtn")

        self.verticalLayout_14.addWidget(self.WellBtn)

        self.verticalLayout_7.addWidget(self.WellGB)

        self.CurveGB = QGroupBox(self.scrollAreaWidgetContents)
        self.CurveGB.setObjectName("CurveGB")
        self.verticalLayout_15 = QVBoxLayout(self.CurveGB)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.CurveLW = QListWidget(self.CurveGB)
        self.CurveLW.setObjectName("CurveLW")

        self.verticalLayout_15.addWidget(self.CurveLW)

        self.CurveBtn = QPushButton(self.CurveGB)
        self.CurveBtn.setObjectName("CurveBtn")

        self.verticalLayout_15.addWidget(self.CurveBtn)

        self.verticalLayout_7.addWidget(self.CurveGB)

        self.StratGB = QGroupBox(self.scrollAreaWidgetContents)
        self.StratGB.setObjectName("StratGB")
        self.StratGB.setMinimumSize(QSize(0, 140))
        self.StratGB.setMaximumSize(QSize(16777215, 140))
        self.StratGB.setFlat(True)
        self.StratGB.setCheckable(True)
        self.StratGB.setChecked(False)
        self.gridLayout_4 = QGridLayout(self.StratGB)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.BotDirectionCB = QComboBox(self.StratGB)
        self.BotDirectionCB.addItem("")
        self.BotDirectionCB.addItem("")
        self.BotDirectionCB.setObjectName("BotDirectionCB")

        self.gridLayout_4.addWidget(self.BotDirectionCB, 3, 2, 1, 1)

        self.TopShiftSB = QSpinBox(self.StratGB)
        self.TopShiftSB.setObjectName("TopShiftSB")
        self.TopShiftSB.setMaximum(1000)

        self.gridLayout_4.addWidget(self.TopShiftSB, 1, 1, 1, 1)

        self.TopDirectionCB = QComboBox(self.StratGB)
        self.TopDirectionCB.addItem("")
        self.TopDirectionCB.addItem("")
        self.TopDirectionCB.setObjectName("TopDirectionCB")

        self.gridLayout_4.addWidget(self.TopDirectionCB, 1, 2, 1, 1)

        self.TopLabel = QLabel(self.StratGB)
        self.TopLabel.setObjectName("TopLabel")

        self.gridLayout_4.addWidget(self.TopLabel, 0, 0, 1, 1)

        self.TopCB = QComboBox(self.StratGB)
        self.TopCB.setObjectName("TopCB")

        self.gridLayout_4.addWidget(self.TopCB, 1, 0, 1, 1)

        self.BotCB = QComboBox(self.StratGB)
        self.BotCB.setObjectName("BotCB")

        self.gridLayout_4.addWidget(self.BotCB, 3, 0, 1, 1)

        self.BotLabel = QLabel(self.StratGB)
        self.BotLabel.setObjectName("BotLabel")

        self.gridLayout_4.addWidget(self.BotLabel, 2, 0, 1, 1)

        self.BotShiftSB = QSpinBox(self.StratGB)
        self.BotShiftSB.setObjectName("BotShiftSB")
        self.BotShiftSB.setMaximum(1000)

        self.gridLayout_4.addWidget(self.BotShiftSB, 3, 1, 1, 1)

        self.TopShiftLabel = QLabel(self.StratGB)
        self.TopShiftLabel.setObjectName("TopShiftLabel")

        self.gridLayout_4.addWidget(self.TopShiftLabel, 0, 1, 1, 1)

        self.BotShiftLabel = QLabel(self.StratGB)
        self.BotShiftLabel.setObjectName("BotShiftLabel")

        self.gridLayout_4.addWidget(self.BotShiftLabel, 2, 1, 1, 1)

        self.TopDirectionLabel = QLabel(self.StratGB)
        self.TopDirectionLabel.setObjectName("TopDirectionLabel")

        self.gridLayout_4.addWidget(self.TopDirectionLabel, 0, 2, 1, 1)

        self.BotDirectionLabel = QLabel(self.StratGB)
        self.BotDirectionLabel.setObjectName("BotDirectionLabel")

        self.gridLayout_4.addWidget(self.BotDirectionLabel, 2, 2, 1, 1)

        self.verticalLayout_7.addWidget(self.StratGB)

        self.MinWidthGB = QGroupBox(self.scrollAreaWidgetContents)
        self.MinWidthGB.setObjectName("MinWidthGB")
        self.horizontalLayout_10 = QHBoxLayout(self.MinWidthGB)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.MinWidthSB = QDoubleSpinBox(self.MinWidthGB)
        self.MinWidthSB.setObjectName("MinWidthSB")
        self.MinWidthSB.setDecimals(1)
        self.MinWidthSB.setMinimum(0.100000000000000)
        self.MinWidthSB.setMaximum(10.000000000000000)
        self.MinWidthSB.setSingleStep(0.100000000000000)
        self.MinWidthSB.setValue(0.500000000000000)

        self.horizontalLayout_10.addWidget(self.MinWidthSB)

        self.verticalLayout_7.addWidget(self.MinWidthGB)

        self.ClusterGB = QGroupBox(self.scrollAreaWidgetContents)
        self.ClusterGB.setObjectName("ClusterGB")
        self.verticalLayout_8 = QVBoxLayout(self.ClusterGB)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.ClusterMethodGB = QGroupBox(self.ClusterGB)
        self.ClusterMethodGB.setObjectName("ClusterMethodGB")
        self.horizontalLayout_5 = QHBoxLayout(self.ClusterMethodGB)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ClusterMethodCB = QComboBox(self.ClusterMethodGB)
        self.ClusterMethodCB.addItem("")
        self.ClusterMethodCB.addItem("")
        self.ClusterMethodCB.addItem("")
        self.ClusterMethodCB.setObjectName("ClusterMethodCB")

        self.horizontalLayout_5.addWidget(self.ClusterMethodCB)

        self.verticalLayout_8.addWidget(self.ClusterMethodGB)

        self.KMeansGB = QGroupBox(self.ClusterGB)
        self.KMeansGB.setObjectName("KMeansGB")
        self.verticalLayout_9 = QVBoxLayout(self.KMeansGB)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.KMeansLabel = QLabel(self.KMeansGB)
        self.KMeansLabel.setObjectName("KMeansLabel")

        self.verticalLayout_9.addWidget(self.KMeansLabel)

        self.KMeansSB = QSpinBox(self.KMeansGB)
        self.KMeansSB.setObjectName("KMeansSB")
        self.KMeansSB.setMinimum(2)
        self.KMeansSB.setMaximum(20)

        self.verticalLayout_9.addWidget(self.KMeansSB)

        self.KMeansCheckBox = QCheckBox(self.KMeansGB)
        self.KMeansCheckBox.setObjectName("KMeansCheckBox")

        self.verticalLayout_9.addWidget(self.KMeansCheckBox)

        self.verticalLayout_8.addWidget(self.KMeansGB)

        self.GaussianMixtureGB = QGroupBox(self.ClusterGB)
        self.GaussianMixtureGB.setObjectName("GaussianMixtureGB")
        self.verticalLayout_10 = QVBoxLayout(self.GaussianMixtureGB)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.GaussianMixtureLabel = QLabel(self.GaussianMixtureGB)
        self.GaussianMixtureLabel.setObjectName("GaussianMixtureLabel")

        self.verticalLayout_10.addWidget(self.GaussianMixtureLabel)

        self.GaussianMixtureSB = QSpinBox(self.GaussianMixtureGB)
        self.GaussianMixtureSB.setObjectName("GaussianMixtureSB")
        self.GaussianMixtureSB.setMinimum(2)
        self.GaussianMixtureSB.setMaximum(20)

        self.verticalLayout_10.addWidget(self.GaussianMixtureSB)

        self.GaussianMixtureCheckBox = QCheckBox(self.GaussianMixtureGB)
        self.GaussianMixtureCheckBox.setObjectName("GaussianMixtureCheckBox")

        self.verticalLayout_10.addWidget(self.GaussianMixtureCheckBox)

        self.verticalLayout_8.addWidget(self.GaussianMixtureGB)

        self.HDBSCANGB = QGroupBox(self.ClusterGB)
        self.HDBSCANGB.setObjectName("HDBSCANGB")
        self.verticalLayout_11 = QVBoxLayout(self.HDBSCANGB)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.HDBSCANMinClusterSizeLabel = QLabel(self.HDBSCANGB)
        self.HDBSCANMinClusterSizeLabel.setObjectName("HDBSCANMinClusterSizeLabel")

        self.verticalLayout_11.addWidget(self.HDBSCANMinClusterSizeLabel)

        self.HDBSCANMinClusterSizeSB = QSpinBox(self.HDBSCANGB)
        self.HDBSCANMinClusterSizeSB.setObjectName("HDBSCANMinClusterSizeSB")
        self.HDBSCANMinClusterSizeSB.setMinimum(3)
        self.HDBSCANMinClusterSizeSB.setMaximum(1000)

        self.verticalLayout_11.addWidget(self.HDBSCANMinClusterSizeSB)

        self.HDBSCANEpsilonLabel = QLabel(self.HDBSCANGB)
        self.HDBSCANEpsilonLabel.setObjectName("HDBSCANEpsilonLabel")

        self.verticalLayout_11.addWidget(self.HDBSCANEpsilonLabel)

        self.HDBSCANEpsilonSB = QDoubleSpinBox(self.HDBSCANGB)
        self.HDBSCANEpsilonSB.setObjectName("HDBSCANEpsilonSB")
        self.HDBSCANEpsilonSB.setSingleStep(0.100000000000000)
        self.HDBSCANEpsilonSB.setValue(0.500000000000000)

        self.verticalLayout_11.addWidget(self.HDBSCANEpsilonSB)

        self.verticalLayout_8.addWidget(self.HDBSCANGB)

        self.verticalLayout_7.addWidget(self.ClusterGB)

        self.PreparerGB = QGroupBox(self.scrollAreaWidgetContents)
        self.PreparerGB.setObjectName("PreparerGB")
        self.PreparerGB.setCheckable(True)
        self.PreparerGB.setChecked(False)
        self.verticalLayout = QVBoxLayout(self.PreparerGB)
        self.verticalLayout.setObjectName("verticalLayout")
        self.NormalizationGB = QGroupBox(self.PreparerGB)
        self.NormalizationGB.setObjectName("NormalizationGB")
        self.NormalizationGB.setCheckable(True)
        self.NormalizationGB.setChecked(False)
        self.verticalLayout_12 = QVBoxLayout(self.NormalizationGB)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.NormalizationCB = QComboBox(self.NormalizationGB)
        self.NormalizationCB.addItem("")
        self.NormalizationCB.addItem("")
        self.NormalizationCB.addItem("")
        self.NormalizationCB.setObjectName("NormalizationCB")

        self.verticalLayout_12.addWidget(self.NormalizationCB)

        self.verticalLayout.addWidget(self.NormalizationGB)

        self.OutliersGB = QGroupBox(self.PreparerGB)
        self.OutliersGB.setObjectName("OutliersGB")
        self.OutliersGB.setCheckable(True)
        self.OutliersGB.setChecked(False)
        self.verticalLayout_18 = QVBoxLayout(self.OutliersGB)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.OutliersCB = QComboBox(self.OutliersGB)
        self.OutliersCB.addItem("")
        self.OutliersCB.addItem("")
        self.OutliersCB.addItem("")
        self.OutliersCB.setObjectName("OutliersCB")

        self.verticalLayout_18.addWidget(self.OutliersCB)

        self.verticalLayout.addWidget(self.OutliersGB)

        self.PCAGB = QGroupBox(self.PreparerGB)
        self.PCAGB.setObjectName("PCAGB")
        self.PCAGB.setFlat(False)
        self.PCAGB.setCheckable(True)
        self.PCAGB.setChecked(False)
        self.verticalLayout_13 = QVBoxLayout(self.PCAGB)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.PCANumbersComponentsLabel = QLabel(self.PCAGB)
        self.PCANumbersComponentsLabel.setObjectName("PCANumbersComponentsLabel")

        self.verticalLayout_13.addWidget(self.PCANumbersComponentsLabel)

        self.PCANumbersComponentsSB = QSpinBox(self.PCAGB)
        self.PCANumbersComponentsSB.setObjectName("PCANumbersComponentsSB")
        self.PCANumbersComponentsSB.setMinimum(2)
        self.PCANumbersComponentsSB.setValue(2)

        self.verticalLayout_13.addWidget(self.PCANumbersComponentsSB)

        self.verticalLayout.addWidget(self.PCAGB)

        self.verticalLayout_7.addWidget(self.PreparerGB)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.InputDataScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_4.addWidget(self.InputDataScrollArea)

        self.StartBtn = QPushButton(self.SettingsFrame)
        self.StartBtn.setObjectName("StartBtn")
        self.StartBtn.setMinimumSize(QSize(0, 0))
        self.StartBtn.setMaximumSize(QSize(15000, 16777215))

        self.verticalLayout_4.addWidget(self.StartBtn)

        self.progressFrame = QFrame(self.SettingsFrame)
        self.progressFrame.setObjectName("progressFrame")
        self.progressFrame.setFrameShape(QFrame.Shape.StyledPanel)
        self.progressFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.progressFrame)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.progressLayout = QHBoxLayout()
        self.progressLayout.setObjectName("progressLayout")
        self.progressBar = QProgressBar(self.progressFrame)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMaximumSize(QSize(115642, 16777215))
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.progressLayout.addWidget(self.progressBar)

        self.gifLabel = QLabel(self.progressFrame)
        self.gifLabel.setObjectName("gifLabel")
        self.gifLabel.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.gifLabel.sizePolicy().hasHeightForWidth())
        self.gifLabel.setSizePolicy(sizePolicy1)
        self.gifLabel.setMinimumSize(QSize(24, 24))
        self.gifLabel.setMaximumSize(QSize(24, 24))

        self.progressLayout.addWidget(self.gifLabel)

        self.verticalLayout_2.addLayout(self.progressLayout)

        self.verticalLayout_4.addWidget(self.progressFrame)

        self.verticalLayout_6.addWidget(self.SettingsFrame)

        self.retranslateUi(WLISettingsWidget)

        QMetaObject.connectSlotsByName(WLISettingsWidget)

    # setupUi

    def retranslateUi(self, WLISettingsWidget):
        WLISettingsWidget.setWindowTitle(
            QCoreApplication.translate("WLISettingsWidget", "Form", None)
        )
        self.WellGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u0421\u043a\u0432\u0430\u0436\u0438\u043d\u044b",
                None,
            )
        )
        self.WellBtn.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c",
                None,
            )
        )
        self.CurveGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget", "\u041a\u0440\u0438\u0432\u044b\u0435", None
            )
        )
        self.CurveBtn.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c",
                None,
            )
        )
        self.StratGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget", "\u041e\u0442\u0431\u0438\u0432\u043a\u0438", None
            )
        )
        self.BotDirectionCB.setItemText(
            0,
            QCoreApplication.translate(
                "WLISettingsWidget", "\u0412\u0432\u0435\u0440\u0445", None
            ),
        )
        self.BotDirectionCB.setItemText(
            1,
            QCoreApplication.translate(
                "WLISettingsWidget", "\u0412\u043d\u0438\u0437", None
            ),
        )

        self.TopDirectionCB.setItemText(
            0,
            QCoreApplication.translate(
                "WLISettingsWidget", "\u0412\u0432\u0435\u0440\u0445", None
            ),
        )
        self.TopDirectionCB.setItemText(
            1,
            QCoreApplication.translate(
                "WLISettingsWidget", "\u0412\u043d\u0438\u0437", None
            ),
        )

        self.TopLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget", "\u041a\u0440\u043e\u0432\u043b\u044f", None
            )
        )
        self.BotLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget", "\u041f\u043e\u0434\u043e\u0448\u0432\u0430", None
            )
        )
        self.TopShiftLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041e\u0442\u0441\u0442\u0443\u043f (\u043c\u0435\u0442\u0440\u044b)",
                None,
            )
        )
        self.BotShiftLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041e\u0442\u0441\u0442\u0443\u043f (\u043c\u0435\u0442\u0440\u044b)",
                None,
            )
        )
        self.TopDirectionLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043e\u0442\u0441\u0442\u0443\u043f\u0430",
                None,
            )
        )
        self.BotDirectionLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043e\u0442\u0441\u0442\u0443\u043f\u0430",
                None,
            )
        )
        self.MinWidthGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u0430\u044f \u0442\u043e\u043b\u0449\u0438\u043d\u0430 \u043f\u0440\u043e\u0441\u043b\u043e\u0439\u043a\u0438, \u043c",
                None,
            )
        )
        self.ClusterGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u0438\u0437\u0430\u0446\u0438\u0438",
                None,
            )
        )
        self.ClusterMethodGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041c\u0435\u0442\u043e\u0434 \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u0438\u0437\u0430\u0446\u0438\u0438",
                None,
            )
        )
        self.ClusterMethodCB.setItemText(
            0, QCoreApplication.translate("WLISettingsWidget", "KMeans", None)
        )
        self.ClusterMethodCB.setItemText(
            1, QCoreApplication.translate("WLISettingsWidget", "GaussianMixture", None)
        )
        self.ClusterMethodCB.setItemText(
            2, QCoreApplication.translate("WLISettingsWidget", "HDBSCAN", None)
        )

        self.KMeansGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0430\u043b\u0433\u043e\u0440\u0438\u0442\u043c\u0430",
                None,
            )
        )
        self.KMeansLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u043e\u0432",
                None,
            )
        )
        self.KMeansCheckBox.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u043f\u043e\u0434\u0431\u043e\u0440",
                None,
            )
        )
        self.GaussianMixtureGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0430\u043b\u0433\u043e\u0440\u0438\u0442\u043c\u0430",
                None,
            )
        )
        self.GaussianMixtureLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442",
                None,
            )
        )
        self.GaussianMixtureCheckBox.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u0410\u0432\u0442\u043e\u043c\u0430\u0442\u0438\u0447\u0435\u0441\u043a\u0438\u0439 \u043f\u043e\u0434\u0431\u043e\u0440",
                None,
            )
        )
        self.HDBSCANGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b \u0430\u043b\u0433\u043e\u0440\u0438\u0442\u043c\u0430",
                None,
            )
        )
        self.HDBSCANMinClusterSizeLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u044b\u0439 \u0440\u0430\u0437\u043c\u0435\u0440 \u043a\u043b\u0430\u0441\u0442\u0435\u0440\u0430",
                None,
            )
        )
        self.HDBSCANEpsilonLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u0440\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435",
                None,
            )
        )
        self.PreparerGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0435 \u043f\u0430\u0440\u0430\u043c\u0435\u0442\u0440\u044b",
                None,
            )
        )
        self.NormalizationGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041d\u043e\u0440\u043c\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f",
                None,
            )
        )
        self.NormalizationCB.setItemText(
            0, QCoreApplication.translate("WLISettingsWidget", "MaxAbs", None)
        )
        self.NormalizationCB.setItemText(
            1, QCoreApplication.translate("WLISettingsWidget", "MinMax", None)
        )
        self.NormalizationCB.setItemText(
            2, QCoreApplication.translate("WLISettingsWidget", "Z-norm", None)
        )

        self.OutliersGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u0423\u0434\u0430\u043b\u0435\u043d\u0438\u0435 \u0432\u044b\u0431\u0440\u043e\u0441\u043e\u0432",
                None,
            )
        )
        self.OutliersCB.setItemText(
            0, QCoreApplication.translate("WLISettingsWidget", "LOF", None)
        )
        self.OutliersCB.setItemText(
            1, QCoreApplication.translate("WLISettingsWidget", "IsolationForest", None)
        )
        self.OutliersCB.setItemText(
            2, QCoreApplication.translate("WLISettingsWidget", "EllipticEnvelope", None)
        )

        self.PCAGB.setTitle(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041f\u043e\u043d\u0438\u0436\u0435\u043d\u0438\u0435 \u0440\u0430\u0437\u043c\u0435\u0440\u043d\u043e\u0441\u0442\u0438",
                None,
            )
        )
        self.PCANumbersComponentsLabel.setText(
            QCoreApplication.translate(
                "WLISettingsWidget",
                "\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u043e\u043c\u043f\u043e\u043d\u0435\u043d\u0442",
                None,
            )
        )
        self.StartBtn.setText(
            QCoreApplication.translate(
                "WLISettingsWidget", "\u0417\u0430\u043f\u0443\u0441\u043a", None
            )
        )
        self.gifLabel.setText("")

    # retranslateUi
