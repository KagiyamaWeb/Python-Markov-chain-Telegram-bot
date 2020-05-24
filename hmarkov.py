from histograms import Dictogram


def make_higher_order_markov_model(order, data):
    markov_model = dict()

    for i in range(0, len(data)-order):
        # Создаем окно
        window = tuple(data[i: i+order])
        # Добавляем в словарь
        if window in markov_model:
            # Присоединяем к уже существующему распределению
            markov_model[window].update([data[i+order]])
        else:
            markov_model[window] = Dictogram([data[i+order]])
    return markov_model
