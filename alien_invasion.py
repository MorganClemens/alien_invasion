# Import Dependencies
import sys
import pygame
# Import Classes
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    #Overall class to manage game asets and behavior

    def __init__(self):
        # Initialize the game, and create game resources 
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # Set the screen dimensions
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Create an instance of the ship
        self.ship = Ship(self)
        # Create group that holds bullets
        self.bullets = pygame.sprite.Group()
        # Create group that holds alien ships
        self.aliens = pygame.sprite.Group()
        # Invoke create fleet helper method
        self._create_fleet()


    def run_game(self):
        # Initialize main game loop

        while True:
            self._check_events()
            # Update ship position
            self.ship.update()
            self._update_bullets()
            # Re-draw the screen with preceeding updates
            self._update_screen()
            # Set the target framerate to 144 fps
            self.clock.tick(144)


    def _check_events(self):
        # Respond to keypresses and mouse events

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Respond to key presses

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self, event):
        # Respond to key releases

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        # Create a new bullet and add it to the bullets group

        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # Updates the positon of bullets and deletes old bullets
        
        self.bullets.update()
        # Delete of bullets that have travelled off-screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        print(len(self.bullets))
    
    def _create_fleet(self):
        # Create the fleet of aliens

        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width.
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * (alien_width)


    def _update_screen(self):
        # Update images on screen, and flip to new screen

        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        # Draws bullets in bullet group
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Draws ship
        self.ship.blitme()
        # Draws alien(s)
        self.aliens.draw(self.screen)
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    # Make game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()