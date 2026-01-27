import logging

from cratonml_gui.UniversalProcessing.ConfigParser import ConfigParser

logger = logging.getLogger("__name__")


class WellLogInterpretationConfigParser(ConfigParser):
    def __init__(self, ui, well_signal, curve_signal):
        super(WellLogInterpretationConfigParser, self).__init__(ui, "mltoolbox_WLI")

        self.well_signal = well_signal
        self.curve_signal = curve_signal

    def create_callbacks(self):
        """Задает реакции на изменение данных пользователем."""

        self.ui.StratGB.toggled.connect(self.prepare_config)
        self.ui.TopCB.currentIndexChanged.connect(self.prepare_config)
        self.ui.TopShiftSB.valueChanged.connect(self.prepare_config)
        self.ui.TopDirectionCB.currentIndexChanged.connect(self.prepare_config)
        self.ui.BotCB.currentIndexChanged.connect(self.prepare_config)
        self.ui.BotShiftSB.valueChanged.connect(self.prepare_config)
        self.ui.BotDirectionCB.currentIndexChanged.connect(self.prepare_config)

        self.ui.ClusterMethodCB.currentIndexChanged.connect(self.prepare_config)
        self.ui.KMeansSB.valueChanged.connect(self.prepare_config)
        self.ui.KMeansCheckBox.checkStateChanged.connect(self.prepare_config)
        self.ui.GaussianMixtureSB.valueChanged.connect(self.prepare_config)
        self.ui.GaussianMixtureCheckBox.checkStateChanged.connect(self.prepare_config)
        self.ui.HDBSCANMinClusterSizeSB.valueChanged.connect(self.prepare_config)
        self.ui.HDBSCANEpsilonSB.valueChanged.connect(self.prepare_config)

        self.ui.PreparerGB.toggled.connect(self.prepare_config)
        self.ui.NormalizationGB.toggled.connect(self.prepare_config)
        self.ui.NormalizationCB.currentIndexChanged.connect(self.prepare_config)
        self.ui.OutliersGB.toggled.connect(self.prepare_config)
        self.ui.OutliersCB.currentIndexChanged.connect(self.prepare_config)
        self.ui.PCAGB.toggled.connect(self.prepare_config)
        self.ui.PCANumbersComponentsSB.valueChanged.connect(self.prepare_config)

        self.ui.WellLW.model().rowsInserted.connect(self.prepare_config)
        self.well_signal.data_empty_signal.connect(self.prepare_config)
        self.ui.CurveLW.model().rowsInserted.connect(self.prepare_config)
        self.curve_signal.data_empty_signal.connect(self.prepare_config)

        self.ui.MinWidthSB.valueChanged.connect(self.prepare_config)

    def prepare_config(self):
        """Вызывает обновление данных в файле."""

        try:
            self.config["Wells"] = {
                "well_names": str(
                    [
                        self.ui.WellLW.item(x).text()
                        for x in range(self.ui.WellLW.count())
                    ]
                ),
                "minimal_width_in_meter": self.ui.MinWidthSB.value(),
            }
            self.config["Curves"] = {
                "curve_names": [
                    self.ui.CurveLW.item(x).text()
                    for x in range(self.ui.CurveLW.count())
                ]
            }
            self.config["StratLevels"] = {"is_checked": self.ui.StratGB.isChecked()}
            self.config["TopStratLevel"] = {
                "name": self.ui.TopCB.currentText(),
                "shift": self.ui.TopShiftSB.value(),
                "direction": self.ui.TopDirectionCB.currentText(),
            }
            self.config["BotStratLevel"] = {
                "name": self.ui.BotCB.currentText(),
                "shift": self.ui.BotShiftSB.value(),
                "direction": self.ui.BotDirectionCB.currentText(),
            }
            self.config["Clusterization"] = {
                "method": self.ui.ClusterMethodCB.currentText()
            }

            if self.config["Clusterization"]["method"] == "KMeans":
                self.config["Clusterization"]["n_clusters"] = str(
                    self.ui.KMeansSB.value()
                )
                self.config["Clusterization"]["auto_selection"] = str(
                    self.ui.KMeansCheckBox.isChecked()
                )
            elif self.config["Clusterization"]["method"] == "GaussianMixture":
                self.config["Clusterization"]["n_clusters"] = str(
                    self.ui.GaussianMixtureSB.value()
                )
                self.config["Clusterization"]["auto_selection"] = str(
                    self.ui.GaussianMixtureCheckBox.isChecked()
                )
            elif self.config["Clusterization"]["method"] == "HDBSCAN":
                self.config["Clusterization"]["min_cluster_size"] = str(
                    self.ui.HDBSCANMinClusterSizeSB.value()
                )
                self.config["Clusterization"]["cluster_selection_epsilon"] = str(
                    self.ui.HDBSCANEpsilonSB.value()
                )

            self.config["Optional_parameters"] = {
                "is_checked": self.ui.PreparerGB.isChecked(),
            }
            self.config["Normalization"] = {
                "is_checked": self.ui.NormalizationGB.isChecked(),
                "method": self.ui.NormalizationCB.currentText(),
            }
            self.config["Outliers"] = {
                "is_checked": self.ui.OutliersGB.isChecked(),
                "method": self.ui.OutliersCB.currentText(),
            }
            self.config["PCA"] = {
                "is_checked": self.ui.PCAGB.isChecked(),
                "n_components": self.ui.PCANumbersComponentsSB.value(),
            }

            self.update_config()
        except Exception as e:
            logger.error(e, exc_info=True)

    def upload_config(self):
        """Загружает данные из файла."""

        config = self.read_config()
        data = {
            "Wells": {"well_names": [], "minimal_width_in_meter": 0.1},
            "Curves": {"curve_names": []},
            "TopStratLevel": {"name": "", "shift": 0, "direction": ""},
            "StratLevels": {"is_checked": False},
            "BotStratLevel": {"name": "", "shift": 0, "direction": ""},
            "Clusterization": {"method": []},
            "Optional_parameters": {"is_checked": False},
            "Normalization": {"is_checked": False, "method": ""},
            "Outliers": {"is_checked": False, "method": ""},
            "PCA": {"is_checked": False, "n_components": 2},
        }

        if "Wells" in config:
            if "well_names" in config["Wells"]:
                data["Wells"]["well_names"] = [
                    i for i in config["Wells"]["well_names"][2:-2].split("', '")
                ]
            if "minimal_width_in_meter" in config["Wells"]:
                data["Wells"]["minimal_width_in_meter"] = float(
                    config["Wells"]["minimal_width_in_meter"]
                )

        if "Curves" in config and "curve_names" in config["Curves"]:
            data["Curves"]["curve_names"] = [
                i for i in config["Curves"]["curve_names"][2:-2].split("', '")
            ]

        if "StratLevels" in config:
            if "is_checked" in config["StratLevels"]:
                data["StratLevels"]["is_checked"] = (
                    config["StratLevels"]["is_checked"] == "True"
                )
        if "TopStratLevel" in config:
            if "name" in config["TopStratLevel"]:
                data["TopStratLevel"]["name"] = config["TopStratLevel"]["name"]
            if "shift" in config["TopStratLevel"]:
                data["TopStratLevel"]["shift"] = int(config["TopStratLevel"]["shift"])
            if "direction" in config["TopStratLevel"]:
                data["TopStratLevel"]["direction"] = config["TopStratLevel"][
                    "direction"
                ]
        if "BotStratLevel" in config:
            if "name" in config["BotStratLevel"]:
                data["BotStratLevel"]["name"] = config["BotStratLevel"]["name"]
            if "shift" in config["BotStratLevel"]:
                data["BotStratLevel"]["shift"] = int(config["BotStratLevel"]["shift"])
            if "direction" in config["BotStratLevel"]:
                data["BotStratLevel"]["direction"] = config["BotStratLevel"][
                    "direction"
                ]

        if "Clusterization" in config:
            if "method" in config["Clusterization"]:
                data["Clusterization"]["method"] = config["Clusterization"]["method"]
            if (
                data["Clusterization"]["method"] == "KMeans"
                or data["Clusterization"]["method"] == "GaussianMixture"
            ):
                if "n_clusters" in config["Clusterization"]:
                    data["Clusterization"]["n_clusters"] = int(
                        config["Clusterization"]["n_clusters"]
                    )
                if "auto_selection" in config["Clusterization"]:
                    data["Clusterization"]["auto_selection"] = (
                        config["Clusterization"]["auto_selection"] == "True"
                    )
            elif data["Clusterization"]["method"] == "HDBSCAN":
                if "min_cluster_size" in config["Clusterization"]:
                    data["Clusterization"]["min_cluster_size"] = int(
                        config["Clusterization"]["min_cluster_size"]
                    )
                if "cluster_selection_epsilon" in config["Clusterization"]:
                    data["Clusterization"]["cluster_selection_epsilon"] = float(
                        config["Clusterization"]["cluster_selection_epsilon"]
                    )

        if "Optional_parameters" in config:
            if "is_checked" in config["Optional_parameters"]:
                data["Optional_parameters"]["is_checked"] = (
                    config["Optional_parameters"]["is_checked"] == "True"
                )
        if "Normalization" in config:
            if "is_checked" in config["Normalization"]:
                data["Normalization"]["is_checked"] = (
                    config["Normalization"]["is_checked"] == "True"
                )
            if "method" in config["Normalization"]:
                data["Normalization"]["method"] = config["Normalization"]["method"]
        if "Outliers" in config:
            if "is_checked" in config["Outliers"]:
                data["Outliers"]["is_checked"] = (
                    config["Outliers"]["is_checked"] == "True"
                )
            if "method" in config["Outliers"]:
                data["Outliers"]["method"] = config["Outliers"]["method"]
        if "PCA" in config:
            if "is_checked" in config["PCA"]:
                data["PCA"]["is_checked"] = config["PCA"]["is_checked"] == "True"
            if "n_components" in config["PCA"]:
                data["PCA"]["n_components"] = int(config["PCA"]["n_components"])

        return data
