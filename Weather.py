import bs4
import requests as req
import os
import sys


next_days_morning_weather = []
next_days_evening_weather = []
next_days_wing_speed_morning = []
next_days_wing_speed_evening = []


def print_week_values(w_m, w_e, wi_m, wi_e, d):
    w_m = w_m[::-1]
    w_e = w_e[::-1]
    wi_m = wi_m[::-1]
    wi_e = wi_e[::-1]
    d = d[::-1]

    menu = ' '*5 + 'Day' + ' '*5 + 'Morning temp   Morning wing   Evening temp   Evening wing'

    for k in range(7):
        print(menu)
        l_1 = '    --' + '-' * len(d[k]) + '--'
        l_2 = '    | ' + d[k] + ' |'

        print(l_1)
        print(l_2 + ' ' * (14 - len(l_2)) + w_m[k] + ' ' * 8 + wi_m[k]
        + ' ' * 8 + w_e[k]  + ' ' * 8 + wi_e[k])
        print(l_1)

        print('-' * 70)

    print('\n')



# import pyttsx3
#
# """Функция для озвучивания погоды"""
# def talk(words):
#     engine = pyttsx3.init()
#     engine.say(words)
#     engine.runAndWait()

while True:

    city = 'salekhard'
    """Открываем страницу с информацией на текущее время"""
    page = req.get('https://yandex.ru/pogoda/' + city)

    # Присваеваем переменной HTML код страницы
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    # Создаем массив со значениями нужного тега
    this_time_weather_arr = soup.select('.temp__value')

    # Присваеваем переменной нужный элемент массива с данными о погоде
    this_time_weather = this_time_weather_arr[0].getText() + '°'

    """Открываем страницу с информацией на весь день"""
    table_page = req.get('https://yandex.ru/pogoda/' + city + '/details')

    # Присваеваем переменной HTML код страницы
    table_page = bs4.BeautifulSoup(table_page.text, "html.parser")

    # Создаем массив с текстовыми значениями нужных тегов таблицы
    table = table_page.select('.temp__value')

    # Присваеваем переменным нужные значения
    morning = table[1].getText()

    morning_weather = table[0].getText() + '...' + table[1].getText()

    evening_weather = table[4].getText() + '...' + table[5].getText()

    """Создание списков с данными на несколько дней вперед"""
    page = req.get('https://salehard.nuipogoda.ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BD%D0%B0-14-%D0%B4%D0%BD%D0%B5%D0%B9')

    # Присваеваем переменной HTML код страницы
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    # Создаем массив со значениями нужного тега
    test_d = soup.select('.t')
    test_n = soup.select('.snt')


    i = 2
    for k in range(7):

        next_days_morning_weather.append(test_d[i].getText())

        next_days_evening_weather.append(test_n[i-1].getText())
        i += 1
    # print(next_days_morning_weather)

    """Переназначение переменной table для вывода даты"""
    table = table_page.select('.forecast-details__day-number')

    """Создание таблицы вывода прогнозов на неделю вперед"""
    print('-' * 70)

    days_arr = []

    for k in range(1, 8):
        days_arr.append(table[k].getText())


    """Создание переменных эллементов таблицы"""

    """Создание строки со значениями погоды"""
    space_1 = ' ' * ((22 - len(morning_weather))//2)
    space_2 = ' ' * (22 - ((22 - len(morning_weather))//2) - len(morning_weather))
    mornig_weather_text = '|' + space_1 + morning_weather + space_2 + '|'

    space_1 = ' ' * ((23 - len(this_time_weather))//2)
    space_2 = ' ' * (23-((23 - len(this_time_weather))//2) - len(this_time_weather))
    this_time_weather_text = space_1 + this_time_weather + space_2 + '|'

    space_1 = ' ' * ((21 - len(evening_weather))//2)
    space_2 = ' ' * (21 - ((21 - len(evening_weather))//2) - len(evening_weather))
    evening_weather_text = space_1 + evening_weather + space_2 + '|'

    # Создаем массив с текстовыми значениями нужных тегов таблицы
    table = table_page.select('.weather-table__wrapper .weather-table__wind')

    """Создаем переменные со значениями скорости ветра"""

    try:
        this_time_wing = soup.select('.wind-speed')[0].getText() + ' m/s'
    except IndexError:
        this_time_wing = '--'

    try:
        morning_wing = table[0].getText() + ' m/s'
    except IndexError:
        morning_wing = '--'

    try:
        evening_wing = table[2].getText() + ' m/s'
    except IndexError:
        evening_wing = '--'

    """Создание строки со значениями скорости ветра"""
    space_1 = ' ' * ((22 - len(morning_wing))//2)
    space_2 = ' ' * (22 - (22 - len(morning_wing))//2 - len(morning_wing))
    morning_wing_text = '|' + space_1 + morning_wing + space_2

    space_1 = ' ' * ((23 - len(this_time_wing))//2)
    space_2 = ' ' * (23 - (23 - len(this_time_wing))//2 - len(this_time_wing))
    this_time_wing_text = '|' + space_1 + this_time_wing + space_2

    space_1 = ' ' * ((21 - len(evening_wing))//2)
    space_2 = ' ' * (21 - (21 - len(evening_wing))//2 - len(evening_wing))
    evening_wing_text = '|' + space_1 + evening_wing + space_2 + '|'

    """Создание списков с данными на несколько дней вперед"""

    i = 4
    for k in range(7):

        next_days_wing_speed_morning.append(table[i].getText())
        i += 2
        next_days_wing_speed_evening.append(table[i].getText())
        i += 2

    for k in range(len(next_days_wing_speed_evening)):
        if next_days_wing_speed_evening[k] == 'Штиль':
            next_days_wing_speed_evening[k] = '0 m/s'

    for k in range(len(next_days_wing_speed_morning)):
        if next_days_wing_speed_morning[k] == 'Штиль':
            next_days_wing_speed_morning[k] = '0 m/s'


    """"""

    print_week_values(next_days_morning_weather, next_days_evening_weather,
                    next_days_wing_speed_morning, next_days_wing_speed_evening,
                    days_arr)

    """Вывод данных с сайта в виде таблицы"""
    print('-' * 70)

    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')
    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')

    print('| ' +' '*3 + 'Morning weather' +'   |   ' + 'This time weather' +'   |   '+ 'Evening weather' +' '*3 + '|')

    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')
    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')

    print('-' * 70)

    # print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')
    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')

    print(mornig_weather_text + this_time_weather_text + evening_weather_text)

    # print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')
    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')

    print('-' * 33 + 'Wing' + '-' * 33)

    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')

    print(morning_wing_text + this_time_wing_text + evening_wing_text)

    print('|' + ' ' * 22 + '|' + ' ' *23 + '|' + ' ' * 21 + '|')

    print('-' * 70)

    # if '−' in this_time_weather:
    #     talk("Температура минус " + this_time_weather_arr[0].getText() + "градуса")
    # else:
    #     talk("Температура " + this_time_weather)
    #
    # if '−' in this_time_wing:
    #     talk("Ветер отсутствует")
    # else:
    #     talk("Ветер " + soup.select('.wind-speed')[0].getText() + "Метра в секунду")

    # http://edu.shd.ru/informerv4.php?size=200
    # import urllib.request
    #
    # html = urllib.request.urlopen("http://edu.shd.ru/informerv4.php?size=200")
    # print(html)

    """ Курс битка и трона
    page = req.get('')

    # Присваеваем переменной HTML код страницы
    soup = bs4.BeautifulSoup(page.text, "html.parser")

    # Создаем массив со значениями нужного тега
    course = soup.select('.DFlfde')

    print(course)
    """

    x = input()

    x = x.lower()

    if x == "update" or x == "u":
        os.system('cls')
        continue
    else:
        sys.exit()
