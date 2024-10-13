import pytest
from calculate.calculator_program import calculate

# to create html reports for the program
# 1 download essential tools

# pip install pytest pytest-cov
# pip install pytest pytest-html

# 2 go to the repository of your project and execute

# pytest --html=test_report.html
# pytest --cov=. --cov-report html

def test_calculate_addition():
    assert calculate(1, 1, '+') == 2

def test_calculate_division():
    assert calculate(8, 2, '/') == 4

def test_calculate_unknown_operation():
    assert calculate(5, 5, 'unknown') == "Неизвестная операция."

'''
Задача. В настоящий момент реализовано три unit-теста
Проверяется корректность работы калькулятора для действий сложения, деления и неизвестной операции
Необходимо, как минимум, добавить тесты для следующих операций:
1. Вычитание
2. Умножение
Но будет круто, если ты сможешь придумать и добавить дополнительные тесты
'''

def test_calculate_division_by_zero():
    assert calculate(5, 0, '/') == 'Ошибка: Деление на ноль.'

def test_calculate_subtraction():
    assert calculate(10, 5, '-') == 5

def test_calculate_multiplication():
    assert calculate(4, 2, '*') == 8