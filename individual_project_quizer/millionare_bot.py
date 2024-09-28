from telebot import TeleBot
from config import *
from simple_gpt_yandex import *
from database import *

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def greeting(message):
    bot.send_message(message.chat.id, '''ДОБРО ПОЖАЛОВАТЬ В ИГРУ КТО ХОЧЕТ СТАТЬ МИЛЛИОНЕРОМ!🎲
ЦЕЛЬ ИГРЫ ОТВЕТИТЬ НА 5 ВОПРОСОВ И ЗАБРАТЬ МАКСИМАЛЬНЫЙ ВЫИГРЫШ!
/new_game - начать новую игру💰
/check_balance - посмотреть баланс.💰''')
    
    data = ()
    if message.from_user.id not in tracker.select_data('SELECT user_id FROM user_stats', data)[0]:
        tracker.executemany('INSERT INTO user_stats (user_id, username, total_money) VALUES (?, ?, ?)', (message.from_user.id, message.from_user.username, 0))

ingame_info = {}
@bot.message_handler(commands=['new_game'])
def game_start(message):
    global ingame_info
    ingame_info[f'{message.from_user.id}money'] = 1000
    ingame_info[f'{message.from_user.id}questionc'] = 1
    ingame_info[f'{message.from_user.id}quest'] = ''
    ingame_info[f'{message.from_user.id}quest'] = gpt('Задай вопрос')
    bot.send_message(message.chat.id, f'''ВОПРОС НОМЕР {ingame_info[f'{message.from_user.id}questionc']} ЗА {ingame_info[f'{message.from_user.id}money']}$: 
{ingame_info[f'{message.from_user.id}quest']}''')
    ingame_info[f'{message.from_user.id}questionc']+=1
    bot.register_next_step_handler(message, question_repetition)

def question_repetition(message):
    # print('entered')
    global ingame_info
    gpt_response = checking(message.text, ingame_info[f'{message.from_user.id}quest'])
    #print(gpt_response)
    if gpt_response == False:
        print('error')
        bot.send_message(message.chat.id, "Ошибка: gpt не ответил😭. Пожалуйста начните новую игру.")
    elif 'да' in gpt_response:
        if ingame_info[f'{message.from_user.id}questionc'] == 6:
            bot.send_message(message.chat.id, f'ПОБЕДА❗, Счёт пополнен на +{ingame_info[f'{message.from_user.id}money']}$')

            current_money = tracker.select_data(f'SELECT total_money FROM user_stats WHERE user_id = {message.from_user.id}', ())[0][0]
            tracker.executemany(f'UPDATE user_stats SET total_money = {current_money+ingame_info[f'{message.from_user.id}money']} WHERE user_id = {message.from_user.id}', ())
        else:
            bot.send_message(message.chat.id, f'''ПРАВИЛЬНЫЙ ОТВЕТ❗
    Продолжить? Да/Нет:''')
            bot.register_next_step_handler(message, continue_or_stop)
    else:
        bot.send_message(message.chat.id, 'Вы ответили не правильно❗ Заработанные деньги сгорели. 😥')

def continue_or_stop(message):
    global ingame_info
    answer = message.text.strip().lower()
    if answer == 'да':
        ingame_info[f'{message.from_user.id}quest'] = gpt('Задай вопрос')
        ingame_info[f'{message.from_user.id}money'] = int(ingame_info[f'{message.from_user.id}money']*(1.65**ingame_info[f'{message.from_user.id}questionc']))
        bot.send_message(message.chat.id, f'''ВОПРОС НОМЕР {ingame_info[f'{message.from_user.id}questionc']} ЗА {ingame_info[f'{message.from_user.id}money']}💲:
    {ingame_info[f'{message.from_user.id}quest']}''')
        ingame_info[f'{message.from_user.id}questionc'] += 1
        bot.register_next_step_handler(message, question_repetition)
    elif answer == 'нет':
        bot.send_message(message.chat.id, f'Игра окончена❗ Ваш баланс пополнен на +{ingame_info[f'{message.from_user.id}money']}')

        current_money = tracker.select_data(f'SELECT total_money FROM user_stats WHERE user_id = {message.from_user.id}', ())[0][0]
        tracker.executemany(f'UPDATE user_stats SET total_money = {current_money+ingame_info[f'{message.from_user.id}money']} WHERE user_id = {message.from_user.id}', ())
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, ответьте Да или Нет❗')
        bot.register_next_step_handler(message, continue_or_stop)

@bot.message_handler(commands=['check_balance'])
def check_balance(message):
    current_money = tracker.select_data(f'SELECT total_money FROM user_stats WHERE user_id = {message.from_user.id}', ())[0][0]
    bot.send_message(message.chat.id, f'Ваш текущий баланс: {current_money}$')

@bot.message_handler(commands=['leaderboard'])
def view_leaderboard(message):
    res = tracker.select_data('SELECT username, total_money FROM user_stats ORDER BY total_money DESC LIMIT 10')
    leaderboard = ['ТОП 10 БОГАТЕЙШИХ ГЕНИЕВ❗ \n', '\n']
    for i in range(len(res)):
        leaderboard.append(f'{i+1}) @{res[i][0]}: {res[i][1]}$ \n')       
    bot.send_message(message.chat.id, ''.join(leaderboard))
    
if __name__ == '__main__':
    tracker = MoneyTracker(DATABASE)
    tracker.create_table()
    bot.infinity_polling()