# Controls the settings for the game

class Settings:
    # A class to store all settings for Alien Invasion

    def __init__(self):
        # Initialize the game's static settings
        # Screen Settings
        self.screen_width  = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60,60)
        self.bullets_allowed = 15

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # Initialize setting that change throughout the game
        self.ship_speed = 3.5
        self.bullet_speed = 7.0
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1


