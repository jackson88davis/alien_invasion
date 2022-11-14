import pygame
from pygame.sprite import Sprite


class Blue_Planet_Move_Right(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/blue_planet_right.png')
        self.rect = self.image.get_rect()

        self.rect.topleft = self.screen.get_rect().topright

        self.x = float(self.rect.x)

    def update(self):
        self.x -= self.settings.blue_planet_move_right_speed
        self.rect.x = self.x
