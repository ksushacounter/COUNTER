import logging

from PySide6.QtWidgets import QCompleter

from cratonml_gui.UniversalWidgets.Settings.SettingsWidget import SettingsWidget
from cratonml_gui.templates.WLI.Widgets.Settings.Processing.WLI_ConfigParser import (
    WellLogInterpretationConfigParser,
)
from cratonml_gui.templates.WLI.Widgets.Settings.UI.WLI_Settings_ui import (
    Ui_WLISettingsWidget,
)
from cratonml_gui.UniversalWidgets.DataSelectWidget.DataSelectWidget import (
    DataSelectWidget,
)
from cratonml_gui.utilities.Signals import DataSelectWidgetSignals
from cratonml_gui.utilities.sorting import sort

logger = logging.getLogger("__name__")


class WellLogInterpretationSettingsWidget(SettingsWidget):
    def __init__(self, well_info, all_strat_levels_info, curve_tags_info):
        super(WellLogInterpretationSettingsWidget, self).__init__()
        self.well_info = well_info
        self.all_strat_levels_info = all_strat_levels_info
        self.curve_tags_info = curve_tags_info

        self.well_signal = DataSelectWidgetSignals()
        self.curve_signal = DataSelectWidgetSignals()

        self.well_select_widget = DataSelectWidget()
        self.curve_select_widget = DataSelectWidget()

        self.ui = Ui_WLISettingsWidget()
        self.ui.setupUi(self)

        self.update_data_widgets()
        self.update_config_data()
        self.__change_strat_combobox()
        self.__update_cluster_gb()
        self.__create_callbacks()

    def __change_strat_combobox(self):
        """Задает настройки выпадающего списка"""
        try:
            self.ui.TopCB.setEditable(True)
            self.ui.TopCB.completer().setCompletionMode(QCompleter.PopupCompletion)

            self.ui.BotCB.setEditable(True)
            self.ui.BotCB.completer().setCompletionMode(QCompleter.PopupCompletion)
        except Exception as e:
            logger.error(e, exc_info=True)

    def __add_strat_levels(self):
        """Обновляет имена стратиграфических уровней в выпадающем списке"""

        self.ui.TopCB.clear()
        self.ui.BotCB.clear()
        if self.all_strat_levels_info is not None:
            strat_levels_names = [
                val["level_name"] for val in self.all_strat_levels_info.values()
            ]
            self.ui.TopCB.addItems(strat_levels_names)
            self.ui.BotCB.addItems(strat_levels_names)

    def __create_callbacks(self):
        """Задает реакции на нажатие кнопок"""

        try:
            self.ui.WellBtn.clicked.connect(self.__open_well_select_widget)
            self.ui.CurveBtn.clicked.connect(self.__open_curve_select_widget)
            self.ui.ClusterMethodCB.currentIndexChanged.connect(
                self.__update_cluster_gb
            )
        except Exception as e:
            logger.error(e, exc_info=True)

    def __open_well_select_widget(self):
        """
        Открывает окно выбора гридов. Заполняет виджеты списков данными.
        Задает реакции на нажатие кнопок и перетаскивание объектов.
        """

        try:
            selected_well_names = [
                self.well_select_widget.ui.SelectedDataLW.item(x).text()
                for x in range(self.well_select_widget.ui.SelectedDataLW.count())
            ]
            self.well_select_widget = DataSelectWidget(
                widget=self.ui.WellLW,
                sorting=sort,
                title="Окно выбора скважин",
                signal=self.well_signal.data_empty_signal,
            )
            self.well_select_widget.open_data_select_widget(
                all_data=list(self.well_info.keys()),
                selected_data=selected_well_names,
                is_light_theme=self.is_light_theme,
            )
        except Exception as e:
            logger.error(e, exc_info=True)

    def __open_curve_select_widget(self):
        """
        Открывает окно выбора кривых. Заполняет виджеты списков данными.
        Задает реакции на нажатие кнопок и перетаскивание объектов.
        """

        try:
            selected_curve_names = [
                self.curve_select_widget.ui.SelectedDataLW.item(x).text()
                for x in range(self.curve_select_widget.ui.SelectedDataLW.count())
            ]
            tag_names = list(self.curve_tags_info.keys())
            if "n/a" in tag_names:
                tag_names.remove("n/a")
            self.curve_select_widget = DataSelectWidget(
                widget=self.ui.CurveLW,
                title="Окно выбора кривых",
                signal=self.curve_signal.data_empty_signal,
            )
            self.curve_select_widget.open_data_select_widget(
                all_data=tag_names,
                selected_data=selected_curve_names,
                sort=True,
                is_light_theme=self.is_light_theme,
            )
        except Exception as e:
            logger.error(e, exc_info=True)

    def func_update_curves_lw(self):
        """Обновляет данные о кривых."""

        try:
            tag_names = list(self.curve_tags_info.keys())
            if "n/a" in tag_names:
                tag_names.remove("n/a")
            self.curve_select_widget.add_data_to_input_lw(all_data=tag_names)
            self.curve_select_widget.delete_data()
        except Exception as e:
            logger.error(e, exc_info=True)

    def __update_cluster_gb(self):
        try:
            cluster_method = self.ui.ClusterMethodCB.currentText()
            self.ui.KMeansGB.hide()
            self.ui.GaussianMixtureGB.hide()
            self.ui.HDBSCANGB.hide()
            if cluster_method == "KMeans":
                self.ui.KMeansGB.show()
            elif cluster_method == "GaussianMixture":
                self.ui.GaussianMixtureGB.show()
            elif cluster_method == "HDBSCAN":
                self.ui.HDBSCANGB.show()
        except Exception as e:
            logger.error(e, exc_info=True)

    def __update_list_widgets(self, data):
        """Обновляет данные в виджетах списках."""

        all_wells = [
            self.well_select_widget.ui.AllDataLW.item(x).text()
            for x in range(self.well_select_widget.ui.AllDataLW.count())
        ]
        selected_wells = [
            self.ui.WellLW.item(x).text() for x in range(self.ui.WellLW.count())
        ]
        for well_name in data["Wells"]["well_names"]:
            if well_name in all_wells and well_name not in selected_wells:
                self.ui.WellLW.addItem(well_name)
        self.well_select_widget.move_data_to_selected_lw(data["Wells"]["well_names"])

        all_curves = [
            self.curve_select_widget.ui.AllDataLW.item(x).text()
            for x in range(self.curve_select_widget.ui.AllDataLW.count())
        ]
        selected_curves = [
            self.ui.CurveLW.item(x).text() for x in range(self.ui.CurveLW.count())
        ]
        for curve_name in data["Curves"]["curve_names"]:
            if curve_name in all_curves and curve_name not in selected_curves:
                self.ui.CurveLW.addItem(curve_name)
        self.curve_select_widget.move_data_to_selected_lw(data["Curves"]["curve_names"])

        if 0.1 <= data["Wells"]["minimal_width_in_meter"] <= 10.0:
            self.ui.MinWidthSB.setValue(data["Wells"]["minimal_width_in_meter"])

    def __update_strat_levels(self, data):
        """Обновляет данные об отбивках."""

        self.ui.StratGB.setChecked(data["StratLevels"]["is_checked"])
        top_strat_level_names = [
            self.ui.TopCB.itemText(x) for x in range(self.ui.TopCB.count())
        ]
        if data["TopStratLevel"]["name"] in top_strat_level_names:
            ind = top_strat_level_names.index(data["TopStratLevel"]["name"])
            self.ui.TopCB.setCurrentIndex(ind)
        all_top_strat_level_direction = [
            self.ui.TopDirectionCB.itemText(x)
            for x in range(self.ui.TopDirectionCB.count())
        ]
        if data["TopStratLevel"]["direction"] in all_top_strat_level_direction:
            ind = all_top_strat_level_direction.index(
                data["TopStratLevel"]["direction"]
            )
            self.ui.TopDirectionCB.setCurrentIndex(ind)
        if 0 <= data["TopStratLevel"]["shift"] <= 1000:
            self.ui.TopShiftSB.setValue(data["TopStratLevel"]["shift"])

        bot_strat_level_names = [
            self.ui.BotCB.itemText(x) for x in range(self.ui.BotCB.count())
        ]
        if data["BotStratLevel"]["name"] in bot_strat_level_names:
            ind = bot_strat_level_names.index(data["BotStratLevel"]["name"])
            self.ui.BotCB.setCurrentIndex(ind)
        all_bot_strat_level_direction = [
            self.ui.BotDirectionCB.itemText(x)
            for x in range(self.ui.BotDirectionCB.count())
        ]
        if data["BotStratLevel"]["direction"] in all_bot_strat_level_direction:
            ind = all_bot_strat_level_direction.index(
                data["BotStratLevel"]["direction"]
            )
            self.ui.BotDirectionCB.setCurrentIndex(ind)
        if 0 <= data["BotStratLevel"]["shift"] <= 1000:
            self.ui.BotShiftSB.setValue(data["BotStratLevel"]["shift"])

    def __update_clusterization(self, data):
        """Обновляет данные о кластеризации."""

        clusterization_methods = [
            self.ui.ClusterMethodCB.itemText(x)
            for x in range(self.ui.ClusterMethodCB.count())
        ]
        if data["Clusterization"]["method"] in clusterization_methods:
            ind = clusterization_methods.index(data["Clusterization"]["method"])
            self.ui.ClusterMethodCB.setCurrentIndex(ind)
        if data["Clusterization"]["method"] == "KMeans":
            if "n_clusters" in data["Clusterization"]:
                if 2 <= data["Clusterization"]["n_clusters"] <= 20:
                    self.ui.KMeansSB.setValue(data["Clusterization"]["n_clusters"])
            if "auto_selection" in data["Clusterization"]:
                self.ui.KMeansCheckBox.setChecked(
                    data["Clusterization"]["auto_selection"]
                )
        if data["Clusterization"]["method"] == "GaussianMixture":
            if "n_clusters" in data["Clusterization"]:
                if 2 <= data["Clusterization"]["n_clusters"] <= 20:
                    self.ui.GaussianMixtureSB.setValue(
                        data["Clusterization"]["n_clusters"]
                    )
            if "auto_selection" in data["Clusterization"]:
                self.ui.GaussianMixtureCheckBox.setChecked(
                    data["Clusterization"]["auto_selection"]
                )
        elif data["Clusterization"]["method"] == "HDBSCAN":
            if "min_cluster_size" in data["Clusterization"]:
                self.ui.HDBSCANMinClusterSizeSB.setValue(
                    data["Clusterization"]["min_cluster_size"]
                )
            if "cluster_selection_epsilon" in data["Clusterization"]:
                self.ui.HDBSCANEpsilonSB.setValue(
                    data["Clusterization"]["cluster_selection_epsilon"]
                )

    def __update_optional_params(self, data):
        """Обновляет данные о дополнительных параметрах(нормализация, выбросы, понижение размерности)."""

        self.ui.PreparerGB.setChecked(data["Optional_parameters"]["is_checked"])
        self.ui.NormalizationGB.setChecked(data["Normalization"]["is_checked"])
        self.ui.OutliersGB.setChecked(data["Outliers"]["is_checked"])
        self.ui.PCAGB.setChecked(data["PCA"]["is_checked"])

        outliers_methods = [
            self.ui.OutliersCB.itemText(x) for x in range(self.ui.OutliersCB.count())
        ]
        if data["Outliers"]["method"] in outliers_methods:
            ind = outliers_methods.index(data["Outliers"]["method"])
            self.ui.OutliersCB.setCurrentIndex(ind)

        normalization_methods = [
            self.ui.NormalizationCB.itemText(x)
            for x in range(self.ui.NormalizationCB.count())
        ]
        if data["Normalization"]["method"] in normalization_methods:
            ind = normalization_methods.index(data["Normalization"]["method"])
            self.ui.NormalizationCB.setCurrentIndex(ind)

        if 2 <= data["PCA"]["n_components"] <= 99:
            self.ui.PCANumbersComponentsSB.setValue(data["PCA"]["n_components"])

    def update_data(self, data):
        """Запускает обновление всех данных, на данные в конфигурационном файле (*.ini)."""

        self.__update_list_widgets(data)
        self.__update_strat_levels(data)
        self.__update_clusterization(data)
        self.__update_optional_params(data)

    def update_data_widgets(self):
        """Обновляет данные в виджетах."""

        self.__add_strat_levels()
        self.well_select_widget.add_data_to_input_lw(
            all_data=list(self.well_info.keys())
        )
        self.well_select_widget.delete_data()
        self.func_update_curves_lw()

    def create_config_parser(self):
        """Создает парсер конфигурационного файла."""

        return WellLogInterpretationConfigParser(
            self.ui, self.well_signal, self.curve_signal
        )

    def close_widgets(self):
        """Закрывает все виджеты."""

        self.well_select_widget.close()
        self.curve_select_widget.close()

    def update_theme(self, is_light_theme):
        self.is_light_theme = is_light_theme
        if self.well_select_widget is not None:
            self.well_select_widget.update_style_sheet(self.is_light_theme)
        if self.curve_select_widget is not None:
            self.curve_select_widget.update_style_sheet(self.is_light_theme)
