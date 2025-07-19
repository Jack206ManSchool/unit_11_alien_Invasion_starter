class Settings: 
    """ A class to store all settings for Alien Invasion. """

    def __init__(self):
        """ Initialize the game's settings. """
        # Screen settings
        
        # The resolution was glitching out a bit because of my choice of display.
        # Because of this, I added a simple additional configuration.
        
        self.displayResolutionMode = 2
        
        if(self.displayResolutionMode == 0):
            self.screen_width = 1200
            self.screen_height = 800
        elif(self.displayResolutionMode == 1):
            self.screen_width = 600
            self.screen_height = 400
        elif(self.displayResolutionMode == 2):
            self.screen_width = 3840
            self.screen_height = 2160

        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5