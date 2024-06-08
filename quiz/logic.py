# Задание 2 - Импортируй нужные классы
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Question:

    def __init__(self, text, answer_id, *options):
        self.__text = text
        self.__answer_id = answer_id
        self.options = options

    # Задание 1 - Создай геттер для получения текста вопроса
    @property
    def text(self):
            return self.__text
    
    def gen_markup(self):
        # Задание 3 - Создай метод для генерации Inline клавиатуры
        markup = InlineKeyboardMarkup()
        markup.row_width = len(self.options)

        for i, option in enumerate(self.options[0:-1]):
            if i == self.__answer_id:
                markup.add(InlineKeyboardButton(option, callback_data='correct'))
            else:
                markup.add(InlineKeyboardButton(option, callback_data='wrong'))
        return markup

# Задание 4 - заполни список своими вопросами
quiz_questions = [
    Question("Какая порода котиков лысая?", 1, "Британцы", "Сфинксы", "task1.jpg"),
    Question("Какой породы котики знают английский?", 0, "Британцы", "Ориенталы", "Сфинксы", "task2.jpg"),
    Question("Что не любит большинскво котиков?", 3, "Читать", "Спать", "Есть", "Воду", "task3.jpg")
]
 