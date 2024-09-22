from telebot import TeleBot
from config import *
from simple_gpt_yandex import *

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def greeting(message):
    bot.send_message(message.chat.id, '''ДОБРО ПОЖАЛОВАТЬ В ИГРУ КТО ХОЧЕТ СТАТЬ МИЛЛИОНЕРОМ!🎲
ЦЕЛЬ ИГРЫ ОТВЕТИТЬ НА 5 ВОПРОСОВ И ЗАБРАТЬ МАКСИМАЛЬНЫЙ ВЫИГРЫШ!
/new_game - начать новую игру💰
/profile - посмотреть баланс💲''')
    
money_counter = 1000
question_counter = 1
question = ''
@bot.message_handler(commands=['new_game'])
def game_start(message):
    global question_counter, question, money_counter
    question = gpt('Задай вопрос')
    bot.send_message(message.chat.id, f'''ВОПРОС НОМЕР {question_counter} ЗА {money_counter}$: 
{question}''')
    question_counter+=1
    bot.register_next_step_handler(message, question_repetition)

def question_repetition(message):
    # print('entered')
    global question_counter, question, money_counter
    if question_counter == 5:
        bot.send_message(message.chat.id, f'ПОБЕДА, Счёт пополнен на +{money_counter}$')
        question_counter = 1
    elif 'да' in checking(message.text, question):
        question = gpt('Задай вопрос')
        bot.send_message(message.chat.id, f'''ВОПРОС НОМЕР {question_counter} ЗА {money_counter*(2**question_counter)}$:
    {question}''')
        question_counter += 1
        bot.register_next_step_handler(message, question_repetition)
    else:
        bot.send_message(message.chat.id, 'Вы ответили не правильно! Заработанные деньги сгорели. 😥')
        question_counter = 0
    
if __name__ == '__main__':
    bot.infinity_polling()