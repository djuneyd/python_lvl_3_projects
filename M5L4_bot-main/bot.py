import os
import telebot
from logic import process_image
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Отправьте мне фото, и я замаскирую лица на нем.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # Получаем файл фотографии
        file_id = message.photo[-1].file_id 
        file_info = bot.get_file(file_id)
        file_ext = '.jpg'

        # Скачиваем файл
        downloaded_file = bot.download_file(file_info.file_path)

        # Сохраняем файл локально
        input_file_path = f"input{file_ext}"
        with open(input_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Задаем имя выходного файла
        output_file_path = f"output{file_ext}"

        # Обрабатываем файл (размытие лиц)
        process_image(input_file_path, output_file_path)

        # Отправляем обратно результат в виде фото
        with open(output_file_path, 'rb') as processed_photo:
            bot.send_photo(message.chat.id, processed_photo)

        # Удаляем временные файлы
        os.remove(input_file_path)
        os.remove(output_file_path)

        # Удаляем сообщение с фото из чата
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Отправьте мне фото, и я размою лица на нем.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
