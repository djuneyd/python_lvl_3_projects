import matplotlib.pyplot as plt
import random
import sqlite3


# getting information
def info():
    conn = sqlite3.connect('matplotlib/e_vehicles_washington_population/data/Electric_Vehicle_Population_Data.db')
    check = 0
    with conn:
        cur = conn.cursor()
        cities = cur.execute('''SELECT DISTINCT City FROM Electric_Vehicle_Population_Data GROUP BY City''')
        cities = cities.fetchall()

        one_city_data = []
        data = []
        for city in cities:
            dat = cur.execute(f'''SELECT Model_Year, COUNT(Model_Year) FROM Electric_Vehicle_Population_Data WHERE City = "{city[0]}" GROUP BY Model_Year ORDER BY Model_Year''')
            years = []
            amounts = []
            for i in dat:
                years.append(i[0])
                amounts.append(i[1])
            one_city_data.append(years)
            one_city_data.append(amounts)
            data.append(one_city_data)
            one_city_data = []
            check+=1
            print(check)
        return data


# drawing the graph
def graph(data):
    plt.figure(figsize=(16, 8), facecolor='black')
    COLOR = 'lime'
    plt.rcParams.update({'text.color' : COLOR,
                     'axes.labelcolor' : COLOR,
                     'xtick.color' : COLOR,
                     'ytick.color' : COLOR})
    ax = plt.axes()
    ax.set_facecolor('black')
    for i in data:
        plt.plot(i[0], i[1], marker='o', color=(round(random.random(), 1),round(random.random(), 1),round(random.random(), 1)))
    plt.title('Количества моделей электро каров определённого года в 757-и городах Вашингтона')
    plt.xlabel('Города')
    plt.ylabel('Количества')
    plt.grid(True)
    # сохранение графика
    plt.savefig('matplotlib/e_vehicles_washington_population/graph.png')
    # Отображаем график
    plt.show()
    
data = info()
graph(data)