# Import Dependencies
import sys
from time import sleep
import pygame
# Import Classes
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    '''Overall class to manage game asets and behavior'''

    def __init__(self):
        '''Initialize the game, and create game resources''' 
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # Set the screen dimensions
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store the game statistics and create scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Create an instance of the ship
        self.ship = Ship(self)
        # Create group that holds bullets
        self.bullets = pygame.sprite.Group()
        # Create group that holds alien ships
        self.aliens = pygame.sprite.Group()
        # Invoke create fleet helper method
        self._create_fleet()
        # Start Alien Invasion in an inactive state
        self.game_active = False
        # Make the Play button
        self.play_button = Button(self, "Play Game")

    def run_game(self):
        '''Initialize main game loop'''
        while True:
            self._check_events()

            if self.game_active:
                # Run these parts of the game when the game is active
                # Update ship position
                self.ship.update()
                # Update bullet position
                self._update_bullets()
                # Update alien fleet position
                self._update_aliens()

            # Re-draw the screen with preceeding updates
            self._update_screen()
            # Set the target framerate to 60 fps
            self.clock.tick(60)

    def _check_events(self):
        '''Respond to keypresses and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            # Reset game statistics and start the game
            self.stats.reset_stats()
            self.sb.prep_score()
            self.game_active = True
            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            # Hide mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        '''Respond to key presses'''
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
        '''Respond to key releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Updates the positon of bullets and deletes old bullets'''
        self.bullets.update()
        # Delete of bullets that have travelled off-screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''Respond to bullet-alien collisions'''
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

        if not self.aliens:
            # destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _update_aliens(self):
        '''Updates the position of all aliens in the fleet'''
        self._check_fleet_edges() # lack of check fleet edges in _update_aliens caused a bug where fleet wouldn't check edges
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
        
    def _create_fleet(self):
        '''Create the fleet of aliens'''
        # Create an alien and keep adding aliens until there's no room left
        # Spacing between aliens is one alien width and one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * (alien_width)

            # Finished a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        '''Create an alien and place it in the fleet'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        '''Responds when aliens have reached the edge of the screen'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Drop entire fleet and change the fleet direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1     
    
    def _check_aliens_bottom(self):
        '''Check if any aliens have reached the bottom of the screen'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break
    
    def _ship_hit(self):
        '''Respond to the ship being hit by an alien'''
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        '''Update images on screen, and flip to new screen'''
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        # Draws bullets in bullet group
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Draws ship
        self.ship.blitme()
        # Draws alien(s)
        self.aliens.draw(self.screen)
        # Draw the score information
        self.sb.show_score()
        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        # Make the most recently drawn screen visible
        pygame.display.flip()


if __name__ == '__main__':
    '''Make game instance, and run the game'''
    ai = AlienInvasion()
    ai.run_game()