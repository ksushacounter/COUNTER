from abc import abstractmethod


class View:
    def __init__(
        self,
        connection,
        set_enabled_func,
        signal_for_visualization_result,
        layout,
        show_message_func,
    ):
        super(View, self).__init__()
        self.connection = connection
        self.set_enabled_func = set_enabled_func
        self.signal_for_visualization_result = signal_for_visualization_result
        self.layout = layout
        self.show_message_func = show_message_func
        self.is_light_theme = True

        self.create_callback()

    def create_callback(self):
        """Создается реакция на сигнал начала визуализации."""

        self.signal_for_visualization_result.connect(self.run)

    @abstractmethod
    def run(self, result):
        """Запускает визуализацию."""

        pass

    @abstractmethod
    def set_enabled(self, state):
        """Если state=True делает элементы активными. Иначе делает их не активными."""

        pass

    def set_connection(self, connection):
        """Устанавливает новое соединение с WSeis."""

        self.connection = connection

    @abstractmethod
    def update_theme(self, is_light_theme):

        pass
