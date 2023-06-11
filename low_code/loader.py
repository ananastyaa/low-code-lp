class Data:

    def __init__(self) -> None:
        pass

    def preprocess(self, data, param, opt_criteria='min'):
        new_values = []
        if opt_criteria == 'min':
            max = data[param].max() * 10 # умножаем, чтобы получить число больше макс и модель не рассматривала это как решение. Но максимальное находит неверно почему-то.
            for value in data[param]:
                try:
                    tmp = int(value)
                    new_value = tmp
                except:
                    new_value = max
                finally:
                    new_values.append(new_value)
        data[param] = new_values
        return data


            

