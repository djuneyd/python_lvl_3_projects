import config
from class_dz import Dog
import random
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
/help - помощь с командами❤\
                 
Я также пересылаю вам картинки которые вы мне отправляете😁
""")

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

# Handle all other messages with content_type 'text' (content_types defaults to ['text']) and ban function for links
@bot.message_handler(func=lambda message: True)
def echo_message(message):
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
    else:
        bot.reply_to(message, message.text)
    print(message.text)



bot.infinity_polling()