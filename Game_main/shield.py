import pygame
from pygame.sprite import Sprite


class Shield(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.shield_color

        self.rect = pygame.Rect(0, 0, self.settings.shield_width,
                                self.settings.shield_height)
        self.rect.midtop = ai_game.character.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.shield_speed
        self.rect.y = self.y

    def draw_shield(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
