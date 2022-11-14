import sys
from time import sleep
from random import random
import pygame
from pygame import mixer

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from hs import Hs
from button import Button
from quit import Quit
from title import Title
from instructions import Instructions
from instructions_open import Instructions_open
from click import Click
from creator import Creator
from background import Background
from background1 import Background1
from character import Character
from bullet import Bullet
from bullet1 import Bullet1
from shield import Shield
from alien import Alien
from alien1 import Alien1
from meteor import Meteor
from blue_planet_move_left import Blue_Planet_Move_Left
from blue_planet_move_right import Blue_Planet_Move_Right


class Game:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Game")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.background = Background(self)
        self.background1 = Background1(self)
        self.click = Click(self)
        self.character = Character(self)
        self.bullets = pygame.sprite.Group()
        self.bullet1s = pygame.sprite.Group()
        self.shields = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien1s = pygame.sprite.Group()
        self.meteors = pygame.sprite.Group()
        self.blue_planet_move_lefts = pygame.sprite.Group()
        self.blue_planet_move_rights = pygame.sprite.Group()

        self.mixer = mixer
        self.alien_sound = pygame.mixer.Sound('sounds/alien_sound.wav')
        self.click_sound = pygame.mixer.Sound('sounds/click_sound.ogg')
        self.confirmation_sound = pygame.mixer.Sound('sounds/confirmation_sound.ogg')
        self.explosion_sound = pygame.mixer.Sound('sounds/explosion_sound.mp3')
        self.hey_sound = pygame.mixer.Sound('sounds/hey_sound.mp3')
        self.hi_sound = pygame.mixer.Sound('sounds/hi_sound.mp3')
        self.instructions_sound = pygame.mixer.Sound('sounds/instructions_sound.wav')
        self.laser_sound = pygame.mixer.Sound('sounds/laser_sound.ogg')
        self.loss_sound = pygame.mixer.Sound('sounds/loss_sound.wav')
        self.meteor_explosion_sound = pygame.mixer.Sound('sounds/meteor_explosion_sound.ogg')
        self.meteor_strike_sound = pygame.mixer.Sound('sounds/meteor_strike_sound.wav')
        self.ouch_sound = pygame.mixer.Sound('sounds/ouch_sound.mp3')
        self.quit_sound = pygame.mixer.Sound('sounds/quit_sound.mp3')
        self.shield_sound = pygame.mixer.Sound('sounds/shield_sound.mp3')
        self.stop_sound = pygame.mixer.Sound('sounds/stop_sound.mp3')
        self.what_sound = pygame.mixer.Sound('sounds/what_sound.mp3')

        pygame.mixer.music.load('sounds/music.mp3')
        pygame.mixer.music.set_volume(0.5)

        self.play_button = Button(self, "Play")
        self.play_quit = Quit(self, "Quit")
        self.play_title = Title(self, "-Planetary Panic-")
        self.play_instructions = Instructions(self, "Instructions")
        self.play_instructions_open = Instructions_open(self, "Controls")
        self.play_creator = Creator(self, "D-a-v-i-s     S-t-u-d-i-o-s")
        self.play_hs = Hs(self, "HIGH SCORE!")
        self.play_click = Click(self)

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.character.update()
                self._update_bullets()
                self._update_bullet1s()
                self._update_shields()
                self._create_alien()
                self._update_aliens()
                self._create_alien1()
                self._update_alien1s()
                self._create_meteor()
                self._update_meteors()
                self._create_blue_planet_move_left()
                self._update_blue_planet_move_lefts()
                self._create_blue_planet_move_right()
                self._update_blue_planet_move_rights()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            if event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_quit(mouse_pos)
                self._check_instructions(mouse_pos)
                self._check_click(mouse_pos)

    def _check_play_button(self, mouse_pos):
        pygame.mixer.Sound.play(self.click_sound)
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            pygame.mixer.Sound.play(self.confirmation_sound)
            pygame.mixer.music.play(-1)
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_characters()

            self.aliens.empty()
            self.alien1s.empty()
            self.meteors.empty()
            self.blue_planet_move_lefts.empty()
            self.blue_planet_move_rights.empty()

            self._create_alien()
            self._create_alien1()
            self._create_meteor()
            self._create_blue_planet_move_left()
            self._create_blue_planet_move_right()
            self.character.midbottom_character()

            pygame.mouse.set_visible(False)

    def _check_quit(self, mouse_pos):
        quit_clicked = self.play_quit.rect.collidepoint(mouse_pos)
        if quit_clicked:
            pygame.mixer.Sound.play(self.quit_sound)
            sleep(1)
            sys.exit()

    def _check_instructions(self, mouse_pos):
        instructions_clicked = self.play_instructions.rect.collidepoint(mouse_pos)
        if instructions_clicked:
            pygame.mixer.Sound.play(self.instructions_sound)
            sleep(1)
            self.play_instructions_open.draw_instructions_open()

    def _check_click(self, mouse_pos):
        click_clicked = self.play_click.rect.collidepoint(mouse_pos)
        if click_clicked:
            pygame.mixer.Sound.play(self.stop_sound)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = True
        if event.key == pygame.K_LEFT:
            self.character.moving_left = True
        if event.key == pygame.K_d:
            self._fire_bullet()
        if event.key == pygame.K_a:
            self._fire_bullet1()
        if event.key == pygame.K_w:
            self._fire_shield()
        if event.key == pygame.K_ESCAPE:
            pygame.mixer.Sound.play(self.quit_sound)
            sleep(1)
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.character.moving_right = False
        if event.key == pygame.K_LEFT:
            self.character.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            pygame.mixer.Sound.play(self.laser_sound)

    def _update_bullets(self):
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            self.bullets.empty()
            self._create_alien()
            self.settings.increase_speed()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _fire_bullet1(self):
        if len(self.bullet1s) < self.settings.bullet1s_allowed:
            new_bullet1 = Bullet1(self)
            self.bullet1s.add(new_bullet1)
            pygame.mixer.Sound.play(self.laser_sound)

    def _update_bullet1s(self):
        self.bullet1s.update()

        for bullet1 in self.bullet1s.copy():
            if bullet1.rect.left <= 0:
                self.bullet1s.remove(bullet1)

        self._check_bullet1_alien1_collisions()

    def _check_bullet1_alien1_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullet1s, self.alien1s, True, True)
        if collisions:
            self.bullet1s.empty()
            self._create_alien1()
            self.settings.increase_speed()
            for alien1s in collisions.values():
                self.stats.score += self.settings.alien1_points * len(alien1s)
            self.sb.prep_score()
            self.sb.check_high_score()

    def _fire_shield(self):
        if len(self.shields) < self.settings.shields_allowed:
            new_shield = Shield(self)
            self.shields.add(new_shield)
            pygame.mixer.Sound.play(self.shield_sound)

    def _update_shields(self):
        self.shields.update()

        for shield in self.shields.copy():
            if shield.rect.left <= 0:
                self.shields.remove(shield)

        self._check_shields_top()
        self._check_shield_meteor_collisions()

    def _check_shields_top(self):
        for shield in self.shields.sprites():
            if shield.rect.top < 0:
                self.shields.empty()

    def _check_shield_meteor_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.shields, self.meteors, True, True)
        if collisions:
            self.shields.empty()
            self._create_meteor()
            self.settings.increase_speed()
            for meteors in collisions.values():
                self.stats.score += self.settings.meteor_points * len(meteors)
            self.sb.prep_score()
            self.sb.check_high_score()
            pygame.mixer.Sound.play(self.meteor_explosion_sound)

    def _create_alien(self):
        if random() < self.settings.alien_frequency:
            alien = Alien(self)
            self.aliens.add(alien)
            pygame.mixer.Sound.play(self.alien_sound)

    def _update_aliens(self):
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.character, self.aliens):
            pygame.mixer.Sound.play(self.ouch_sound)
            sleep(.6)
            self._character_hit()

    def _create_alien1(self):
        if random() < self.settings.alien1_frequency:
            alien1 = Alien1(self)
            self.alien1s.add(alien1)
            pygame.mixer.Sound.play(self.alien_sound)

    def _update_alien1s(self):
        self.alien1s.update()
        if pygame.sprite.spritecollideany(self.character, self.alien1s):
            pygame.mixer.Sound.play(self.ouch_sound)
            sleep(.6)
            self._character_hit()

    def _create_meteor(self):
        if random() < self.settings.meteor_frequency:
            meteor = Meteor(self)
            self.meteors.add(meteor)
            pygame.mixer.Sound.play(self.meteor_strike_sound)

    def _update_meteors(self):
        self.meteors.update()
        if pygame.sprite.spritecollideany(self.character, self.meteors):
            pygame.mixer.Sound.play(self.explosion_sound)
            sleep(.6)
            self._character_hit()

    def _create_blue_planet_move_left(self):
        if random() < self.settings.blue_planet_move_left_frequency:
            pygame.mixer.Sound.play(self.hey_sound)
            blue_planet_move_left = Blue_Planet_Move_Left(self)
            self.blue_planet_move_lefts.add(blue_planet_move_left)

    def _update_blue_planet_move_lefts(self):
        self.blue_planet_move_lefts.update()

    def _create_blue_planet_move_right(self):
        if random() < self.settings.blue_planet_move_right_frequency:
            pygame.mixer.Sound.play(self.hi_sound)
            blue_planet_move_right = Blue_Planet_Move_Right(self)
            self.blue_planet_move_rights.add(blue_planet_move_right)

    def _update_blue_planet_move_rights(self):
        self.blue_planet_move_rights.update()

    def _character_hit(self):
        if self.stats.characters_left > 0:
            self.stats.characters_left -= 1
            self.sb.prep_characters()

            self.bullets.empty()
            self.bullet1s.empty()
            self.shields.empty()
            self.aliens.empty()
            self.alien1s.empty()
            self.meteors.empty()
            self.blue_planet_move_lefts.empty()
            self.blue_planet_move_rights.empty()

            self.character.midbottom_character()
        else:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(self.loss_sound)
            pygame.mixer.Sound.play(self.what_sound)
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        self.background1.blitme()
        self.background.blitme()
        self.character.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet1 in self.bullet1s.sprites():
            bullet1.draw_bullet1()
        for shield in self.shields.sprites():
            shield.draw_shield()

        self.aliens.draw(self.screen)
        self.alien1s.draw(self.screen)
        self.meteors.draw(self.screen)
        self.blue_planet_move_lefts.draw(self.screen)
        self.blue_planet_move_rights.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.click.blitme()
            self.play_button.draw_button()
            self.play_quit.draw_quit()
            self.play_instructions.draw_instructions()
            self.play_title.draw_title()
            self.play_creator.draw_creator()
            if self.sb.stats.score > 0 and self.sb.stats.score >= self.sb.stats.high_score:
                self.play_hs.draw_hs()
            if self.sb.stats.score > 0 and self.sb.stats.score >= self.sb.stats.high_score:
                self.play_instructions_open.draw_instructions_open()

        pygame.display.flip()


if __name__ == '__main__':
    ai = Game()
    ai.run_game()
