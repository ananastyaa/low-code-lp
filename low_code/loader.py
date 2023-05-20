import pandas as pd

from abc import abstractmethod
from data import Data
from indexes import Indexes
from parameter import Parameter
from model import Model


class Loader:
    """
    Базовый класс загрузчик для классов, которые
    будут реализовывать методы загрузки данных
    из разных источников.
    """

    @abstractmethod
    def read(self, filepath):
        pass


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
        self.columns_indexes = ['workers', 'tasks']
        self.param = ['time']

    def add_handler(self, handler):
        self.handlers.append(handler)

    def response(self, filepath):
        for handler in self.handlers:
            try:
                data = Data(handler.read(filepath))
                print(data.read())
                data.preprocess()
            except FileNotFoundError:
                pass
            except ValueError:
                pass
        self.create_model(data)


    def create_model(self, data):
        Model(data, self.columns_indexes, self.param).create()


if __name__ == "__main__":
    client = Client()
    client.add_handler(LoaderExcel())
    client.add_handler(LoaderCSV())
    client.response("task.csv")
