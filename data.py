class Data:
    def __init__(self, data):
        self.data = data
        self.columns = data.columns

    def read(self):
        print(self.data)
