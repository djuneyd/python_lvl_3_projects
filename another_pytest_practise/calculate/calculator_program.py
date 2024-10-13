def calculate(num1, num2, operation):
    if operation == '+':
        return num1 + num2
    elif operation == '-':
        return num1 - num2
    elif operation == '*':
        return num1 * num2
    elif operation == '/':
        if num2 != 0:
            return num1 / num2
        else:
            return "Ошибка: Деление на ноль."
    else:
        return "Неизвестная операция."


def main():
    print("Простой калькулятор. Введите два числа и выберите операцию.")
    num1 = float(input("Введите первое число: "))
    num2 = float(input("Введите второе число: "))
    operation = input("Выберите операцию (+, -, *, /): ")
    result = calculate(num1, num2, operation)
    print(f"Результат: {result}")


if __name__ == "__main__":
    main()
