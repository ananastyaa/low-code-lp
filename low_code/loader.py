from model import Model

class Client:
    """ Клиент, перебирающий все возможные запросы """

    def __init__(self):
        self.handlers = []
        self.columns_indexes = ['workers', 'tasks']
        self.param = ['time']

    def add_handler(self, handler):
        self.handlers.append(handler)

    def response(self, data):
        data = data.replace('-', 1000)
        self.res = self.create_model(data)
        #print(self.res)
        return self.res

    def create_model(self, data):
        self.res = Model(data, self.columns_indexes, self.param).create()
