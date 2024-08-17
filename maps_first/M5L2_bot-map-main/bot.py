import telebot
from config import *
from logic import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

commands = ['/start - начать\n', '/help - все команды\n', '/show_city - показать какойто город на карте\n', '/remember_city - добавить город в ваш список городов\n', '/show_my_cities - отрисовать ваш список городов\n']
commands = ''.join(commands)
@bot.message_handler(commands=['help'])
def handle_help(message):
    global commands
    bot.send_message(message.chat.id, f"""Привет! Доступные команды:
{commands}                     """)

def color_markup(chat_id):
    data = 'color'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('🔵', callback_data=f'{data} Blue'))
    markup.add(InlineKeyboardButton('🔴', callback_data=f'{data} Red'))
    markup.add(InlineKeyboardButton('🟢', callback_data=f'{data} Green'))
    bot.send_message(chat_id,f"Выберите цвет маркеров!", reply_markup=markup)

goroda = []
@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    # генерируем карту
    city_name = message.text.split()[-1].capitalize()
    goroda.append(city_name)
    color_markup(message.chat.id)

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1].capitalize()
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    global goroda
    # генерируем карту
    cities = manager.select_cities(message.chat.id)
    goroda = cities
    color_markup(message.chat.id)

    
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global goroda
    # удаление инлайн клавы
    bot.delete_message(call.message.chat.id, call.message.message_id)
    # ключевое слово
    key_word = call.data.split()[0]
    # обработка
    if key_word == 'color':
        # коррекция параметра
        color = call.data.split()[1]
        manager.create_grapf('maps_first/map.png', goroda, color)
        # время
        try:
            if len(goroda) == 1:
                conn = sqlite3.connect(manager.database)
                with conn:
                    cursor = conn.cursor()
                    cursor.execute('''SELECT country
                                    FROM cities  
                                    WHERE city = ?''', (*goroda,))
                    country = cursor.fetchone()
                country = country[0][0:2].upper()
                url = 'https://api.openweathermap.org/data/2.5/weather?q='+goroda[0]+', '+country+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
                print(url)
                weather_data = requests.get(url).json()
                temperature = round(weather_data['main']['temp'])
                temperature_feels = round(weather_data['main']['feels_like'])
                forecast = [goroda[0], str(temperature), str(temperature_feels)]
                bot.send_message(call.message.chat.id, f'Город: {forecast[0]}, Температура: {forecast[1]}°C, Ощущается как: {forecast[2]}°C')
        except:
            goroda = []
        goroda = []

        # Отправляем карту
        bot.send_document(call.message.chat.id, open('maps_first/map.png', 'rb'))

if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
