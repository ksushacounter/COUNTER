from PySide6.QtCore import QObject, Signal


class WorkerSignals(QObject):
    """Класс сигналов."""

    progress = Signal(tuple)
    message = Signal(object)
    result = Signal((object,), (object, int))
    error = Signal()


class DataSelectWidgetSignals(QObject):
    data_empty_signal = Signal()


class WidgetSignals(QObject):
    """Класс сигналов для виджетов."""

    signal_for_visualization_result = Signal(object)
    signal_for_visualization_pca_statistics = Signal(object)


class SSFAWidgetSignals(QObject):
    """Класс сигналов для виджета сейсмофациального анализа с учителем."""

    signal_for_visualization_statistics = Signal(object)
    signal_for_run_calculate_classes = Signal(object)
    signal_for_run_join_classes = Signal(object)
