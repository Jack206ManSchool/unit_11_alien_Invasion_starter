class Settings: 
    """ A class to store all settings for Alien Invasion. """

    def __init__(self):
        """ Initialize the game's settings. """
        # Screen settings
        
        # Edited from this because it wasn't fitting on the screen
        # self.screen_width = 1200
        # self.screen_height = 800
        self.screen_width = 600
        self.screen_height = 400

        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 1.5