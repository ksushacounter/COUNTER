import logging

from PySide6.QtWidgets import QWidget

from cratonml_gui.UniversalWidgets.TabWithSave.TabWithSave_ui import (
    Ui_TabWithSaveWidget,
)

logger = logging.getLogger("__name__")


class TabWithSave(QWidget):
    def __init__(
        self, widget, save_function, label_name=None, button_name=None, **save_kwargs
    ):
        super(TabWithSave, self).__init__()

        self.ui = Ui_TabWithSaveWidget()
        self.ui.setupUi(self)

        self.set_names(label_name, button_name)
        self.add_plot(widget)
        self.__create_callback(save_function, **save_kwargs)

    def set_names(self, label_name=None, button_name=None):
        if label_name:
            self.ui.SaveNameLabel.setText(label_name)
        if button_name:
            self.ui.SaveMapBtn.setText(button_name)

    def add_plot(self, widget):
        self.ui.PlotLayout.addWidget(widget)

    def __create_callback(self, save_function, **save_kwargs):
        self.ui.SaveMapBtn.clicked.connect(lambda: save_function(**save_kwargs))
