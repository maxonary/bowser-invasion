import pygame
from pygame.sprite import Sprite
import math

class GreenShell(Sprite):
    """A class to manage green_shells fired from the mario."""

    def __init__(self, ai_settings, screen, luigi):
        """Create a green_shell object, at marios and luigis current positions."""
        super(GreenShell, self).__init__()
        self.screen = screen

        # Load the green_shell image, and get its rect.
        self.image = pygame.image.load('images/green_shell.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Create the green_shell at (0, 0), then set correct position.
        self.rect.centerx = luigi.rect.centerx
        self.rect.top = luigi.rect.top

        # Store the green_shell's position as a decimal value.
        self.y = float(self.rect.y)

        # self.color = ai_settings.green_shell_color
        self.speed_factor = ai_settings.green_shell_speed_factor

    def update(self):
        """Move the green_shell up the screen."""
        # Update the decimal position of the green_shell.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_green_shell(self):
        """Draw the green_shell to the screen."""
        self.screen.blit(self.image, self.rect)