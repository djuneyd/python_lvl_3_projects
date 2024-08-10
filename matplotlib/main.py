# Импортируем библиотеку matplotlib.pyplot для создания графиков
import matplotlib.pyplot as plt
# Импортируем библиотеку random для генерации случайных чисел
import random
import sqlite3

def get_data(start_date, end_date):
    con = sqlite3.connect('matplotlib\data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM data WHERE date BETWEEN ? AND ? ORDER BY date ", (start_date, end_date))
    res = cur.fetchall()
    con.close()
    dates = [res[i][0] for i in range(len(res))]
    prices = [res[i][1] for i in range(len(res))]
    return dates, prices

dates, prices = get_data('2022-01-01', '2022-01-11')

# Настройка размера фигуры графика (ширина 8 дюймов, высота 6 дюймов)
plt.figure(figsize=(8, 6))

# Создание линейного графика: по оси X идут числа от 1 до 10, по оси Y - случайные числа
# marker='o' означает, что каждое значение будет отмечено круглым маркером
# color='r' задает красный цвет линии
# linestyle='--' задает стиль линии (пунктирная)


plt.plot(dates, prices, marker='o', color='g', linestyle='--')

# Задаем заголовок графика
plt.title('Курс доллара')

# Задаем название оси X
plt.xlabel('Даты')

# Задаем название оси Y
plt.ylabel('Цена')

# Включаем сетку на графике для удобства восприятия данных
plt.grid(True)

# сохранение графика
plt.savefig('matplotlib/figure.png')

# Отображаем график
plt.show()

