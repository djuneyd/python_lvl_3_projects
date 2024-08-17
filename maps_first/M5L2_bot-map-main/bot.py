import telebot
from config import *
from logic import *

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

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    # генерируем карту
    city_name = message.text.split()[-1].capitalize()
    manager.create_grapf('maps_first/map.png', [city_name])

    # Отправляем карту
    bot.send_document(message.chat.id, open('maps_first/map.png', 'rb'))


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
    # генерируем карту
    cities = manager.select_cities(message.chat.id)
    manager.create_grapf('maps_first/map.png', cities)

    # Отправляем карту
    bot.send_document(message.chat.id, open('maps_first/map.png', 'rb'))
    


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
