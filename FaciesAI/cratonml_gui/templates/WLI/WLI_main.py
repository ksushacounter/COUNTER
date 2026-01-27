from cratonml_gui.UniversalWidgets.TabMain.TabMain import TabMain
from cratonml_gui.templates.WLI.Widgets.Settings.WLI_Settings import (
    WellLogInterpretationSettings,
)
from cratonml_gui.templates.WLI.Widgets.View.WLI_View import WellLogInterpretationView


class WellLogInterpretation(TabMain):
    def __init__(
        self,
        well_info,
        all_strat_levels_info,
        curve_tags_info,
        connection,
        update_button,
        threadpool,
    ):
        super(WellLogInterpretation, self).__init__(
            update_button=update_button, threadpool=threadpool
        )
        self.well_info = well_info
        self.all_strat_levels_info = all_strat_levels_info
        self.curve_tags_info = curve_tags_info

        self.settings = WellLogInterpretationSettings(
            well_info=well_info,
            all_strat_levels_info=all_strat_levels_info,
            curve_tags_info=curve_tags_info,
            connection=connection,
            threadpool=threadpool,
            signal_for_visualization_result=self.signal_for_visualization_result,
            set_enabled_func=self.set_enabled,
            show_message_func=self.show_message,
        )
        self.view = WellLogInterpretationView(
            well_info=well_info,
            curve_tags_info=curve_tags_info,
            set_enabled_func=self.set_enabled,
            show_message_func=self.show_message,
            update_progress_bar_func=self.settings.update_progress_bar,
            connection=connection,
            threadpool=threadpool,
            signal_for_visualization_result=self.signal_for_visualization_result,
            layout=self.ui.PlotLayout,
        )
        self.ui.SettingsLayout.addWidget(self.settings.widget)

        self.__create_callbacks()

    def __create_callbacks(self):
        """Создается реакция на нажатие кнопки запуска."""

        self.settings.widget.ui.StartBtn.clicked.connect(self.__run)

    def __run(self):
        self.message_line_count = 0
        self.ui.MessageLineEdit.clear()
        self.message_widget.ui.MessageTextEdit.clear()
        self.set_enabled(False)
        self.settings.collecting_data_from_widget()
