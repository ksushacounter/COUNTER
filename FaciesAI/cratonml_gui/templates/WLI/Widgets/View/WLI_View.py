import logging

import numpy as np
from PySide6.QtWidgets import QTabWidget

from cratonml_gui.UniversalControllers.WorkerSaver import WellWorkerSaver
from cratonml_gui.UniversalWidgets.TabWithSave.TabWithSave import TabWithSave
from cratonml_gui.UniversalWidgets.View.WellWindow import WellWindow
from cratonml_gui.templates.WLI.Widgets.Settings.WLI_Settings import WLISettingsResult
from cratonml_gui.templates.WLI.Widgets.View.Processing.WLI_DataParser import (
    get_strat_levels,
    update_visual_props,
    prepare_curve_data_for_visualization,
)
from cratonml_gui.utilities import Message
from cratonml_gui.UniversalWidgets.View.View import View


PROGRESS_BAR_VALUES = [0, 40, 100]
logger = logging.getLogger("__name__")


class WellLogInterpretationView(View):
    def __init__(
        self,
        well_info,
        curve_tags_info,
        connection,
        show_message_func,
        set_enabled_func,
        update_progress_bar_func,
        threadpool,
        signal_for_visualization_result,
        layout,
    ):
        super(WellLogInterpretationView, self).__init__(
            connection=connection,
            set_enabled_func=set_enabled_func,
            signal_for_visualization_result=signal_for_visualization_result,
            layout=layout,
            show_message_func=show_message_func,
        )
        self.well_info = well_info
        self.curve_tags_info = curve_tags_info
        self.update_progress_bar_func = update_progress_bar_func
        self.threadpool = threadpool

        self.tab_viewer = None
        self.settings = None
        self.curves_info = None
        self.strat_levels_info = None
        self.well_reader_result = None
        self.post_processing_data = None
        self.mask_curve = None
        self.clustering_result = None
        self.scaling_interval = None
        self.curve_names = None
        self.visual_properties = None
        self.strat_levels_names = None
        self.strat_levels_depths = None
        self.isFirstPlot = True
        self.plot_count = 0
        self.well_count = 0
        self.well_plot_widgets = []
        self.well_plot_tabs = []

    def __get_well_widget(self, well_number):
        return WellWindow(
            curves=self.well_reader_result[well_number].values[
                :, ~self.mask_curve[well_number]
            ],
            depths=self.well_reader_result[well_number].depths,
            labels=self.post_processing_data[well_number],
            names=np.array(self.curve_names[well_number])[
                ~self.mask_curve[well_number]
            ],
            colors=np.array(self.visual_properties["colors"])[
                ~self.mask_curve[well_number]
            ],
            logs=np.array(self.visual_properties["type_scale"])[
                ~self.mask_curve[well_number]
            ],
            priority=np.array(self.visual_properties["priority"])[
                ~self.mask_curve[well_number]
            ],
            is_light_theme=self.is_light_theme,
            labels_before_proc=self.clustering_result[well_number].labels,
            strat_levels_names=self.strat_levels_names[well_number],
            strat_levels_depths=self.strat_levels_depths[well_number],
            auto_scaling=np.array(self.visual_properties["auto_scaling"])[
                ~self.mask_curve[well_number]
            ],
            manual_scaling_interval=np.array(
                self.visual_properties["manual_scaling_interval"]
            )[~self.mask_curve[well_number]],
            manual_scaling_step=np.array(self.visual_properties["manual_scaling_step"])[
                ~self.mask_curve[well_number]
            ],
            scaling_interval=np.array(self.scaling_interval[well_number])[
                ~self.mask_curve[well_number]
            ],
        )

    def run(self, result):
        if type(result) is not WLISettingsResult:
            self.well_count = result
        else:
            try:
                if self.isFirstPlot:
                    self.isFirstPlot = False

                    self.settings = result.settings
                    self.curves_info = result.curves_info
                    self.strat_levels_info = result.strat_levels_info
                    self.well_count += len(self.settings.well_metadata["well_names"])

                    self.well_reader_result = list(range(self.well_count))
                    self.clustering_result = list(range(self.well_count))
                    self.post_processing_data = list(range(self.well_count))
                    self.mask_curve = list(range(self.well_count))
                    self.well_plot_widgets = []
                    self.well_plot_tabs = []

                    if self.tab_viewer:
                        self.tab_viewer.deleteLater()

                    self.tab_viewer = QTabWidget()
                    self.tab_viewer.setCurrentIndex(0)
                    self.layout.addWidget(self.tab_viewer)

                    self.scaling_interval, self.curve_names = (
                        prepare_curve_data_for_visualization(
                            curves_info=self.curves_info,
                            well_ids=self.settings.well_metadata["well_ids"],
                            tag_ids=[
                                self.curve_tags_info[tag_name]["id"]
                                for tag_name in self.settings.curve_metadata[
                                    "curve_names"
                                ]
                            ],
                        )
                    )
                    self.visual_properties = update_visual_props(
                        curve_tags_info=self.curve_tags_info,
                        tag_ids=[
                            self.curve_tags_info[tag_name]["id"]
                            for tag_name in self.settings.curve_metadata["curve_names"]
                        ],
                    )
                    self.strat_levels_names, self.strat_levels_depths = (
                        get_strat_levels(
                            well_ids=self.settings.well_metadata["well_ids"],
                            strat_levels_info=self.strat_levels_info,
                        )
                    )
                ind = result.ind
                self.well_reader_result[ind] = result.well_reader_result
                self.post_processing_data[ind] = result.post_processing_data
                self.clustering_result[ind] = result.clustering_result
                self.mask_curve[ind] = result.mask_curve
                self.well_plot_widget = self.__get_well_widget(ind)
                self.well_plot_tab = TabWithSave(
                    label_name="Имя кривой для сохранения",
                    button_name="Сохранить кривую",
                    widget=self.well_plot_widget,
                    save_function=self.__save_curve,
                    **{"ind": ind, "ind_plot": self.plot_count}
                )
                self.plot_count += 1
                self.tab_viewer.insertTab(
                    ind,
                    self.well_plot_tab,
                    self.settings.well_metadata["well_names"][ind],
                )
                self.well_plot_widgets.append(self.well_plot_widget)
                self.well_plot_tabs.append(self.well_plot_tab)

            except Exception as e:
                message = Message(
                    message="Произошла ошибка при визуализации.", is_warning=True
                )
                self.show_message_func(message)
                self.set_enabled_func(True)
                logger.error(e, exc_info=True)
        if self.well_count == self.plot_count or self.well_count < 0:
            self.set_enabled_func(True)
            self.isFirstPlot = True
            self.plot_count = 0
            self.well_count = 0

    def __save_curve(self, ind, ind_plot):
        """Сохраняет кривую в GISWell."""

        try:
            self.set_enabled_func(False)
            self.worker_saver = WellWorkerSaver(
                connection=self.connection,
                data=self.post_processing_data[ind],
                depths=self.well_reader_result[ind].depths,
                curve_name=self.well_plot_tabs[ind_plot].ui.SaveNameLE.text(),
                curve_type=0,
                well_id=self.settings.wells_properties[ind]["well_id"],
                data_name=self.settings.well_metadata["well_names"][ind],
                start_progress_bar_value=PROGRESS_BAR_VALUES[1],
                end_progress_bar_value=PROGRESS_BAR_VALUES[2],
            )
            self.worker_saver.signals.result.connect(
                lambda: self.set_enabled_func(True)
            )
            self.worker_saver.signals.progress.connect(self.update_progress_bar_func)
            self.worker_saver.signals.message.connect(self.show_message_func)
            self.worker_saver.signals.error.connect(lambda: self.set_enabled_func(True))
            self.threadpool.start(self.worker_saver)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при сохранении кривой.", is_warning=True
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def set_enabled(self, state):
        """Если state=True делает элементы активными. Иначе делает их не активными."""

        pass

    def update_info(self, well_info, curve_tags_info):
        """Обновляет метаданные в виджете."""

        try:
            if well_info is not None:
                self.well_info = well_info
            if curve_tags_info is not None:
                self.curve_tags_info = curve_tags_info
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении метаданных в виджете визуализации.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def update_theme(self, is_light_theme):
        self.is_light_theme = is_light_theme
        for well_plot_widget in self.well_plot_widgets:
            well_plot_widget.set_colors(self.is_light_theme)
