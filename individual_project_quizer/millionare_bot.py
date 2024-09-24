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
    money_counter = 1000
    question_counter = 1
    question = ''
    question = gpt('Задай вопрос')
    bot.send_message(message.chat.id, f'''ВОПРОС НОМЕР {question_counter} ЗА {money_counter}💲: 
{question}''')
    question_counter+=1
    bot.register_next_step_handler(message, question_repetition)

def question_repetition(message):
    # print('entered')
    global question_counter, question, money_counter
    gpt_response = checking(message.text, question)
    print(gpt_response)
    if gpt_response == False:
        print('error')
        bot.send_message(message.chat.id, "Ошибка: gpt не ответил😭. Пожалуйста начните новую игру.")
    elif 'да' in gpt_response:
#         question = gpt('Задай вопрос')
#         money_counter = int(money_counter*(1.65**question_counter))
#         bot.send_message(message.chat.id, f''' ПРАВИЛЬНЫЙ ОТВЕТ❗
# ВОПРОС НОМЕР {question_counter} ЗА {money_counter}💲:
#     {question}''')
#         question_counter += 1
#         bot.register_next_step_handler(message, question_repetition)

        if question_counter == 6:
            bot.send_message(message.chat.id, f'ПОБЕДА❗, Счёт пополнен на +{money_counter}💲')
        else:
            bot.send_message(message.chat.id, f'''ПРАВИЛЬНЫЙ ОТВЕТ❗
    Продолжить? Да/Нет:''')
            bot.register_next_step_handler(message, continue_or_stop)
    else:
        bot.send_message(message.chat.id, 'Вы ответили не правильно❗ Заработанные деньги сгорели. 😥')

def continue_or_stop(message):
    global question_counter, question, money_counter
    answer = message.text.strip().lower()
    if answer == 'да':
        question = gpt('Задай вопрос')
        money_counter = int(money_counter*(1.65**question_counter))
        bot.send_message(message.chat.id, f'''ВОПРОС НОМЕР {question_counter} ЗА {money_counter}💲:
    {question}''')
        question_counter += 1
        bot.register_next_step_handler(message, question_repetition)
    elif answer == 'нет':
        bot.send_message(message.chat.id, f'Игра окончена❗ Ваш баланс пополнен на +{money_counter}')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет❗')
        bot.register_next_step_handler(message, continue_or_stop)
    
if __name__ == '__main__':
    bot.infinity_polling()