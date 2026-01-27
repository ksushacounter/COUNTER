import logging
import time
from dataclasses import dataclass

from cratonml_gui.UniversalControllers.WorkerClustreing import WorkerClustering
from cratonml_gui.UniversalControllers.WorkerPostProcessing import (
    WellWorkerPostProcessing,
)
from cratonml_gui.UniversalControllers.WorkerPreparer import WorkerPreparer
from cratonml_gui.UniversalControllers.WorkerReader import WorkerWellReader
from cratonml_gui.UniversalControllers.WorkerInfoReader import (
    WorkerCurvesInfoReader,
    WorkerStratLevelsInfoReader,
)
from cratonml_gui.UniversalWidgets.Settings.Settings import Settings
from cratonml_gui.templates.WLI.Widgets.Settings.Processing.WLI_Caching import (
    WLICaching,
)
from cratonml_gui.templates.WLI.Widgets.Settings.Processing.WLI_SettingsParser import (
    WLISettingsParser,
)
from cratonml_gui.templates.WLI.Widgets.Settings.UI.WLI_Settings import (
    WellLogInterpretationSettingsWidget,
)
from cratonml_gui.utilities import Message

PROGRESS_BAR_VALUES = [0, 10, 20, 50, 70, 90, 100]
logger = logging.getLogger("__name__")


@dataclass
class WLISettingsResult:
    clustering_result: list or None
    settings: WLISettingsParser
    well_reader_result: list or None
    post_processing_data: list or None
    ind: int
    mask_curve: list or None
    curves_info: dict or None
    strat_levels_info: dict or None


