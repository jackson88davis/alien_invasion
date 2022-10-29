import sys
import pygame

from settings import Settings
from character import Character
from rocket import Rocket

class homework:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("homework")

        self.character = Character(self)
        self.rocket = Rocket(self)
        self.stars = pygame.sprite.Group()

        self._create_fleet()

        self.bg_color = (80, 83, 212)

    def _create_fleet(self):
        star = Star(self)
        self.stars.add(star)

    def run_game(self):
        while True:
            self._check_events()
            self.rocket.update()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.rocket.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.rocket.moving_left = True
                if event.key == pygame.K_UP:
                    self.rocket.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.rocket.moving_down = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.rocket.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.rocket.moving_left = False
                if event.key == pygame.K_UP:
                    self.rocket.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.rocket.moving_down = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.character.blitme()
        self.rocket.blitme()
        self.stars.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    ai = homework()
    ai.run_game()