from pygame import image
import ship

class Settings: 
    """ A class to store all settings for Alien Invasion. """

    def __init__(self):
        """ Initialize the game's settings. """
        # Screen settings
        
        # The resolution was glitching out a bit because of my choice of display.
        # Because of this, I added a simple additional configuration.

        self.displayResolutionMode = 2
        self.setScreenRes(self.displayResolutionMode)

        self.bg_color = (230, 230, 230)
        self.bg_image = image.load("Assets/images/background.bmp")
        self.bg_rect = self.bg_image.get_rect()

        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_image = image.load("Assets/images/laser.bmp")
        #self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        self.blast_image = image.load("Assets/images/laser_blast.bmp")
        self.blast_rect = self.blast_image.get_rect()

    def setScreenRes(self, dRM, shipOBJ=None, w=64, h=64):
        if(dRM == 0):
            self.screen_width = w
            self.screen_height = h
        elif(dRM == 1):
            self.screen_width = 1200
            self.screen_height = 800
        elif(dRM == 2):
            self.screen_width = 600
            self.screen_height = 400
        elif(dRM == 3):
            self.screen_width = 3840
            self.screen_height = 2160

        if(shipOBJ != None):
            shipOBJ.screenResCalc(shipOBJ, True)