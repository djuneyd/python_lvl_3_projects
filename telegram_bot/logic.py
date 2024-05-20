from random import randint
import requests

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.level = 0
        self.hp = randint(1,1000)
        self.damage = randint(200,500)
        self.rase = 'Common'

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        pics = []
        if response.status_code == 200:
            data = response.json()
            pics.append(data['sprites']['other']['official-artwork']['front_default'])
            pics.append(data['sprites']['other']['official-artwork']['front_shiny'])
        return pics
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"


    # Метод класса для получения информации
    def info(self):
        return f'''Имя твоего покеомона: {self.name}
Класс твоего покеомона: {self.rase}
Левел покемона: {self.level}
Здоровье покемона: {self.hp}
Урон покемона: {self.damage}'''

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

    def lvl(self):
        return self.level
    
    def health(self):
        return self.hp
    
    def attack(self):
        return self.damage
    
    def fight(self, enemy):
        if enemy.hp > 0:
            if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
                chanse = randint(1,5)
                if chanse == 1:
                    return "Покемон-волшебник применил щит в сражении, урон не прошёл!"
                
            if isinstance(self, Fighter):
                ulta = randint(200,500)
                self.damage += ulta
                if enemy.hp > self.damage:
                    enemy.hp -= self.damage
                    self.damage -= ulta
                    return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer} Боец применил супер-атаку силой:{ulta}"
                else:
                    enemy.hp = 0
                    self.damage -= ulta
                    return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! Боец применил супер-атаку силой:{ulta}"
            if isinstance(self, Pokemon):
                if enemy.hp > self.damage:
                    enemy.hp -= self.damage
                    return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
                else:
                    enemy.hp = 0
                    return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!"
        else:
            return 'СОПЕРНИК СДОХ!'
        
class Fighter(Pokemon):
    def __init__(self, pokemon_trainer):
        super(Fighter, self).__init__(pokemon_trainer)
        self.pokemon_trainer = pokemon_trainer
        self.rase = 'Fighter'
    pass
class Wizard(Pokemon):
    def __init__(self, pokemon_trainer):
        super(Wizard, self).__init__(pokemon_trainer)
        self.rase = 'Wizard'
        self.pokemon_trainer = pokemon_trainer
    pass

if __name__ == '__main__':
    wizard = Wizard("username1")
    fighter = Fighter("username2")
    common = Pokemon('username3')

    print(wizard.info())
    print()
    print(fighter.info())
    print()
    print(common.info())
    print(common.fight(wizard))