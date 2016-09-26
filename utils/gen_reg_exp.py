# -*- coding: utf-8 -*-

def generate_regexp_by_format(fs):
    """
    Генерирует регулярку из форматной строки Python
    больше вариантов: https://docs.python.org/2/library/time.html
    :param fs:
    :return:
    """
    replaces = {
        '%d': '\d{2}', # день месяца [01,31].
        '%b': '\w{3}', # месяц (аббревиатура)
        '%Y': '\d{4}', # год 4 симв.
        '%X': '\d{2}:\d{2}:\d{2}', # время в локальном формате чч:мм:сс
        '%m': '\d{2}', # месяц числом [01,12].
        '%H': '\d{2}', # часы (24-формат)
        '%M': '\d{2}', # минуты
        '%S': '\d{2}', # секунды
        '%f': '\d{3}', # миллисикунды
    }

    res = fs.replace('/', '\/')
    for key in replaces:
        res = res.replace(key, replaces[key])
    return res