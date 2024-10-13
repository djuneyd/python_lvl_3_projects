# test_string_reverser.py

import pytest
from string_reverser import reverse_string

# Тестирование функции reverse_string на обычной строке.
def test_reverse_string_normal():
    assert reverse_string("hello") == "olleh", "Ожидается, что строка 'hello' будет перевернута в 'olleh'"

# Проверяется корректность работы функции reverse_string при наличии пробелов в строке.
def test_reverse_string_with_spaces():
    assert reverse_string("hello world") == "dlrow olleh", "Ожидается, что строка 'hello world' будет перевернута в 'dlrow olleh'"

# Важно убедиться, что функция reverse_string корректно обрабатывает пустую строку, не вызывая ошибок.
def test_reverse_string_empty():
    assert reverse_string("") == "", "Ожидается, что пустая строка будет перевернута в пустую строку"
