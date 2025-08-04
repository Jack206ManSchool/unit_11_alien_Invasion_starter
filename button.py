import pygame.font

from typing import TYPE_CHECKING

if TYPE_CHECKING:
        from alien_invasion import AlienInvasion

class Button:

    def __init__(self, game: 'AlienInvasion', msg):
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings

        self.font = pygame.font.Font(self.settings.font_file, 
            self.settings.button_font_size)
        self.rect = pygame.Rect(0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self.highlight_rect = pygame.Rect(0, 0, self.settings.button_w+1, self.settings.button_h+1)
        self.highlight_rect.center = self.boundaries.center
        self.highlight_rect.centerx -= 2
        self.highlight_rect.centery -= 2
        self.shadow_rect = pygame.Rect(0, 0, self.settings.button_w+1, self.settings.button_h+1)
        self.shadow_rect.center = self.boundaries.center
        self.shadow_rect.centerx += 2
        self.shadow_rect.centery += 2
        self.bar_rect = pygame.Rect(0, 0, self.settings.button_w, 20)
        self.bar_rect.center = (self.boundaries.center)
        self.bar_rect.centery -= (self.settings.button_h/2)+10
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, False, self.settings.button_text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.settings.button_highlight_color, self.highlight_rect)
        self.screen.fill(self.settings.button_shadow_color, self.shadow_rect)

        self.screen.fill(self.settings.button_color, self.rect)
        #self.screen.fill(self.settings.bar_color, self.bar_rect)

        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
         return self.rect.collidepoint(mouse_pos)