from dataclasses import dataclass
from typing import Type

import numpy as np
from cratonml.calculate.Clustering import (
    KMeansClassifier,
    GaussianMixtureClassifier,
    HDBSCANClassifier,
)
from cratonml.calculate.DimensionReduction import pca_transform
from cratonml.calculate.Prepare import (
    max_abs_scaler,
    min_max_scaler,
    standard_scaler,
    delete_outliers_LOF,
    delete_outliers_IsolationForest,
    delete_outliers_EllipticEnvelope,
)
from cratonml.data import Well

from cratonml_gui.UniversalProcessing.SettingsParser import SettingsParser


@dataclass
class WLISettings:
    well_metadata: dict
    curve_metadata: dict
    wells_properties: list
    parses_properties: list
    prepare_settings: dict
    cluster_method: (
        Type[KMeansClassifier]
        | Type[GaussianMixtureClassifier]
        | Type[HDBSCANClassifier]
    )
    auto_selection: bool
    clustering_properties: dict
    post_processing_settings: dict


class WLISettingsParser(SettingsParser):
    def __init__(self, well_info, curve_tags_info, ui):
        super(WLISettingsParser, self).__init__(ui)
        self.well_info = well_info
        self.curve_tags_info = curve_tags_info

        self.well_metadata = None
        self.curve_metadata = None
        self.wells_properties = None
        self.parses_properties = None
        self.prepare_settings = {}
        self.cluster_method = None
        self.auto_selection = None
        self.clustering_properties = None
        self.post_processing_settings = None

    def update_info(self, curves_info, strat_levels_info):
        self.curves_info = curves_info
        self.strat_levels_info = strat_levels_info

    def get_settings(self):
        return WLISettings(
            well_metadata=self.well_metadata,
            curve_metadata=self.curve_metadata,
            wells_properties=self.wells_properties,
            parses_properties=self.parses_properties,
            prepare_settings=self.prepare_settings,
            cluster_method=self.cluster_method,
            auto_selection=self.auto_selection,
            clustering_properties=self.clustering_properties,
            post_processing_settings=self.post_processing_settings,
        )

    def collecting_data_from_widget(self):
        """Обновляет все данные и запускает вычисления."""

        self.__prepare_data_for_worker_well_reader()
        self.__prepare_data_for_worker_upload_curves()
        self.__update_data_for_preparing()
        self.__prepare_data_for_clusterization()
        self.__update_width()

    def update_well_metadata(self):
        self.well_metadata = {"well_names": [], "well_ids": []}
        for idx in range(self.ui.WellLW.count()):
            item = self.ui.WellLW.item(idx)
            self.well_metadata["well_names"].append(item.text())
            self.well_metadata["well_ids"].append(self.well_info[item.text()]["id"])

    def __prepare_data_for_worker_well_reader(self):
        """Устанавливает параметр метаданных гридов."""

        self.strat_levels_parameters = {
            "top": {"name": None, "shift": None, "direction": None},
            "bot": {"name": None, "shift": None, "direction": None},
        }
        if self.ui.StratGB.isChecked():
            self.strat_levels_parameters = {
                "top": {
                    "name": self.ui.TopCB.currentText(),
                    "shift": self.ui.TopShiftSB.value(),
                    "direction": (
                        1 if self.ui.TopDirectionCB.currentText() == "Вниз" else -1
                    ),
                },
                "bot": {
                    "name": self.ui.BotCB.currentText(),
                    "shift": self.ui.BotShiftSB.value(),
                    "direction": (
                        1 if self.ui.BotDirectionCB.currentText() == "Вниз" else -1
                    ),
                },
            }

    def __prepare_data_for_worker_upload_curves(self):
        tag_names = {}
        tag_ids = []
        for idx in range(self.ui.CurveLW.count()):
            item = self.ui.CurveLW.item(idx)
            tag_ids.append(self.curve_tags_info[item.text()]["id"])
            tag_names[self.curve_tags_info[item.text()]["id"]] = item.text()
        tag_ids = sorted(tag_ids)
        self.curve_metadata = {
            "curve_names": [val for _, val in sorted(tag_names.items())]
        }
        self.wells_properties = []
        self.parses_properties = []
        well_ids = self.well_metadata["well_ids"]
        for well_id in well_ids:
            well_properties = {"well_id": well_id, "well_curve_types": tag_ids}
            if not self.ui.StratGB.isChecked():
                min_depth = -np.inf
                max_depth = np.inf
            else:
                min_depth = Well.get_strat_depth(
                    strat_dict=self.strat_levels_parameters["top"],
                    strat_info=self.strat_levels_info[well_id]["strat_levels"],
                    else_number=np.inf,
                )
                max_depth = Well.get_strat_depth(
                    strat_dict=self.strat_levels_parameters["bot"],
                    strat_info=self.strat_levels_info[well_id]["strat_levels"],
                    else_number=-np.inf,
                )
            parse_properties = {"min_depth": min_depth, "max_depth": max_depth}
            self.parses_properties.append(parse_properties)
            self.wells_properties.append(well_properties)

    def __update_data_for_preparing(self):
        if self.ui.PreparerGB.isChecked():
            self.__update_normalization()
            self.__update_outliers()
            self.__update_dimension_reduction()
        else:
            self.prepare_settings["scaler"] = False
            self.prepare_settings["outliers"] = False
            self.prepare_settings["dimension_reduction"] = False
        self.prepare_settings["balancing"] = False

    def __update_normalization(self):
        is_checked = self.ui.NormalizationGB.isChecked()
        if not is_checked:
            self.prepare_settings["scaler"] = False
        else:
            normalization = self.ui.NormalizationCB.currentText()
            match normalization:
                case "MaxAbs":
                    self.prepare_settings["scaler"] = max_abs_scaler
                case "MinMax":
                    self.prepare_settings["scaler"] = min_max_scaler
                case "Z-norm":
                    self.prepare_settings["scaler"] = standard_scaler

    def __update_outliers(self):
        is_checked = self.ui.OutliersGB.isChecked()
        if not is_checked:
            self.prepare_settings["outliers"] = False
        else:
            outliers = self.ui.OutliersCB.currentText()
            match outliers:
                case "LOF":
                    self.prepare_settings["outliers"] = delete_outliers_LOF
                case "IsolationForest":
                    self.prepare_settings["outliers"] = delete_outliers_IsolationForest
                case "EllipticEnvelope":
                    self.prepare_settings["outliers"] = delete_outliers_EllipticEnvelope

    def __update_dimension_reduction(self):
        is_checked = self.ui.PCAGB.isChecked()
        if not is_checked:
            self.prepare_settings["dimension_reduction"] = False
        else:
            self.prepare_settings["dimension_reduction"] = pca_transform
            self.prepare_settings["dimension_reduction_params"] = {
                "n_components": self.ui.PCANumbersComponentsSB.value()
            }

    def __prepare_data_for_clusterization(self):
        """."""

        cluster_method = self.ui.ClusterMethodCB.currentText()
        if cluster_method == "KMeans":
            n_clusters = self.ui.KMeansSB.value()
            self.auto_selection = self.ui.KMeansCheckBox.isChecked()
            self.cluster_method = KMeansClassifier
            self.clustering_properties = {"n_clusters": n_clusters}
        elif cluster_method == "GaussianMixture":
            n_clusters = self.ui.GaussianMixtureSB.value()
            self.auto_selection = self.ui.GaussianMixtureCheckBox.isChecked()
            self.cluster_method = GaussianMixtureClassifier
            self.clustering_properties = {"n_clusters": n_clusters}
        elif cluster_method == "HDBSCAN":
            self.auto_selection = False
            min_cluster_size = self.ui.HDBSCANMinClusterSizeSB.value()
            cluster_selection_epsilon = self.ui.HDBSCANEpsilonSB.value()
            self.cluster_method = HDBSCANClassifier
            self.clustering_properties = {
                "min_cluster_size": min_cluster_size,
                "cluster_selection_epsilon": cluster_selection_epsilon,
            }

    def __update_width(self):
        self.post_processing_settings = {
            "minimal_width_in_meter": self.ui.MinWidthSB.value()
        }
