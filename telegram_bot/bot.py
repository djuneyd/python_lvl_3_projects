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
/info - информация о боте😊
/help - помощь с командами❤\
                 
Я также пересылаю вам картинки которые вы мне отправляете😁
""")

@bot.message_handler(commands=['info'])
def send_welcome(message):
    bot.reply_to(message, 'Я повторюша дядя хрюша🐷')

@bot.message_handler(commands=['dog'])
def send_welcome(message):
    arguments = telebot.util.extract_arguments(message.text)
    arguments = arguments.split(' ')
    bobby = Dog(arguments[0], arguments[1], arguments[2])
    bot.reply_to(message, bobby.info())

stickers = ['CAACAgIAAxkBAAEMB2BmMTRrAAGUBjrhLQWylq4k_9HU-YQAAosVAALvokhL3DAhhLVmmaA0BA',
            'CAACAgIAAxkBAAEMB2JmMTRx5zoGBuExLcmX0L-jXN7FRAACzxEAAlKRQEtOAAGmnvjK7y80BA',
            'CAACAgIAAxkBAAEMB2VmMTR2Acjyi9Q0hfAAARa60VLory4AAkARAAIjrEFLq5rcPQrrUd80BA',
            'CAACAgIAAxkBAAEMB2dmMTR5VDH774vVy7I9FRt4u-_K3wACcREAAuzsQUu1GqzW_T-jpDQE',
            'CAACAgIAAxkBAAEMB2pmMTR8PBGoIUvABEz3n0QfQdr3kAACoQ8AAkG1QUtuwcKEzQGhITQE',
            'CAACAgIAAxkBAAEMB3BmMTR_48NtSA62WmzZMRGoIVciRQAC9g0AAvetSEtWDywqQrcoYzQE']

@bot.message_handler(commands=['dice'])
def send_welcome(message):
    global stickers
    bot.send_sticker(message.chat.id, random.choice(stickers))

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

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)
    print(message.text)



bot.infinity_polling()