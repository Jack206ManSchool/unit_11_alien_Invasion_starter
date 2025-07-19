import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class to manage bullets fired from the ship. """

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = self.settings.bullet_image
        self.bullet_resolution = self.settings.bullet_image.get_rect()
        self.is_blast = False
        self.blast_timer = 120
        #self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set the correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width*2, self.settings.bullet_height*2)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a float
        self.y = float(self.rect.y)
    
    def update(self):
        """ Move the bullet up the screen. """
        if self.is_blast == False:
            # Update the exact position of the bullet
            self.y -= self.settings.bullet_speed
            # Update the rect position
            self.rect.y = self.y

    def draw_blast(self):
        """ Move the bullet up the screen. """

    
    def draw_bullet(self):
        """ Draw the bullet to the screen. """
        
        if self.is_blast == False:
            temp1 = 0
            temp2 = 0
            while(temp2 < (self.settings.bullet_height*2)):
                while(temp1 < (self.settings.bullet_width*2)):
                    self.screen.blit(self.settings.bullet_image, ((self.rect.x+temp1, self.rect.y+temp2)))
                    temp1 += self.bullet_resolution.width
                temp1 = 0
                temp2 += self.bullet_resolution.height
        elif self.is_blast == True:
            if self.blast_timer > 0:
                self.screen.blit(self.settings.blast_image, 
                (self.rect.x-(self.settings.blast_rect[3]/2)+((self.settings.bullet_width*self.bullet_resolution[3])/2), 
                self.rect.y+(self.settings.bullet_height*2)))
                self.blast_timer -= 1

        #pygame.draw.rect(self.screen, self.color, self.rect)