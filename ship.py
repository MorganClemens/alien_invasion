import pygame

class Ship:
    #Class to manage the ship

    def __init__(self):
        #Initialize the ship and set starting position
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get.rect()

        #Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Start each new ship at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        #Draw the ship at current location
        self.screen.blit(self.image, self.rect)
        
