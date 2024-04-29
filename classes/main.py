import random # пкм на random и перейти к определению, открываем класс тобиж исходный код (начинка библиотеки)


class Car: # Шаблон/параметры

    def __init__(self, color, brand): # Запись параметрых данных пользователем
        self.color = color
        self.brand = brand

    def go(self): # self сам себя, экземпдяр подставляется в функцию
        print("Go")

    def stop(self):
        print("Stop")

    def info(self):
        print("цвет машины: ", self.color, ", марка машины: ", self.brand)

black_car = Car('black', 'prius') # Экземпляр/изменение параметров
black_car.info()

# practice
class Student:
    def __init__(self, name, surname, group_name, course, progress):
        self.name = name
        self.surname = surname
        self.group_name = group_name
        self.course = course
        self.progress = progress

    def info(self):
        print(f'name: {self.name}, surname: {self.surname}, group name: {self.group_name}, course: {self.course}, progress: {self.progress}')

    def expulsion(self):
        print(f'student: {self.name} {self.surname} is no longer a student :)')

student1 = Student('djuneyd', 'ganbarov', 'СБ-14', 'python lvl 3', 'legend 4')
student2 = Student('dima', 'dairovich', 'СБ-14', 'python lvl 3', 'legend 1')
student3 = Student('biba', 'aboba', 'СБ-14', 'python lvl 3', 'pro 4')

student1.info()
student2.info()
student3.info()