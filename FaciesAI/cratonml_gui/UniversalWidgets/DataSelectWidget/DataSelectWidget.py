import logging

from PySide6.QtWidgets import QWidget

from cratonml_gui.Themes.DarkTheme import DarkThemeStylesheet
from cratonml_gui.Themes.LightTheme import LightThemeStylesheet
from cratonml_gui.UniversalWidgets.DataSelectWidget.DataSelectWidget_ui import (
    Ui_DataSelectWidget,
)

logger = logging.getLogger("__name__")


class DataSelectWidget(QWidget):
    def __init__(
        self,
        widget=None,
        sorting=None,
        title="DataSelectWidget",
        signal=None,
        hide_facies_frame=True,
    ):
        super(DataSelectWidget, self).__init__()

        self.widget = widget
        self.sorting = sorting
        self.signal = signal
        self.hide_facies_frame = hide_facies_frame
        self.prev_data = []

        self.isDropToSelected = False
        self.isDropToInput = False
        self.count_drop_items = 0

        self.ui = Ui_DataSelectWidget()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        if hide_facies_frame:
            self.ui.FaciesFrame.hide()
        else:
            self.ui.ApplyBtn.setText("Объединить")

        self.__create_callbacks()

    def update_style_sheet(self, is_light_theme):
        if is_light_theme:
            stylesheet = LightThemeStylesheet().stylesheet
        else:
            stylesheet = DarkThemeStylesheet().stylesheet

        self.setStyleSheet(stylesheet)

    def __create_callbacks(self):
        """Задает реакции на нажатие кнопок"""

        self.ui.OkBtn.clicked.connect(self.__ok_data)
        self.ui.CancelBtn.clicked.connect(self.__cancel_data)
        self.ui.ApplyBtn.clicked.connect(self.apply_data)

    def apply_data(self):
        """Меняет данные в списке (widget) на данные из списка выбранных."""

        try:
            if self.hide_facies_frame:
                selected_data = [
                    self.ui.SelectedDataLW.item(x).text()
                    for x in range(self.ui.SelectedDataLW.count())
                ]
                if self.widget is not None:
                    self.widget.clear()
                    self.widget.addItems(selected_data)
                    if len(selected_data) == 0 and self.signal is not None:
                        self.signal.emit()
                self.prev_data = selected_data
            else:
                self.prev_data = []
        except Exception as e:
            logger.error(e, exc_info=True)

    def delete_data(self):
        """Меняет данные в списке (widget) на предыдущие данные, которые есть в списке выбранных."""

        selected_data = [
            self.ui.SelectedDataLW.item(x).text()
            for x in range(self.ui.SelectedDataLW.count())
        ]
        selected_data = [x for x in self.prev_data if x in selected_data]
        if self.widget is not None:
            self.widget.clear()
            self.widget.addItems(selected_data)
        self.prev_data = selected_data

    def __ok_data(self):
        """Меняет данные в списке (widget) на данные из списка выбранных. Закрывает окно."""

        try:
            self.apply_data()
            self.close()
        except Exception as e:
            logger.error(e, exc_info=True)

    def __cancel_data(self):
        """Возвращает данные в предыдущее состояние."""

        try:
            self.ui.SelectedDataLW.clear()
            self.ui.SelectedDataLW.addItems(self.prev_data)
            self.close()
        except Exception as e:
            logger.error(e, exc_info=True)

    def closeEvent(self, event):
        """
        Функция, которая вызывается при закрытии окна.
        Если данные обновились, то возвращает их в предыдущее состояние.
        """

        try:
            selected_data = [
                self.ui.SelectedDataLW.item(x).text()
                for x in range(self.ui.SelectedDataLW.count())
            ]
            if self.prev_data == selected_data:
                event.accept()
            else:
                event.ignore()
                self.__cancel_data()
        except Exception as e:
            logger.error(e, exc_info=True)

    def move_data_to_selected_lw(self, data):

        all_data = [
            self.ui.AllDataLW.item(x).text() for x in range(self.ui.AllDataLW.count())
        ]
        for item in data:
            if item in all_data:
                ind = all_data.index(item)
                self.ui.AllDataLW.takeItem(ind)
                self.ui.SelectedDataLW.addItem(item)
        self.prev_data = [
            self.ui.SelectedDataLW.item(x).text()
            for x in range(self.ui.SelectedDataLW.count())
        ]
        self.__sort()

    def open_data_select_widget(
        self, all_data, selected_data, sort=False, is_light_theme=True
    ):
        """
        Открывает окно выбора данных и заполняет списки.
        Задает реакции на нажатие кнопок и перетаскивание объектов.
        """

        self.update_style_sheet(is_light_theme)
        self.ui.VisibilityCheckBox.hide()

        self.ui.AddDataBtn.clicked.connect(self.__add_data_to_selected_lw)
        self.ui.ClearDataBtn.clicked.connect(self.__clear_data_in_selected_lw)
        self.ui.AllDataLW.itemChanged.connect(self.__drop_data_to_input_lw)
        self.ui.SelectedDataLW.itemChanged.connect(self.__drop_data_to_selected_lw)

        if sort:
            if self.widget is not None:
                self.widget.setSortingEnabled(True)
            self.ui.AllDataLW.setSortingEnabled(True)
            self.ui.SelectedDataLW.setSortingEnabled(True)

        self.ui.SelectedDataLW.addItems(selected_data)
        self.add_data_to_input_lw(all_data=all_data)
        self.prev_data = selected_data
        self.show()

    def add_data_to_input_lw(self, all_data):
        """Обновляет список доступных элементов. Добавляет туда элементы, которых нет в списке выбранных."""

        selected_data = [
            self.ui.SelectedDataLW.item(x).text()
            for x in range(self.ui.SelectedDataLW.count())
        ]
        self.ui.AllDataLW.clear()
        self.ui.SelectedDataLW.clear()
        if all_data:
            selected_tag_names = [x for x in selected_data if x in all_data]
            not_selected_tag_names = [x for x in all_data if x not in selected_data]
            self.ui.AllDataLW.addItems(not_selected_tag_names)
            self.ui.SelectedDataLW.addItems(selected_tag_names)
            self.__sort()

    def __clear_data_in_selected_lw(self):
        """
        Отчищает список выбранных данных.
        Удаляет элементы выбранные пользователем и перемещает их в список всех элементов.
        """

        try:
            items = [item for item in self.ui.SelectedDataLW.selectedItems()]
            if len(items) > 0:
                for item in items:
                    ind = self.ui.SelectedDataLW.indexFromItem(item).row()
                    self.ui.SelectedDataLW.takeItem(ind)
                    if not self.isDropToInput:
                        self.ui.AllDataLW.addItem(item.text())
            else:
                existing_items = [
                    self.ui.SelectedDataLW.item(x).text()
                    for x in range(self.ui.SelectedDataLW.count())
                ]
                self.ui.AllDataLW.addItems(existing_items)
                self.ui.SelectedDataLW.clear()
            if not self.isDropToInput:
                self.__sort()
        except Exception as e:
            logger.error(e, exc_info=True)

    def __drop_data_to_input_lw(self):
        """
        Функция вызывается, если пользователь перекидывает элементы из списка выбранных в список всех элементов.
        Вызывает функцию удаления элементов из списка.
        Если все элементы удалены, то сортирует список.
        """

        try:
            self.isDropToInput = True
            count_items = len(self.ui.SelectedDataLW.selectedItems())
            if count_items:
                self.count_drop_items = count_items
                self.__clear_data_in_selected_lw()
            self.count_drop_items -= 1
            if self.count_drop_items == 0:
                self.__sort()
            self.isDropToInput = False
        except Exception as e:
            logger.error(e, exc_info=True)

    def __drop_data_to_selected_lw(self):
        """
        Функция вызывается, если пользователь перекидывает элементы из списка всех элементов в список выбранных.
        Вызывает функцию добавления элементов в список выбранных.
        Если все элементы добавлены, то сортирует список.
        """

        try:
            self.isDropToSelected = True
            count_items = len(self.ui.AllDataLW.selectedItems())
            if count_items:
                self.count_drop_items = count_items
                self.__add_data_to_selected_lw()
            self.count_drop_items -= 1
            if self.count_drop_items == 0:
                self.__sort()
            self.isDropToSelected = False
        except Exception as e:
            logger.error(e, exc_info=True)

    def __add_data_to_selected_lw(self):
        """Добавляет выбранные элементы в список выбранных элементов. Удаляет их из списка доступных элементов."""

        try:
            items = [item for item in self.ui.AllDataLW.selectedItems()]
            for item in items:
                if not self.isDropToSelected:
                    self.ui.SelectedDataLW.addItem(item.text())
                ind = self.ui.AllDataLW.indexFromItem(item).row()
                self.ui.AllDataLW.takeItem(ind)
            if not self.isDropToSelected:
                self.__sort()
        except Exception as e:
            logger.error(e, exc_info=True)

    def __sort(self):
        """Сортирует списки."""

        if self.sorting is not None:
            well_names = [
                self.ui.SelectedDataLW.item(x).text()
                for x in range(self.ui.SelectedDataLW.count())
            ]
            sorting_well_names = self.sorting(well_names)
            self.ui.SelectedDataLW.clear()
            self.ui.SelectedDataLW.addItems(sorting_well_names)
            well_names = [
                self.ui.AllDataLW.item(x).text()
                for x in range(self.ui.AllDataLW.count())
            ]
            self.ui.AllDataLW.clear()
            self.ui.AllDataLW.addItems(self.sorting(well_names))
