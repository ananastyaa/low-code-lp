import pandas as pd


class Parameter:
    def __init__(self, columns, param, data):
        self.columns_idx = columns
        self.param = param
        self.data = data
        self.values = {}

    def create(self):
        new_data = pd.DataFrame(data=self.data.data[self.columns_idx])
        params = pd.DataFrame(self.data.data[self.param])
        for row in new_data.itertuples(index=False, name='Index'):
            for i, r in params.iterrows():
                self.values[row] = r[0]
