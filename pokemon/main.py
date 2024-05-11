import telebot 
from config import token

from logic import Pokemon

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        pokemon = Pokemon(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_message(message.chat.id, 'Обычная версия')
        bot.send_photo(message.chat.id, pokemon.show_img()[0])
        bot.send_message(message.chat.id, 'Светящаяся версия')
        bot.send_photo(message.chat.id, pokemon.show_img()[1])
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


bot.infinity_polling(none_stop=True)

