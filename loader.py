import pandas as pd

from abc import abstractmethod
from data import Data


class Loader:
    """
    Базовый класс загрузчик для классов, которые
    будут реализовывать методы загрузки данных
    из разных источников.
    """

    @abstractmethod
    def read(self):
        raise FileNotFoundError("Файл не найден")


class LoaderExcel(Loader):
    """ Реализует метод загрузки данных из `excel` формата."""

    def read(self, filepath):
        return pd.read_excel(filepath)


class LoaderCSV(Loader):
    """ Реализует метод загрузки данных из `csv` формата. """

    def read(self, filepath):
        return pd.read_csv(filepath)


class Client:
    """ Клиент, перебирающий все возможные запросы """

    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def response(self, filepath):
        for handler in self.handlers:
            try:
                Data(handler.read(filepath))
            except FileNotFoundError:
                pass
            except ValueError:
                pass


if __name__ == "__main__":
    client = Client()
    client.add_handler(LoaderExcel())
    client.add_handler(LoaderCSV())
    client.response("")
