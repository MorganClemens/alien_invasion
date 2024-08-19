import pygame

class Ship:
    # Class to manage the ship

    def __init__(self, ai_game):
        # Initialize the ship and set starting position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for ship x position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flag; start with ship that is not moving
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        # Update ship position based on movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Update rect object from self.x and self.y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        # Draw the ship at current location
        self.screen.blit(self.image, self.rect)


