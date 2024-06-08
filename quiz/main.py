import telebot
from config import token
# Задание 7 - испортируй команду defaultdict
from collections import defaultdict
from logic import quiz_questions

user_responses = {} 
num_of_questions = {}
# Задание 8 - создай словарь points для сохранения количества очков пользователя
points = defaultdict(int)

bot = telebot.TeleBot(token)

def send_question(chat_id, usid, name):
    bot.send_message(chat_id, {quiz_questions[user_responses[usid]].text + ' ' + '@' + str(name) + ' tg id: ' + str(usid)}, reply_markup=quiz_questions[user_responses[usid]].gen_markup())
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if str(call.from_user.id) in call.message.text:
        num_of_questions[call.from_user.id] += 1
        if call.data == "correct":
            bot.answer_callback_query(call.id, "Answer is correct")
            # Задание 9 - добавь очки пользователю за правильный ответ
            points[call.from_user.id] += 1
        elif call.data == "wrong":
            bot.answer_callback_query(call.id,  "Answer is wrong")
        bot.delete_message(call.message.chat.id, call.message.message_id-1)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        # Задание 5 - реализуй счетчик вопросов
        user_responses[call.from_user.id]+=1
        # Задание 6 - отправь пользователю сообщение с количеством его набранных очков, если он ответил на все вопросы, а иначе отправь следующий вопрос
        if user_responses[call.from_user.id]>=len(quiz_questions):
            bot.send_message(call.message.chat.id, f"The end, {call.message.text.split()[-4] + ' ' + call.message.text.split()[-2] + ' ' + call.message.text.split()[-1]} points: {points[call.from_user.id]}")
        else:
            photo = open(f'quiz\sk{num_of_questions[call.from_user.id]}.jpg', 'rb')
            bot.send_photo(call.message.chat.id, photo)
            send_question(call.message.chat.id, call.from_user.id, call.from_user.username)
    else:
        bot.send_message(call.message.chat.id, f'''ЭТОТ КВИЗ ПРИНАДЛЕЖИТ {call.message.text.split()[-4] + ' ' + call.message.text.split()[-2] + ' ' + call.message.text.split()[-1]}
Нажмите /start чтобы начать свой квиз❗''')

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in user_responses.keys():
        if num_of_questions[message.from_user.id]==4:
            del user_responses[message.from_user.id]
            del num_of_questions[message.from_user.id]
        else:
            bot.send_message(message.chat.id, f'''СНАЧАЛА ЗАВЕРШИ ПРЕДЫДУЩИЙ КВИЗ!!! @{message.from_user.username} id: {message.from_user.id}
Если что то пошло не так сотри свои данные командой /clear потом снова нажми /start''')
            bot.delete_message(message.chat.id, message.message_id)
    if message.from_user.id not in user_responses.keys():
        user_responses[message.from_user.id] = 0
        points[message.from_user.id] = 0
        num_of_questions[message.from_user.id] = 1
        photo = open(f'quiz\sk{num_of_questions[message.from_user.id]}.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        send_question(message.chat.id, message.from_user.id, message.from_user.username)

@bot.message_handler(commands=['clear'])
def clear(message):
    if message.from_user.id in user_responses.keys():
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f'Данные @{message.from_user.username} id: {message.from_user.id} успешно удалены!!!')
        del user_responses[message.from_user.id]
        del num_of_questions[message.from_user.id]
    else:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, '''У тебя ещё нету данных 😋
/start чтобы начать''')
bot.infinity_polling()