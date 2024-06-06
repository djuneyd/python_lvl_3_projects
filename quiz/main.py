import telebot
from config import token
# Задание 7 - испортируй команду defaultdict
from collections import defaultdict
from logic import quiz_questions

user_responses = {} 
# Задание 8 - создай словарь points для сохранения количества очков пользователя
points = defaultdict(int)

bot = telebot.TeleBot(token)

def send_question(chat_id):
    bot.send_message(chat_id, {quiz_questions[user_responses[chat_id]].text} , reply_markup=quiz_questions[user_responses[chat_id]].gen_markup())

i=1
us = ''
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global i, us
    if call.from_user.id == us:
        i+=1
        if call.data == "correct":
            bot.answer_callback_query(call.id, "Answer is correct")
            # Задание 9 - добавь очки пользователю за правильный ответ
            points[call.from_user.id] += 1
        elif call.data == "wrong":
            bot.answer_callback_query(call.id,  "Answer is wrong")
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        # Задание 5 - реализуй счетчик вопросов
        user_responses[call.message.chat.id]+=1
        # Задание 6 - отправь пользователю сообщение с количеством его набранных очков, если он ответил на все вопросы, а иначе отправь следующий вопрос
        if user_responses[call.message.chat.id]>=len(quiz_questions):
            bot.send_message(call.message.chat.id, f"The end, your points: {points[call.from_user.id]}")
        else:
            photo = open(f'quiz\sk{i}.jpg', 'rb')
            bot.send_photo(call.message.chat.id, photo)
            send_question(call.message.chat.id)

@bot.message_handler(commands=['start'])
def start(message):
    global i, us
    if message.chat.id in user_responses.keys():
        if i==4:
            del user_responses[message.chat.id]
        else:
            bot.send_message(message.chat.id, "СНАЧАЛА ЗАВЕРШИ ПРЕДЫДУЩИЙ КВИЗ!!!")
            bot.delete_message(message.chat.id, message.message_id)
    if message.chat.id not in user_responses.keys():
        user_responses[message.chat.id] = 0
        points[message.from_user.id] = 0
        i = 1
        us = message.from_user.id
        photo = open(f'quiz\sk{i}.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        send_question(message.chat.id)


bot.infinity_polling()
