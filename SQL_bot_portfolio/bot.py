import telebot
import  config
API_TOKEN = config.TOKEN

bot = telebot.TeleBot(API_TOKEN)





bot.infinity_polling()