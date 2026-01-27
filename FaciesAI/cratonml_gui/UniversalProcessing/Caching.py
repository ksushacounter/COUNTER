from abc import ABC


class Caching(ABC):
    def __init__(self):
        super(Caching, self).__init__()
        self.settings = None
        self.are_settings_same = True
        self.is_connection_update = False

    def set_settings(self, settings):
        self.settings = settings

    def get_are_settings_same(self):
        return self.are_settings_same

    def set_are_settings_same(self, state: bool):
        self.are_settings_same = state

    def set_is_connection_update(self, state: bool):
        self.is_connection_update = state
