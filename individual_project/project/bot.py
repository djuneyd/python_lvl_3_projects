from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-Аист, моё предназначение это помогать молодым семейкам без фантазии.
---------------------------------------------------------------------------
Я помогаю придумать вам красивое, а самое главное уникальное имя для вашего ребёночка!
---------------------------------------------------------------------------
Я анализирую свыше 70.000 различных записей которые ведутся с 2011-2021 года.
На протяжении этих десяти лет велось наблюдение над каждым именем вплоть до того, сколько детей определённой этнической принадлежности в определённый год определённого пола были названы определённым именем!
У меня хранятся данные 2.338.005-и детишек❗❗❗
---------------------------------------------------------------------------
/name - предложить имя.🧐
/most_popular_names - самые популярные имена.🚀
/the_rarest_names - самые редкие имена.🤯
/random_name - выдаёт рандомное имя по полу.🎲
""")

# ethnicity question
def generate_markup_ethnicity(chat_id):
    sql = f'''SELECT DISTINCT Ethnicity FROM Names_data'''
    data = []
    result = manager.select_data(sql, data)

    markup = InlineKeyboardMarkup()
    for i in result:
        markup.add(InlineKeyboardButton(i[0], callback_data=f'ethnicity {i[0]}'))
    bot.send_message(chat_id,"Выберите этническую принадлежность вашего ребёночка, или же максимально приблежённую.🥰", reply_markup=markup)

# gender question
def generate_markup_gender(chat_id, check, check_popularity):
    if check == 1:
        data = 'gender_name'
    elif check == 2:
        data = f'gender_popular_{check_popularity}'
    elif check == 3:
        data = f'gender_random'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('MALE', callback_data=f'{data} MALE'))
    markup.add(InlineKeyboardButton('FEMALE', callback_data=f'{data} FEMALE'))
    bot.send_message(chat_id,f"Выберите пол ребёночка.🥰", reply_markup=markup)

# same names question
def same_names_question(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('10', callback_data='amount 10'))
    markup.add(InlineKeyboardButton('100', callback_data='amount 100'))
    markup.add(InlineKeyboardButton('1000', callback_data='amount 1000'))
    markup.add(InlineKeyboardButton('10000', callback_data='amount 10000'))
    markup.add(InlineKeyboardButton('100000', callback_data='amount 100000'))
    bot.send_message(chat_id,f"Выберите максимальное количество тёзок вашего ребёночка.🥰", reply_markup=markup)

# number of names
def number_of_names(chat_id, check, popularity_check):
    if check == 1:
        data = 'number_name'
    elif check == 2:
        data = f'number_popular_{popularity_check}'
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('10', callback_data=f'{data} 10'))
    markup.add(InlineKeyboardButton('50', callback_data=f'{data} 50'))
    markup.add(InlineKeyboardButton('100', callback_data=f'{data} 100'))
    bot.send_message(chat_id,f"Выберите количество имён которые хотите посмотреть.🥰", reply_markup=markup)

# names output
def names_amount(ethnicity, gender, amount, number, chat_id):
    sql = f'''SELECT Names_data.Childs_First_Name, SUM(Names_data.Count) AS overall
            FROM Names_data WHERE Ethnicity="{ethnicity}" AND Gender="{gender}"
            GROUP BY Names_data.Childs_First_Name HAVING overall <= {amount} ORDER BY overall DESC LIMIT {number}'''
    data = []

    result = manager.select_data(sql, data)

    response = ''
    responselist = ['Имя:  |Названо детей за последние 10 лет:\n']
    for number,i in enumerate(result):
        responselist.append(f'{number+1}) {i[0]} : {i[1]}\n')
    amount = len(responselist) - 1

    if amount > 0:
        bot.send_message(chat_id, f'''Вот топ {amount} самых популярных имён среди детей {ethnicity}.🥰
{response.join(responselist)}''')
    else:
        bot.send_message(chat_id, 'У меня нет имён с такими параметрами.😲')
    
# name a child
@bot.message_handler(commands=['name'])
def name_an_infant(message):
    generate_markup_ethnicity(message.chat.id)

# most popular names output
def most_popular_or_rare_names_func(gender, amount, popularity_check, chat_id):
    if popularity_check == 1:
        sql = f'''SELECT Names_data.Childs_First_Name, SUM(Names_data.Count) as overall
                FROM Names_data WHERE Names_data.Gender="{gender}" GROUP BY Names_data.Childs_First_Name
                ORDER BY overall DESC LIMIT {amount}'''
    elif popularity_check == 2:
        sql = f'''SELECT Names_data.Childs_First_Name, SUM(Names_data.Count) as overall
                FROM Names_data WHERE Names_data.Gender="{gender}" GROUP BY Names_data.Childs_First_Name
                ORDER BY overall LIMIT {amount}'''
    data = []
    result = manager.select_data(sql, data)

    response = ''
    responselist = ['Имя:  |Названо детей за последние 10 лет:\n']
    for number,i in enumerate(result):
        responselist.append(f'{number+1}) {i[0]} : {i[1]}\n')
    amount = len(responselist) - 1
    bot.send_message(chat_id, f'''Вот топ {amount} самых популярных имён.🥰
{response.join(responselist)}''')

# random name function
def random_name_function(gender, chat_id):
    sql = f'SELECT Names_data.Childs_First_Name FROM Names_data WHERE Gender="{gender}"'
    data = []

    result = random.choice(manager.select_data(sql, data))

    bot.send_message(chat_id, f'''Удача сложилась так, что вам выпало имя: {result[0]}😋''')

# most popular handler
@bot.message_handler(commands=['most_popular_names'])
def most_popular_names(message):
    generate_markup_gender(message.chat.id, 2, 1)

@bot.message_handler(commands=['the_rarest_names'])
def the_rarest_names(message):
    generate_markup_gender(message.chat.id, 2, 2)

# random name handler
@bot.message_handler(commands=['random_name'])
def random_name(message):
    generate_markup_gender(message.chat.id, 3, 0)
    
# callback process
data = []
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global data
    # удаление инлайн клавы
    bot.delete_message(call.message.chat.id, call.message.message_id)
    # ключевое слово
    key_word = call.data.split()[0]
    # обработка
    if key_word == 'ethnicity':
        # коррекция параметра
        ethnicity = call.data.replace(f'{key_word}', '').strip()
        data.append(ethnicity)
        # некст гуэшн
        generate_markup_gender(call.message.chat.id, 1, 1)
    elif key_word == 'gender_name':
        # коррекция параметра
        gender = call.data.split()[1]
        data.append(gender)
        # некст гуэшн
        same_names_question(call.message.chat.id)
    elif key_word == 'gender_popular_1':
        # коррекция параметра
        gender = call.data.split()[1]
        data.append(gender)
        # некст гуэшн
        number_of_names(call.message.chat.id, 2, 1)
    elif key_word == 'gender_popular_2':
        # коррекция параметра
        gender = call.data.split()[1]
        data.append(gender)
        # некст гуэшн
        number_of_names(call.message.chat.id, 2, 2)
    elif key_word == 'gender_random':
        # коррекция параметра
        gender = call.data.split()[1]
        data.append(gender)
        # ансвер 
        random_name_function(data[0], call.message.chat.id)
        data = []
    elif key_word == 'amount':
        # коррекция параметра
        amount = int(call.data.split()[1])
        data.append(amount)
        # некст гуэшн
        number_of_names(call.message.chat.id, 1, 1)
    elif key_word == 'number_name':
        # коррекция параметра
        amount = int(call.data.split()[1])
        data.append(amount)
        # ансвер 
        names_amount(data[0], data[1], data[2], data[3], call.message.chat.id)
        data = []
    elif key_word == 'number_popular_1':
        # коррекция параметра
        amount = int(call.data.split()[1])
        data.append(amount)
        # ансвер 
        most_popular_or_rare_names_func(data[0], data[1], 1, call.message.chat.id)
        data = []
    elif key_word == 'number_popular_2':
        # коррекция параметра
        amount = int(call.data.split()[1])
        data.append(amount)
        # ансвер 
        most_popular_or_rare_names_func(data[0], data[1], 2, call.message.chat.id)
        data = []
        
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()