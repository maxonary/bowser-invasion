import pygame
from pygame.sprite import Sprite

class Luigi(Sprite):

    def __init__(self, ai_settings, screen):
        """Initialize Luigi, and set his starting position."""
        super(Luigi, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the luigi image, and get its rect.
        self.image = pygame.image.load('images/luigi.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.image = pygame.transform.scale(self.image, (70, 70))

        # Start each new luigi at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # Store a decimal value for the luigi's center.
        self.center = float(self.rect.centerx)
        
        # Movement flags.
        self.moving_right = False
        self.moving_left = False
        self.rotation_angle = 0
        
    def center_luigi(self):
        """Center Luigi on the screen."""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """Update Luigis position, based on movement flags."""
        # Update Luigis center value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.luigi_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.luigi_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the Luigi at his current location."""
        self.screen.blit(self.image, self.rect)