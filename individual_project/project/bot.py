from logic import DB_Manager
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-Аист, моё предназначение это помогать молодым семейкам без фантазии.
---------------------------------------------------------------------------
Я помогаю придумать вам красивое, а самое главное уникальное имя для вашего ребёночка!
---------------------------------------------------------------------------
Я анализирую свыше 70.000 различных записей которые ведутся с 2011-2021 года.
На протяжении этих десяти лет велось наблюдение над каждым именем вплоть до того, сколько детей определённой этнической принадлежности в определённый год определённого пола были названы определённым именем!
---------------------------------------------------------------------------
/name - предложить имя
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
def generate_markup_gender(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('MALE', callback_data='gender MALE'))
    markup.add(InlineKeyboardButton('FEMALE', callback_data='gender FEMALE'))
    bot.send_message(chat_id,f"Выберите пол ребёночка.🥰", reply_markup=markup)

def same_names_question(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('10', callback_data='amount 10'))
    markup.add(InlineKeyboardButton('100', callback_data='amount 100'))
    markup.add(InlineKeyboardButton('1000', callback_data='amount 1000'))
    markup.add(InlineKeyboardButton('10000', callback_data='amount 10000'))
    bot.send_message(chat_id,f"Выберите максимальное количество тёзок вашего ребёночка.🥰", reply_markup=markup)

# names output
def names_amount(ethnicity, gender, amount, chat_id):
    sql = f'''SELECT Names_data.Childs_First_Name, SUM(Names_data.Count) AS overall
            FROM Names_data WHERE Ethnicity="{ethnicity}" AND Gender="{gender}"
            GROUP BY Names_data.Childs_First_Name HAVING overall <= {amount} ORDER BY overall DESC LIMIT 10'''
    data = []

    result = manager.select_data(sql, data)

    response = ''
    responselist = ['Имя:  |Названо детей за последние 10 лет:\n']
    for i in result:
        responselist.append(f'{i[0]} : {i[1]}\n')
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
    
# callback process
data = []
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global data
    # удаление инлайн клавы
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data.split()[0] == 'ethnicity':
        # коррекция параметра
        ethnicity = call.data.replace(f'{call.data.split()[0]}', '')
        ethnicity = ethnicity.strip()
        data.append(ethnicity)
        # некст гуэшн
        generate_markup_gender(call.message.chat.id)
    elif call.data.split()[0] == 'gender':
        # коррекция параметра
        gender = call.data.split()[1]
        data.append(gender)
        # некст гуэшн
        same_names_question(call.message.chat.id)
    elif call.data.split()[0] == 'amount':
        # коррекция параметра
        amount = int(call.data.split()[1])
        data.append(amount)
        # ансвер 
        names_amount(data[0], data[1], data[2], call.message.chat.id)
        data = []
        
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()