# This class creates the iconic Mario Kart "OK" button
import pygame

class OkButton():

    def __init__(self, ai_settings, screen, msg):
        """Initialize button attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Load the button image, and get its rect.
        self.image = pygame.image.load('images/ok_button.png')
        self.rect = self.image.get_rect()
        
        # Center the button.
        self.rect.center = self.screen_rect.center

    def draw_ok_button(self):
        """Draw the button to the screen."""
        self.screen.blit(self.image, self.rect)