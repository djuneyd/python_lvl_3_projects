import config
from class_dz import Dog
import random
from logic import Pokemon, Wizard, Fighter
from datetime import datetime
from datetime import timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
# Создание объекта даты и времени
now = datetime.now()
print('Bot is active!')

#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.

import telebot

API_TOKEN = config.token

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я ЭхоБот.
Я здесь, чтобы повторить ваши добрые слова в ваш адрес. Просто скажи что-нибудь приятное, и я скажу тебе то же самое!😎\
""")
    bot.reply_to(message, """\
НЕКОТОРЫЕ КОМАНДЫ!😉
/dog - сделать собачку, рядом укажите имя, породу и характер🐶
/dice - кинуть игральную кость🎲
/ban - забанить участника группы в ответ на его сообщение💩
/info - информация о боте😊
/help - помощь с командами❤
/go - ИГРА В POKEMON GO!🤩\
/Normal - Воспользоваться встроенной клавиатурой!
                 
Я также пересылаю вам картинки которые вы мне отправляете😁
""")

keys = ["1","2","3","4","5","6","7","8","9","0","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
symbols = ["1","2","3","4","5","6","7","8","9","0","!","@","#","$","%","^","&","*","(",")","\'","\"","/","\\",",",".",";",":"]

def keyboard(key_type="Normal"):
    markup = ReplyKeyboardMarkup(row_width=10)
    if key_type == "Normal":
        row = [KeyboardButton(x) for x in keys[:10]]
        markup.add(*row)
        row = [KeyboardButton(x) for x in keys[10:20]]
        markup.add(*row)
        row = [KeyboardButton(x) for x in keys[20:29]]
        markup.add(*row)
        row = [KeyboardButton(x) for x in keys[29:]]
        markup.add(*row)
        markup.add(KeyboardButton("Caps Lock"),KeyboardButton("Symbols"),KeyboardButton("🔙Delete"),KeyboardButton("✅Done"))
    elif key_type == "Symbols":
        row = [KeyboardButton(x) for x in symbols[:10]]
        markup.add(*row)
        row = [KeyboardButton(x) for x in symbols[10:20]]
        markup.add(*row)
        row = [KeyboardButton(x) for x in symbols[20:]]
        markup.add(*row)
        markup.add(KeyboardButton("Caps Lock"),KeyboardButton("Normal"),KeyboardButton("🔙Delete"),KeyboardButton("✅Done"))
    else:
        row = [KeyboardButton(x.upper()) for x in keys[:10]]
        markup.add(*row)
        row = [KeyboardButton(x.upper()) for x in keys[10:20]]
        markup.add(*row)
        row = [KeyboardButton(x.upper()) for x in keys[20:29]]
        markup.add(*row)
        row = [KeyboardButton(x.upper()) for x in keys[29:]]
        markup.add(*row)
        markup.add(KeyboardButton("Normal"),KeyboardButton("Symbols"),KeyboardButton("🔙Delete"),KeyboardButton("✅Done"))
    return markup

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id,"You can use the keyboard",reply_markup=keyboard())





def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Ты подтвердил своё причастие к 43 федеральным приступлениям :)")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(commands=['random_question'])
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())

#get info
@bot.message_handler(commands=['info'])
def information(message):
    bot.reply_to(message, 'Я повторюша дядя хрюша🐷')

#make a doggy
@bot.message_handler(commands=['dog'])
def dog_creator(message):
    arguments = telebot.util.extract_arguments(message.text)
    arguments = arguments.split(' ')
    bobby = Dog(arguments[0], arguments[1], arguments[2])
    bot.reply_to(message, bobby.info())


#throw a dice
stickers = ['CAACAgIAAxkBAAEMB2BmMTRrAAGUBjrhLQWylq4k_9HU-YQAAosVAALvokhL3DAhhLVmmaA0BA',
            'CAACAgIAAxkBAAEMB2JmMTRx5zoGBuExLcmX0L-jXN7FRAACzxEAAlKRQEtOAAGmnvjK7y80BA',
            'CAACAgIAAxkBAAEMB2VmMTR2Acjyi9Q0hfAAARa60VLory4AAkARAAIjrEFLq5rcPQrrUd80BA',
            'CAACAgIAAxkBAAEMB2dmMTR5VDH774vVy7I9FRt4u-_K3wACcREAAuzsQUu1GqzW_T-jpDQE',
            'CAACAgIAAxkBAAEMB2pmMTR8PBGoIUvABEz3n0QfQdr3kAACoQ8AAkG1QUtuwcKEzQGhITQE',
            'CAACAgIAAxkBAAEMB3BmMTR_48NtSA62WmzZMRGoIVciRQAC9g0AAvetSEtWDywqQrcoYzQE']

@bot.message_handler(commands=['dice'])
def throw_a_dice(message):
    global stickers
    bot.send_sticker(message.chat.id, random.choice(stickers))

#clear ban function
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен, пока!😁")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

#resender photos
@bot.message_handler(content_types=['photo'])
def photo(message):   
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
         new_file.write(downloaded_file)
    photo = open('image.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    bot.send_message(message.chat.id, 'Я знаю что ты мне кидаешь😉')

#new members
@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'Я принял нового участника!🥰')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

snacks = 0
counter = 0
pokemon = 0
@bot.message_handler(commands=['go'])
def go(message):
    global snacks, pokemon
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = random.randint(1,3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_message(message.chat.id, 'Обычная версия')
        bot.send_photo(message.chat.id, pokemon.show_img()[0])
        bot.send_message(message.chat.id, 'Светящаяся версия')
        bot.send_photo(message.chat.id, pokemon.show_img()[1])
        bot.send_message(message.chat.id, f'Количество вкусняшек: {snacks}. Чтобы получить вкусняшку, напишите "ВКУСНЯШКА" 10 раз. (с их помощью можно улучшать покемона)')
        bot.send_message(message.chat.id, f'''Прокачать левел: /lvlup
АТАКОВАТЬ КОГО-ТО⚔: /attack
Чекнуть статы покемона: /pokemoninfo''')
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pok = Pokemon.pokemons[message.from_user.username]
            res = pok.fight(enemy)
            bot.send_message(message.chat.id, res)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами")
    else:
            bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")

@bot.message_handler(commands=['pokemoninfo'])
def pokemon_information(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        bot.send_message(message.chat.id, pok.info())

@bot.message_handler(commands=['lvlup'])
def lvlup(message):
    global snacks, pokemon
    feed_interval = 20
    if message.from_user.username in Pokemon.pokemons.keys() and snacks > 0:
        current_time = datetime.now()  
        delta_time = timedelta(hours=feed_interval)  
        if (current_time - pokemon.feed_time) >= delta_time:
            pokemon.level += 1
            snacks -= 1
            pokemon.hp += random.randint(1,100)
            pokemon.damage += random.randint(1,100)
            pokemon.feed_time = current_time
            bot.send_message(message.chat.id, f'Левел покемона повышен! Произошло случайное улучшение характеристик!')
            bot.send_message(message.chat.id, pokemon.info())
            bot.send_message(message.chat.id, f'''Количество вкусняшек: {snacks}.
Чтобы получить вкусняшку, напишите "ВКУСНЯШКА" 10 раз. (с их помощью можно улучшать покемона)''')
            bot.send_message(message.chat.id, f"Следующее время кормления покемона: {pokemon.feed_time+delta_time}")
            bot.send_message(message.chat.id, f'''Прокачать левел: /lvlup
АТАКОВАТЬ КОГО-ТО⚔: /attack
Чекнуть статы покемона: /pokemoninfo''')
        else:
            bot.send_message(message.chat.id, f"Следующее время кормления покемона: {pokemon.feed_time+delta_time}")
    else:
        bot.send_message(message.chat.id, f'НЕДОСТАТОЧНО ВКУСНЯШЕК ИЛИ НЕТУ ПОКЕМОНА!')
        
@bot.message_handler(func=lambda message:True)
def all_messages(message):
    if message.text == "✅Done":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id,"Done with Keyboard",reply_markup=markup)
    elif message.text == "Symbols":
        bot.send_message(message.from_user.id,"Special characters",reply_markup=keyboard("Symbols"))
    elif message.text == "Normal":
        bot.send_message(message.from_user.id,"Normal Keyboard",reply_markup=keyboard("Normal"))
    elif message.text == "Caps Lock":
        bot.send_message(message.from_user.id,"Caps Lock",reply_markup=keyboard("Caps"))
    elif message.text == "🔙Delete":
        bot.delete_message(message.from_user.id,message.message_id)
    else:
        bot.send_message(message.chat.id,message.text)

# Handle all other messages with content_type 'text' (content_types defaults to ['text']) and ban function for links
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global counter, snacks
    if 'https://' in message.text:
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Админ, не шали😤")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен за отправку подозрительных ссылок.")
    elif message.text == 'ВКУСНЯШКА':
        counter+=1
    else:
        bot.reply_to(message, message.text)
    if counter == 10:
        snacks+=1
        counter = 0
        bot.send_message(message.chat.id, f'Получена вкусняшка!')
        bot.send_message(message.chat.id, f'Количество вкусняшек: {snacks}. Чтобы получить вкусняшку, напишите "ВКУСНЯШКА" 10 раз. (с их помощью можно улучшать покемона)')
        bot.send_message(message.chat.id, f'''Прокачать левел: /lvlup
АТАКОВАТЬ КОГО-ТО⚔: /attack
Чекнуть статы покемона: /pokemoninfo''')
    
    print(message.text)



bot.infinity_polling()