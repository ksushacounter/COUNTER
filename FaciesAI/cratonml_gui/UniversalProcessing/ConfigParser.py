import configparser
import os
from abc import abstractmethod, ABC


class ConfigParser(ABC):
    def __init__(self, ui, name):
        super(ConfigParser, self).__init__()

        self.ui = ui
        self.name = name + ".ini"
        self.path = os.getenv("APPDATA") + "/StratoScope/MLToolBox/"
        os.makedirs(self.path, exist_ok=True)

        self.config = configparser.ConfigParser()

    @abstractmethod
    def create_callbacks(self):
        """Задает реакции на изменение данных пользователем."""

        pass

    @abstractmethod
    def prepare_config(self):
        """Вызывает обновление данных в файле."""

        pass

    def update_config(self):
        """Обновляет данные в файле."""

        with open(self.path + self.name, "w") as configfile:
            self.config.write(configfile)

    def read_config(self):
        """Читает данные из файла."""

        config = configparser.ConfigParser()
        config.read(self.path + self.name)
        return config

    @abstractmethod
    def upload_config(self):
        """Загружает данные из файла."""

        pass
