import sys
from random import random
import pygame

from settings import Settings
from game_stats import GameStats
from rocket import Rocket
from bullet import Bullet
from alien import Alien

class homework2:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("homework2")

        self.stats = GameStats(self)

        self.rocket = Rocket(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.bg_color = (80, 83, 212)

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self._create_alien()
                self.rocket.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_UP:
            self.rocket.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_UP:
            self.rocket.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

    def _create_alien(self):
        if random() < self.settings.alien_frequency:
            alien = Alien(self)
            self.aliens.add(alien)

    def _update_aliens(self):
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.rocket, self.aliens):
            self._rocket_hit()

        self._check_aliens_left_edge()

    def _check_aliens_left_edge(self):
        for alien in self.aliens.sprites():
            if alien.rect.left < 0:
                self._rocket_hit()
                break

    def _rocket_hit(self):
        if self.stats.rockets_left > 0:
            self.stats.rockets_left -= 1

            self.aliens.empty()
            self.bullets.empty()

            self.rocket.midleft_rocket()
        else:
            self.stats.game_active = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.rocket.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        pygame.display.flip()

if __name__ == '__main__':
    ai = homework2()
    ai.run_game()