#Dependencies
import sys
import pygame

from settings import Settings

class AlienInvasion:
    """Overall class to manage game asets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            #Game Loop
            
            #Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    
            #Redraw the screen during each pass through the loop
            self.screen.fill(self.settings.bg_color)

            #Make the most recently drawn screen visible
            pygame.display.flip()

            #Set the target framerate to 60 fps
            self.clock.tick(60)
            

if __name__ == '__main__':
    #Make game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()