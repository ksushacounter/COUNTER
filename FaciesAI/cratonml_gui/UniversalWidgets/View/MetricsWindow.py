import numpy as np
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QLabel, QTableWidgetItem, QTableWidget, QAbstractItemView
from cratonml.calculate.Statistics import confusion_matrix
from cratonml.calculate.metrics import feature_importance, k_fold, calculate_metrics
from pyqtgraph import colormap

from cratonml_gui.UniversalWidgets.View.TableWindow import TableWindow

NUMBER_OF_COLORS = 101
FONT_SIZE = 11


class MetricsWindow(TableWindow):
    def __init__(
        self,
        train_data,
        train_labels,
        model,
        test_data,
        true_labels,
        predict_labels,
        attribute_names,
    ):
        super(MetricsWindow, self).__init__()
        self.train_data = train_data
        self.train_labels = train_labels
        self.model = model
        self.test_data = test_data
        self.true_labels = true_labels
        self.predict_labels = predict_labels
        self.attribute_names = attribute_names

        self.font = QFont()
        self.font.setBold(True)

        self.__show_table()

    def __create_table_widget(self):
        """Создает виджет таблицу"""

        self.add_confusion_matrix_table()
        self.add_metrics_table()
        self.add_kfold_table()
        self.add_feature_importance_table()

    def add_confusion_matrix_table(self):
        matrix, self.uniq_labels = confusion_matrix(
            true_labels=self.true_labels, predict_labels=self.predict_labels
        )
        headers = self.uniq_labels.astype(int).astype(str)
        ncols = len(headers)
        nrows = ncols
        self.confusion_matrix_table = QTableWidget(rowCount=nrows, columnCount=ncols)
        self.confusion_matrix_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.confusion_matrix_table.setHorizontalHeaderLabels(headers)
        self.confusion_matrix_table.setVerticalHeaderLabels(headers)

        for row in range(self.confusion_matrix_table.rowCount()):
            for col in range(self.confusion_matrix_table.columnCount()):
                value = matrix[row][col]
                item = QTableWidgetItem(str(value))
                if not np.isnan(value):
                    color = self.colors[
                        int(value * (NUMBER_OF_COLORS - 1) / np.sum(matrix))
                    ]
                    item.setBackground(QColor(color[0], color[1], color[2]))
                    item.setFont(self.font)
                    if sum(color) < 255:
                        item.setForeground(QColor("white"))
                    else:
                        item.setForeground(QColor("black"))
                self.confusion_matrix_table.setItem(row, col, item)

        self.set_columns_width(self.confusion_matrix_table, headers)

    def add_metrics_table(self):
        vert_headers = self.uniq_labels.astype(int).astype(str)
        hor_headers = ["precision", "recall", "accuracy", "f1"]
        metrics = calculate_metrics(y_true=self.true_labels, y_pred=self.predict_labels)
        metrics = np.array(
            [
                np.round(metrics[0], 3),
                np.round(metrics[1], 3),
                np.round(metrics[2], 3),
                metrics[3].astype(int),
            ]
        ).T
        ncols = len(hor_headers)
        nrows = len(vert_headers)
        self.metrics_table = QTableWidget(rowCount=nrows, columnCount=ncols)
        self.metrics_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.metrics_table.setHorizontalHeaderLabels(hor_headers)
        self.metrics_table.setVerticalHeaderLabels(vert_headers)

        for row in range(self.metrics_table.rowCount()):
            for col in range(self.metrics_table.columnCount()):
                value = metrics[row][col]
                item = QTableWidgetItem(str(value))
                if not np.isnan(value):
                    if col == 3:
                        color = self.colors[
                            int(value * (NUMBER_OF_COLORS - 1) / len(self.true_labels))
                        ]
                    else:
                        color = self.colors[int(value * (NUMBER_OF_COLORS - 1))]
                    item.setBackground(QColor(color[0], color[1], color[2]))
                    item.setFont(self.font)
                    if sum(color) < 255:
                        item.setForeground(QColor("white"))
                    else:
                        item.setForeground(QColor("black"))
                self.metrics_table.setItem(row, col, item)

        self.set_columns_width(self.metrics_table, hor_headers)

    def add_kfold_table(self):
        precision, recall, accuracy, f1 = k_fold(
            y_train=self.train_labels, x_train=self.train_data, model=self.model
        )
        metrics = np.empty((len(precision) + 1, 4))
        metrics[:-1, 0] = precision
        metrics[:-1, 1] = recall
        metrics[:-1, 2] = accuracy
        metrics[:-1, 3] = f1
        metrics[-1, 0] = precision.mean()
        metrics[-1, 1] = recall.mean()
        metrics[-1, 2] = accuracy.mean()
        metrics[-1, 3] = f1.mean()
        metrics = np.round(metrics, 3)
        vert_headers = np.arange(len(metrics)).astype(str)
        vert_headers[-1] = "mean"

        hor_headers = ["precision", "recall", "accuracy", "f1"]
        ncols = len(hor_headers)
        nrows = len(vert_headers)
        self.kfold_table = QTableWidget(rowCount=nrows, columnCount=ncols)
        self.kfold_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.kfold_table.setHorizontalHeaderLabels(hor_headers)
        self.kfold_table.setVerticalHeaderLabels(vert_headers)

        for row in range(self.kfold_table.rowCount()):
            for col in range(self.kfold_table.columnCount()):
                value = metrics[row][col]
                item = QTableWidgetItem(str(value))
                if not np.isnan(value):
                    color = self.colors[int(value * (NUMBER_OF_COLORS - 1))]
                    item.setBackground(QColor(color[0], color[1], color[2]))
                    item.setFont(self.font)
                    if sum(color) < 255:
                        item.setForeground(QColor("white"))
                    else:
                        item.setForeground(QColor("black"))
                self.kfold_table.setItem(row, col, item)

        self.set_columns_width(self.kfold_table, hor_headers)

    def add_feature_importance_table(self):
        importances = feature_importance(
            model=self.model, x_test=self.test_data, y_test=self.true_labels
        )
        sorted_indices = sorted(
            range(len(importances)), key=lambda k: importances[k], reverse=True
        )
        vert_headers = [self.attribute_names[i] for i in sorted_indices]
        sorted_importances = np.array(
            [round(importances[i], 3) for i in sorted_indices]
        ).T.reshape(-1, 1)
        hor_headers = ["feature importanse"]

        ncols = len(hor_headers)
        nrows = len(vert_headers)
        self.feature_importance_table = QTableWidget(rowCount=nrows, columnCount=ncols)
        self.feature_importance_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.feature_importance_table.setHorizontalHeaderLabels(hor_headers)
        self.feature_importance_table.setVerticalHeaderLabels(vert_headers)

        for row in range(self.feature_importance_table.rowCount()):
            for col in range(self.feature_importance_table.columnCount()):
                value = sorted_importances[row][col]
                item = QTableWidgetItem(str(value))
                item.setFont(self.font)
                if not np.isnan(value) and np.nansum(sorted_importances) != 0:
                    color = self.colors[
                        int(
                            value
                            * (NUMBER_OF_COLORS - 1)
                            / np.nansum(sorted_importances)
                        )
                    ]
                    item.setBackground(QColor(color[0], color[1], color[2]))
                    if sum(color) < 255:
                        item.setForeground(QColor("white"))
                    else:
                        item.setForeground(QColor("black"))
                self.feature_importance_table.setItem(row, col, item)

        self.set_columns_width(self.feature_importance_table, hor_headers)

    def __show_table(self):
        cmap = colormap.getFromMatplotlib("Blues")
        self.colors = cmap.getLookupTable(nPts=NUMBER_OF_COLORS)
        self.__create_table_widget()

        self.font = QFont()
        self.font.setPointSize(FONT_SIZE)

        label = QLabel("Матрица ошибок")
        label.setFont(self.font)
        self.layout.addWidget(label, 0, 0)
        self.layout.addWidget(self.confusion_matrix_table, 1, 0)
        label = QLabel("Метрики")
        label.setFont(self.font)
        self.layout.addWidget(label, 0, 1)
        self.layout.addWidget(self.metrics_table, 1, 1)
        label = QLabel("Кросс-валидация")
        label.setFont(self.font)
        self.layout.addWidget(label, 2, 0)
        self.layout.addWidget(self.kfold_table, 3, 0)
        label = QLabel("Влияние признаков")
        label.setFont(self.font)
        self.layout.addWidget(label, 2, 1)
        self.layout.addWidget(self.feature_importance_table, 3, 1)
        self.setLayout(self.layout)
