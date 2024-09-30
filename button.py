import pygame.font

class Button:
    def __init__(self, ai_game, msg):
        #Налаштування екрану
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #Розмір та колір кніпки
        self.width, self.height = 250, 60
        self.text_color = (255, 255, 255)
        self.button_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        #Розмістити кніпку на екрані
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #Текст на кнопці
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        #Рендер тексту в зображення, розміщення
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)