'''Налаштування до гри "Вторгнення прибульців"'''

class Settings:
    def __init__(self):
        """Ініціалізуємо налаштування гри"""

        #Налаштування екрану
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230) #Виставити пізніше на 3, 10, 70

        #Налаштування корабля
        self.ships_limit = 3

        #Налаштування кулі
        self.bullet_width = 3.0
        self.bullet_height = 5.0
        self.bullet_color = (14, 88, 60)
        self.bullets_allowed = 5

        #Налаштування прибульця
        self.fleet_descention_speed = 17

        #Налаштування складності
        self.game_speed_up_scale = 2
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #Змінні налаштування
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.alien_speed = 0.7
        self.fleet_direction = 1
        self.alien_value = 10

    def increase_game_speed(self):
        self.ship_speed *= self.game_speed_up_scale
        self.bullet_speed *= self.game_speed_up_scale
        self.alien_speed *= self.game_speed_up_scale

        self.alien_value = int(self.alien_value * self.score_scale)
