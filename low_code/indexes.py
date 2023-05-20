class Indexes:
    def __init__(self, data, column):
        self.data = data
        self.name = column
        self.values = []

    def index(self):
        for i in self.data.data[self.name]:
            if i not in self.values:
                self.values.append(i)
        return self.values