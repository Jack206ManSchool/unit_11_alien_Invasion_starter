import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
from alien_fleet import AlienFleet
from time import sleep
from button import Button
from hud import HUD

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )

        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
        )

        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)
        
        self.crashed_ship_sound = pygame.mixer.Sound(self.settings.crashed_ship_sound)
        self.crashed_ship_sound.set_volume(0.7)

        self.winning_sound = pygame.mixer.Sound(self.settings.winning_sound)
        self.winning_sound.set_volume(0.8)

        self.gameover_sound = pygame.mixer.Sound(self.settings.gameover_sound)
        self.gameover_sound.set_volume(0.8)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet(False)

        self.play_button = Button(self, 'Play')
        self.game_active = False

        self.finished_intro = False

    def run_game(self):
        # Game loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_collisions(self):
        # Check collisions for ship
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            # subtrack one life if possable

        # Check collisions for aliens and bottom of screen
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()

        # Check collisions of projectiles and aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(250)
            self.game_stats.update(collisions)
            self.HUD.update_scores()
        
        if self.alien_fleet.check_destroyed_status():
            self._reset_level(False)
            self.settings.increase_difficulty()
            # Update game stats level
            self.game_stats.update_level()
            # Update HUD view
            self.HUD.update_level()
            self.winning_sound.play()
            sleep(1.25)

    def _check_game_status(self):
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level(False)
            self.crashed_ship_sound.play()
            self.ship.has_crashed = True
            self._update_screen()
            sleep(1)
            self.ship.has_crashed = False
        else:
            self.crashed_ship_sound.play()
            self.ship.has_crashed = True
            self._update_screen()
            sleep(1)
            self.gameover_sound.play()
            sleep(2.0)
            self.ship.has_crashed = False
            self.game_active = False


    def _reset_level(self, start_mode):
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet(start_mode)

    def restart_game(self):
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self.ship._center_ship()
        self._reset_level(True)
        self.game_active = True
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        self._render_Background()
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        if not self.game_active and not self.finished_intro:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(250)
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()

    def _render_Background(self):
        """ Make a background using a continuously repeating image. (uses background.png) """
        bg_w_counter = 0
        bg_h_counter = 0
        bg_image = pygame.image.load(self.settings.bg_file)
        bg_rect = bg_image.get_rect()
        while(bg_h_counter <= (self.settings.screen_h)):
            while(bg_w_counter <= (self.settings.screen_w)):
                self.screen.blit(bg_image, (bg_w_counter, bg_h_counter))
                bg_w_counter += bg_rect.width
            bg_w_counter = 0
            bg_h_counter += bg_rect.height

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
