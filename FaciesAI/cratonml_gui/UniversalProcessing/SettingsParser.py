from abc import ABC, abstractmethod


class SettingsParser(ABC):
    def __init__(self, ui):
        super(SettingsParser, self).__init__()
        self.ui = ui

    @abstractmethod
    def get_settings(self):
        pass

    @abstractmethod
    def collecting_data_from_widget(self):
        pass
