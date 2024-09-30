""" Гра "Вторгнення прибульців". Гравець керує космічним човном, який знищує ворожу армаду. 
    Вороги спускаються по екрану вниз. Якщо хтось з ворогів дістанеться низу екрану, або 
    зачепить човен Героя -- його броня понесе урон. Після трьох ударів човен ламається, 
    а гра закінчується. Вдалих пригод, солдате! (гра розповсюджується за ліцензією WTFPL)"""

import sys
from time import sleep

import pygame

from settings import Settings
from button import Button
from game_stats import GameStats
from score_board import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.sb = Scoreboard(self)

        self.play_button = Button(self, "Грати")
        
    def run_game(self):
        '''Розпочати головний цикл гри'''
        while True:
            self._check_events()
            if not self.stats.game_active:
                pygame.mouse.set_visible(True)
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._check_alien_grounded()
                
            self._update_screen() #Зобразити екран по закінченню циклу

    def _start_game(self):
        self.stats.reset_stats()
        self.stats.game_active = True

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

        self.settings.initialize_dynamic_settings()



    def _check_playbutton(self, mouse_position):
        button_pressed = self.play_button.rect.collidepoint(mouse_position)
        if button_pressed and not self.stats.game_active:
            self._start_game()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            pygame.mouse.set_visible(False)


    def _check_events(self):
        """Event dispatcher"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    self._check_playbutton(mouse_position)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
        self._check_alien_ship_collision()

    def _check_alien_ship_collision(self):
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _ship_hit(self):
        self.stats.ships_left -= 1
        self.sb.prep_ships()

        if self.stats.ships_left > 0:

            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _check_alien_grounded(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_value * len(alien)
            self.sb.prep_score()
            self.sb.check_highscore()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_game_speed()

            self.stats.current_level += 1
            self.sb.prep_level()

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()

    def _create_fleet(self):
        alien = Alien(self)
        self.aliens.add(alien)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width * 3)
        number_of_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        rows_number = available_space_y // (2 * alien_height)

        for row_number in range(rows_number):
            for alien_number in range(number_of_aliens_x):
                self._create_alien(alien_number, row_number)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_descention_speed
        self.settings.fleet_direction *= -1



    def _update_screen(self):
        """Screen updater and image rendering code"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai_game = AlienInvasion()
    ai_game.run_game()
