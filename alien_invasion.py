import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """ Overall class to manage game assets and behavior. """
    def __init__(self):
        """ Initalize the game, and create game resources. """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # True = Fullscreen, False = Windowed
        self.screenModeToggle = False
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def screenMode(self, inputBool):
        if(inputBool == False):
            self.settings.setScreenRes(self.settings.displayResolutionMode, self.ship)
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            self.ship.screenResCalc(self, True)
        elif(inputBool == True):
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.setScreenRes(0, self.ship, self.screen.get_rect().width, self.screen.get_rect().height)

    def run_game(self):
        """ Start the main loop for the game. """
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """ Respond to keypresses. """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_f:
            if(self.screenModeToggle == True):
                self.screenModeToggle = False
            else:
                self.screenModeToggle = True
            self.screenMode(self.screenModeToggle)

    def _check_keyup_events(self, event):
        """ Respond to key releases. """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group. """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update position of bullets and get rid of old bullets. """
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                bullet.is_blast = True 
            if bullet.blast_timer <= 0:
                self.bullets.remove(bullet)
        #print(len(self.bullets))

    def _update_screen(self):
            """ Update images on screen, and flip to the new screen. """
            self._render_Background()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()

            pygame.display.flip()

    def _render_Background(self):
        """ Make a background using a continuously repeating image. (uses background.bmp) """
        bg_w_counter = 0
        bg_h_counter = 0
        while(bg_h_counter <= (self.settings.screen_height)):
            while(bg_w_counter <= (self.settings.screen_width)):
                self.screen.blit(self.settings.bg_image, (bg_w_counter, bg_h_counter))
                bg_w_counter += self.settings.bg_rect.width
            bg_w_counter = 0
            bg_h_counter += self.settings.bg_rect.height
        #self.screen.fill(self.settings.bg_color)

if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()