class WellLogInterpretationSettings(Settings):
    def __init__(
        self,
        well_info,
        all_strat_levels_info,
        curve_tags_info,
        connection,
        threadpool,
        set_enabled_func,
        show_message_func,
        signal_for_visualization_result,
    ):
        super(WellLogInterpretationSettings, self).__init__(
            connection=connection,
            threadpool=threadpool,
            show_message_func=show_message_func,
            signal_for_visualization_result=signal_for_visualization_result,
            set_enabled_func=set_enabled_func,
        )
        self.well_info = well_info
        self.all_strat_levels_info = all_strat_levels_info
        self.curve_tags_info = curve_tags_info

        self.widget = WellLogInterpretationSettingsWidget(
            well_info=well_info,
            all_strat_levels_info=all_strat_levels_info,
            curve_tags_info=curve_tags_info,
        )
        self.widget.ui.progressFrame.hide()
        self.caching = WLICaching()

        self.pb_value = 0
        self.settings_preparer = None
        self.settings = None
        self.curves_info = None
        self.strat_levels_info = None
        self.well_reader_result = []

    def collecting_data_from_widget(self):
        """Обновляет все данные и запускает вычисления."""

        try:
            logger.info("Запущена интерпретация данных ГИС")

            self.pb_value = 0
            self.set_enabled_func(False)
            self.widget.ui.progressBar.setValue(0)
            self.widget.ui.progressBar.show()
            self.widget.add_gif()

            self.settings_preparer = WLISettingsParser(
                well_info=self.well_info,
                curve_tags_info=self.curve_tags_info,
                ui=self.widget.ui,
            )
            self.settings_preparer.update_well_metadata()
            self.settings = self.settings_preparer.get_settings()
            self.caching.set_settings(settings=self.settings)
            self.caching.set_are_settings_same(
                True, length=len(self.settings.well_metadata["well_names"])
            )
            self.run_read_curves_info()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при подготовке данных.", is_warning=True
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def run_read_curves_info(self):
        """Читает метаданные кривых. Ставит реакции на сигналы."""

        try:
            if (
                self.caching.read_info_condition()
                and self.curves_info is not None
                and self.strat_levels_info is not None
            ):
                self.update_progress_bar(
                    (PROGRESS_BAR_VALUES[0], PROGRESS_BAR_VALUES[2])
                )
                self.update_settings(self.strat_levels_info)
            else:
                self.caching.update_read_info()
                self.worker_curves_info_reader = WorkerCurvesInfoReader(
                    connection=self.connection,
                    well_ids=self.settings.well_metadata["well_ids"],
                    start_progress_bar_value=PROGRESS_BAR_VALUES[0],
                    end_progress_bar_value=PROGRESS_BAR_VALUES[1],
                )
                self.worker_curves_info_reader.signals.result.connect(
                    self.__run_read_start_levels_info
                )
                self.worker_curves_info_reader.signals.progress.connect(
                    self.update_progress_bar
                )
                self.worker_curves_info_reader.signals.message.connect(
                    self.show_message_func
                )
                self.worker_curves_info_reader.signals.error.connect(
                    lambda: self.set_enabled_func(True)
                )
                self.threadpool.start(self.worker_curves_info_reader)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтение метаданных кривых.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def __run_read_start_levels_info(self, result):
        """Читает метаданные стратиграфических уровней. Ставит реакции на сигналы."""

        try:
            self.curves_info = result
            if self.curves_info is not None:
                self.worker_strat_levels_info_reader = WorkerStratLevelsInfoReader(
                    connection=self.connection,
                    well_ids=self.settings.well_metadata["well_ids"],
                    all_strat_levels_info=self.all_strat_levels_info,
                    start_progress_bar_value=PROGRESS_BAR_VALUES[1],
                    end_progress_bar_value=PROGRESS_BAR_VALUES[2],
                )
                self.worker_strat_levels_info_reader.signals.result.connect(
                    self.update_settings
                )
                self.worker_strat_levels_info_reader.signals.progress.connect(
                    self.update_progress_bar
                )
                self.worker_strat_levels_info_reader.signals.message.connect(
                    self.show_message_func
                )
                self.worker_strat_levels_info_reader.signals.error.connect(
                    lambda: self.set_enabled_func(True)
                )
                self.threadpool.start(self.worker_strat_levels_info_reader)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтение метаданных стратиграфических уровней.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def update_settings(self, result):
        """Обновляет все данные и запускает вычисления."""

        try:
            self.strat_levels_info = result
            if self.strat_levels_info is not None:
                self.settings_preparer.update_info(
                    curves_info=self.curves_info.info,
                    strat_levels_info=self.strat_levels_info.info,
                )
                self.settings_preparer.collecting_data_from_widget()
                self.settings = self.settings_preparer.get_settings()
                self.caching.set_settings(settings=self.settings)

                self.well_count = len(self.settings.well_metadata["well_names"])

                if len(self.well_reader_result) != self.well_count:
                    self.well_reader_result = list(range(self.well_count))
                    self.prepare_result = list(range(self.well_count))
                    self.clustering_result = list(range(self.well_count))
                    self.post_processing_result = list(range(self.well_count))

                self.worker_preparer = list(range(self.well_count))
                self.worker_clustering = list(range(self.well_count))
                self.worker_post_processing = list(range(self.well_count))

                self.run()
        except Exception as e:
            message = Message(
                message="Произошла ошибка при подготовке данных.", is_warning=True
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def update_progress_bar(self, progress_bar_values):
        """Обновляет прогресс бар."""
        try:
            for i in range(
                int(self.pb_value) + 1,
                int(self.pb_value + progress_bar_values[1] - progress_bar_values[0])
                + 1,
            ):
                time.sleep(0.01)
                self.widget.ui.progressBar.setValue(i)
            self.pb_value += progress_bar_values[1] - progress_bar_values[0]
        except Exception as e:
            message = Message(
                message="Произошла ошибка при обновлении индикатора выполнения.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def run(self):
        """Читает гриды. Ставит реакции на сигналы."""

        try:
            if self.caching.wells_condition() and self.well_reader_result is not None:
                self.update_progress_bar(
                    (PROGRESS_BAR_VALUES[2], PROGRESS_BAR_VALUES[3])
                )
                for i, res in enumerate(self.well_reader_result):
                    self.__run_preparing(res, i)
            else:
                self.caching.update_wells_properties()
                self.worker_reader = WorkerWellReader(
                    settings=self.settings.wells_properties,
                    parse_settings=self.settings.parses_properties,
                    connection=self.connection,
                    well_names=self.settings.well_metadata["well_names"],
                    start_progress_bar_value=PROGRESS_BAR_VALUES[2],
                    end_progress_bar_value=PROGRESS_BAR_VALUES[3],
                )
                self.worker_reader.signals.result.connect(self.__run_preparing)
                self.worker_reader.signals.progress.connect(self.update_progress_bar)
                self.worker_reader.signals.message.connect(self.show_message_func)
                self.worker_reader.signals.error.connect(
                    self.emit_signal_for_visualization
                )
                self.threadpool.start(self.worker_reader)
        except Exception as e:
            message = Message(
                message="Произошла ошибка при чтение кривых.", is_warning=True
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def __run_preparing(self, result, ind):
        """Подготавливает кривые. Ставит реакции на сигналы."""

        try:
            self.well_reader_result[ind] = result
            if self.well_reader_result[ind] is not None:
                if (
                    self.caching.prepare_condition(ind)
                    and self.prepare_result[ind] is not None
                ):
                    self.update_progress_bar(
                        (
                            PROGRESS_BAR_VALUES[3],
                            PROGRESS_BAR_VALUES[3]
                            + (PROGRESS_BAR_VALUES[4] - PROGRESS_BAR_VALUES[3])
                            / self.well_count,
                        )
                    )
                    self.__run_clustering(self.prepare_result[ind], ind)
                else:
                    self.caching.update_prepare_settings(ind)
                    self.worker_preparer[ind] = WorkerPreparer(
                        data=self.well_reader_result[ind].values,
                        settings=self.settings.prepare_settings,
                        isCurves=True,
                        data_name=self.settings.well_metadata["well_names"][ind],
                        data_number=ind,
                        start_progress_bar_value=PROGRESS_BAR_VALUES[3],
                        end_progress_bar_value=PROGRESS_BAR_VALUES[3]
                        + (PROGRESS_BAR_VALUES[4] - PROGRESS_BAR_VALUES[3])
                        / self.well_count,
                    )
                    self.worker_preparer[ind].signals.result.connect(
                        self.__run_clustering
                    )
                    self.worker_preparer[ind].signals.progress.connect(
                        self.update_progress_bar
                    )
                    self.worker_preparer[ind].signals.message.connect(
                        self.show_message_func
                    )
                    self.worker_preparer[ind].signals.error.connect(
                        self.emit_signal_for_visualization
                    )
                    self.threadpool.start(self.worker_preparer[ind])
        except Exception as e:
            message = Message(
                message="Произошла ошибка при подготовке кривых.", is_warning=True
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def __run_clustering(self, result, ind):
        """Запускает кластеризацию данных. Ставит реакции на сигналы."""
        try:
            self.prepare_result[ind] = result
            if self.prepare_result[ind] is not None:
                if (
                    self.caching.clustering_condition(ind)
                    and self.clustering_result[ind] is not None
                ):
                    self.update_progress_bar(
                        (
                            PROGRESS_BAR_VALUES[4],
                            PROGRESS_BAR_VALUES[4]
                            + (PROGRESS_BAR_VALUES[5] - PROGRESS_BAR_VALUES[4])
                            / self.well_count,
                        )
                    )
                    self.__run_post_processing(self.clustering_result[ind], ind)
                else:
                    self.caching.update_clustering_settings(ind)
                    self.worker_clustering[ind] = WorkerClustering(
                        data=self.prepare_result[ind].data,
                        method=self.settings.cluster_method,
                        auto_selection=self.settings.auto_selection,
                        settings=self.settings.clustering_properties.copy(),
                        data_name=self.settings.well_metadata["well_names"][ind],
                        data_number=ind,
                        start_progress_bar_value=PROGRESS_BAR_VALUES[4],
                        end_progress_bar_value=PROGRESS_BAR_VALUES[4]
                        + (PROGRESS_BAR_VALUES[5] - PROGRESS_BAR_VALUES[4])
                        / self.well_count,
                    )
                    self.worker_clustering[ind].signals.result.connect(
                        self.__run_post_processing
                    )
                    self.worker_clustering[ind].signals.progress.connect(
                        self.update_progress_bar
                    )
                    self.worker_clustering[ind].signals.message.connect(
                        self.show_message_func
                    )
                    self.worker_clustering[ind].signals.error.connect(
                        self.emit_signal_for_visualization
                    )
                    self.threadpool.start(self.worker_clustering[ind])
        except Exception as e:
            message = Message(
                message="Произошла ошибка при кластеризации данных.", is_warning=True
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def __run_post_processing(self, result, ind):
        """Делает пост обработку данных. Ставит реакции на сигналы."""

        try:
            self.clustering_result[ind] = result
            if self.clustering_result[ind] is not None:
                if (
                    self.caching.post_processing_condition(ind)
                    and self.post_processing_result[ind] is not None
                ):
                    self.update_progress_bar(
                        (
                            PROGRESS_BAR_VALUES[5],
                            PROGRESS_BAR_VALUES[5]
                            + (PROGRESS_BAR_VALUES[6] - PROGRESS_BAR_VALUES[5])
                            / self.well_count,
                        )
                    )
                    self.emit_signal(self.post_processing_result[ind], ind=ind)
                else:
                    self.caching.update_post_processing_settings(ind)
                    self.worker_post_processing[ind] = WellWorkerPostProcessing(
                        values=self.clustering_result[ind].labels,
                        mask=self.prepare_result[ind].mask,
                        depths=self.well_reader_result[ind].depths,
                        data_name=self.settings.well_metadata["well_names"][ind],
                        data_number=ind,
                        start_progress_bar_value=PROGRESS_BAR_VALUES[5],
                        end_progress_bar_value=PROGRESS_BAR_VALUES[5]
                        + (PROGRESS_BAR_VALUES[6] - PROGRESS_BAR_VALUES[5])
                        / self.well_count,
                        **self.settings.post_processing_settings
                    )
                    self.worker_post_processing[ind].signals.result.connect(
                        self.emit_signal
                    )
                    self.worker_post_processing[ind].signals.progress.connect(
                        self.update_progress_bar
                    )
                    self.worker_post_processing[ind].signals.message.connect(
                        self.show_message_func
                    )
                    self.worker_post_processing[ind].signals.error.connect(
                        self.emit_signal_for_visualization
                    )
                    self.threadpool.start(self.worker_post_processing[ind])
        except Exception as e:
            message = Message(
                message="Произошла ошибка при пост обработке данных.", is_warning=True
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def prepare_data(self, result, ind=None):
        """Подготавливает данные для визуализации."""

        try:
            if self.well_count > 0:
                self.update_progress_bar(
                    (self.widget.ui.progressBar.value(), PROGRESS_BAR_VALUES[6])
                )
            self.post_processing_result[ind] = result
            if self.post_processing_result[ind] is None:
                self.emit_signal_for_visualization()
            else:
                return WLISettingsResult(
                    settings=self.settings,
                    well_reader_result=self.well_reader_result[ind],
                    mask_curve=self.prepare_result[ind].mask_curve,
                    clustering_result=self.clustering_result[ind],
                    post_processing_data=self.post_processing_result[ind].filled_data,
                    curves_info=self.curves_info.info,
                    strat_levels_info=self.strat_levels_info.info,
                    ind=ind,
                )
        except Exception as e:
            message = Message(
                message="Произошла ошибка при подготовке данных для визуализации.",
                is_warning=True,
            )
            self.show_message_func(message)
            self.set_enabled_func(True)
            logger.error(e, exc_info=True)

    def emit_signal_for_visualization(self):
        self.well_count -= 1
        self.signal_for_visualization_result.emit(self.well_count)
