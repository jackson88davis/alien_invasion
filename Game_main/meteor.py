import pygame
from pygame.sprite import Sprite
from random import randint


class Meteor(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/meteor.png')
        self.image = pygame.transform.scale(self.image, (150, 200))
        self.rect = self.image.get_rect()

        self.rect.bottom = self.screen.get_rect().top
        meteor_left_max = self.settings.screen_height - self.rect.height
        self.rect.left = randint(0, meteor_left_max)

        self.y = float(self.rect.y)

    def update(self):
        self.y += self.settings.meteor_speed
        self.rect.y = self.y
