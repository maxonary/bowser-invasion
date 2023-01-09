import pygame
from pygame.sprite import Sprite

class Mario(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize mario and luigi and set their starting position."""
        super(Mario, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the mario image, and get its rect.
        self.image = pygame.image.load('images/mario.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.image = pygame.transform.scale(self.image, (70, 70))

        # Start each new mario at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the mario's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_right = False
        self.moving_left = False
        self.rotation_angle = 0
        
    def center_mario(self):
        """Center the mario on the screen."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Update the mario's position, based on movement flags."""
        # Update the mario's center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.mario_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.mario_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the mario at its current location."""
        self.screen.blit(self.image, self.rect)