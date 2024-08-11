# Импортируем библиотеку matplotlib.pyplot для создания графиков
import matplotlib.pyplot as plt
# Импортируем библиотеку random для генерации случайных чисел
import random
import sqlite3

def get_data(start_date, end_date):
    con = sqlite3.connect('matplotlib_first_project\dollar\data.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM data WHERE date BETWEEN ? AND ? ORDER BY date ", (start_date, end_date))
    res = cur.fetchall()
    con.close()
    dates = [res[i][0] for i in range(len(res))]
    prices = [res[i][1] for i in range(len(res))]
    return dates, prices

dates, prices = get_data('2022-01-01', '2022-01-31')

def graph(dates, prices):
    plt.figure(figsize=(8, 6))
    plt.plot(dates, prices, marker='o', color='g', linestyle='--')
    plt.title('Курс доллара')
    plt.xlabel('Даты')
    plt.ylabel('Цена')
    plt.grid(True)
    # сохранение графика
    plt.savefig('matplotlib_first_project/dollar/figure.png')
    # Отображаем график
    plt.show()
    
graph(dates, prices)