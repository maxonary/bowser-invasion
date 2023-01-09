import pygame
from pygame.sprite import Sprite

# This class creates the red shell which tracks down enemies
class RedShell(Sprite):
    """A class to manage red_shells fired from the luigi."""

    def __init__(self, ai_settings, screen, luigi):
        """Create a red_shell object, at the luigi's current position."""
        super(RedShell, self).__init__()
        self.screen = screen

        # Load the red_shell image, and get its rect.
        self.image = pygame.image.load('images/red_shell.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Create the red_shell at (0, 0), then set correct position.
        self.rect.centerx = luigi.rect.centerx
        self.rect.top = luigi.rect.top
        
        #Store the red_shell's position as a decimal value.
        self.y = float(self.rect.y)

        # self.color = ai_settings.red_shell_color
        self.speed_factor = ai_settings.red_shell_speed_factor

    def update(self):
        """Move the red_shell up the screen."""
        # Update the decimal position of the red_shell.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_red_shell(self):
        """Draw the red_shell to the screen."""
        self.screen.blit(self.image, self.rect)