import pygame
from pygame import image
from pygame.sprite import Sprite
import random

class Bowser(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """Initialize the bowsers, and set their starting position."""
        super(Bowser, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load bowsers images, and set their rect attribute.
        bowser_select = "bowsers/bowser" + str(random.randint(0, 20)) + ".png"
        self.image = pygame.image.load(bowser_select)
        # rescale image
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()

        # Start each new boser image near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store bowsers's exact position.
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """Return True if bowser is at the edge of the screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """Move bowser right or left."""
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x