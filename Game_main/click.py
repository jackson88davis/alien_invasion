import pygame


class Click:

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/aliens.png')
        self.image = pygame.transform.smoothscale(self.image, (230, 85))
        self.rect = self.image.get_rect()

        self.rect.topleft = self.screen_rect.topleft

    def blitme(self):
        self.screen.blit(self.image, self.rect)