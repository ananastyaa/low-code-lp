import numpy as np
class Data:
    def __init__(self, data):
        self.data = data
        self.columns = data.columns

    def read(self):
        print(self.data)

    def preprocess(self):
        self.data = self.data.replace('-', 1000)

