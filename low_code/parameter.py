import pandas as pd


class Parameter:
    def __init__(self, columns, param, data):
        self.columns_idx = columns
        self.param = param
        self.data = data
        self.values = {}

    def create(self):
        new_data = pd.DataFrame(data=self.data[self.columns_idx])
        params = [elem for elem in self.data[self.param]]
        for i, row in enumerate(new_data.itertuples(index=False)):
            temp = (row[0], row[1])
            self.values[temp] = int(params[i])
        return self.values
        
