import random

class Dog:
    def __init__(self, name, breed, temper):
        self.name = name
        self.breed = breed
        self.temper = temper

    def info(self):
        return f'имя: {self.name}, порода: {self.breed}, характер: {self.temper}'

    def eat(self):
        food = ['косточка', 'стейк', 'куринное крылышко', 'корм', 'тортик']
        return f'{self.name} решил(-ла) полакомиться {random.choice(food)}'

    def play(self):
        activities = ['пойти погулять', 'поиграть с мячиком', 'поиграть в прятки', 'поспать']
        return f'{self.name} хочет {random.choice(activities)}'