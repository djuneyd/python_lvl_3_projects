from logic import DB_Manager
from config import *
from telebot import TeleBot

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-Аист, моё предназначение это помогать молодым семейкам без фантазии.
---------------------------------------------------------------------------
Я помогаю придумать вам красивое, а самое главное уникальное имя для вашего ребёночка!
---------------------------------------------------------------------------
Я анализирую свыше 70.000 различных имён детей, с разными возрастами, этническим происхождением, гендером и так далее.
""")

    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()