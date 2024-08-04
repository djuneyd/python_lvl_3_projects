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

@bot.message_handler(commands=['name'])
def name_an_infant(message):
    markup = generate_markup_ethnicity(message.chat.id)

# names output
def names_amount(ethnicity, gender, chat_id):
    sql = f'''SELECT Names_data.Childs_First_Name, SUM(Names_data.Count) AS overall
            FROM Names_data WHERE Ethnicity="{ethnicity}" AND Gender="{gender}" GROUP BY Names_data.Childs_First_Name ORDER BY overall DESC LIMIT 10'''
    data = []
    # хуйня не берёт инфу, уже по гендеру
    result = manager.select_data(sql, data)
    print(result)

    response = ''
    responselist = []
    for i in result:
        responselist.append(f'{i[0]} : {i[1]}\n')
    bot.send_message(chat_id, f"{response.join(responselist)}")
    
# gender question
def generate_markup_gender(chat_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('MALE', callback_data='gender MALE'))
    markup.add(InlineKeyboardButton('FEMALE', callback_data='gender FEMALE'))
    bot.send_message(chat_id,f"Выберите пол ребёночка.🥰", reply_markup=markup)


#callback process
data = []
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global data
    if call.data.split()[0] == 'ethnicity':
        ethnicity = call.data.replace(f'{call.data.split()[0] }', '')
        data.append(ethnicity)
        # bot.send_message(call.message.chat.id,f"{ethnicity}")
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        generate_markup_gender(call.message.chat.id)
    elif call.data.split()[0] == 'gender':
        gender = call.data.split()[1]
        data.append(gender)
        names_amount(data[0], data[1], call.message.chat.id)
        
    
if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()