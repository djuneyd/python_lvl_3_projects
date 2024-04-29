import random

class Dog:
    def __init__(self, name, breed, temper):
        self.name = name
        self.breed = breed
        self.temper = temper

    def info(self):
        print(f'name: {self.name}, breed: {self.breed}, temper: {self.temper}')

    def eat(self):
        food = ['bone', 'steak', 'chicken wing', 'snack', 'cake']
        print(f'{self.name} decided to have a {random.choice(food)}')

    def play(self):
        activities = ['go for a walk', 'play with ball', 'play hide and seek', 'sleep']
        print(f'{self.name} wants to {random.choice(activities)}')
bobby = Dog('bobby', 'american hairless terrier', 'kind')

bobby.info()
bobby.eat()
bobby.play()