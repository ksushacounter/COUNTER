from cratonml_gui.UniversalProcessing.Caching import Caching


class WLICaching(Caching):
    def __init__(self):
        super(WLICaching, self).__init__()
        self.well_metadata = None
        self.wells_properties = None
        self.parses_properties = None
        self.prepare_settings = [None]
        self.auto_selection = [None]
        self.clustering_properties = [None]
        self.cluster_method = [None]
        self.post_processing_settings = [None]

    def get_are_settings_same(self):
        return self.are_settings_same

    def set_are_settings_same(self, state: bool, length=1):
        self.are_settings_same = [state] * length
        if self.well_metadata is None or len(self.prepare_settings) != length:
            self.prepare_settings = [None] * length
            self.auto_selection = [None] * length
            self.clustering_properties = [None] * length
            self.cluster_method = [None] * length
            self.post_processing_settings = [None] * length

    def update_read_info(self):
        self.are_settings_same = [False] * len(self.are_settings_same)
        self.well_metadata = {
            "well_names": self.settings.well_metadata["well_names"].copy(),
            "well_ids": self.settings.well_metadata["well_ids"].copy(),
        }

    def read_info_condition(self):
        condition = self.well_metadata == self.settings.well_metadata
        return (
            condition and all(self.are_settings_same) and not self.is_connection_update
        )

    def update_wells_properties(self):
        self.are_settings_same = [False] * len(self.are_settings_same)
        self.wells_properties = self.settings.wells_properties
        self.parses_properties = self.settings.parses_properties.copy()

    def wells_condition(self):
        condition1 = self.wells_properties == self.settings.wells_properties
        condition2 = self.parses_properties == self.settings.parses_properties
        return (
            condition1
            and condition2
            and all(self.are_settings_same)
            and not self.is_connection_update
        )

    def update_prepare_settings(self, ind):
        self.are_settings_same[ind] = False
        self.prepare_settings[ind] = self.settings.prepare_settings.copy()

    def prepare_condition(self, ind):
        condition = self.prepare_settings[ind] == self.settings.prepare_settings
        return (
            condition and self.are_settings_same[ind] and not self.is_connection_update
        )

    def update_clustering_settings(self, ind):
        self.are_settings_same[ind] = False
        self.auto_selection[ind] = self.settings.auto_selection
        self.clustering_properties[ind] = self.settings.clustering_properties.copy()
        self.cluster_method[ind] = self.settings.cluster_method

    def clustering_condition(self, ind):
        condition_1 = self.auto_selection[ind] == self.settings.auto_selection
        condition_2 = (
            self.clustering_properties[ind] == self.settings.clustering_properties
        )
        condition_3 = self.cluster_method[ind] == self.settings.cluster_method
        return (
            condition_1
            and condition_2
            and condition_3
            and self.are_settings_same[ind]
            and not self.is_connection_update
        )

    def update_post_processing_settings(self, ind):
        self.are_settings_same[ind] = False
        self.post_processing_settings[ind] = (
            self.settings.post_processing_settings.copy()
        )

    def post_processing_condition(self, ind):
        condition = (
            self.post_processing_settings[ind] == self.settings.post_processing_settings
        )
        return (
            condition and self.are_settings_same[ind] and not self.is_connection_update
        )
