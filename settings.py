import pygame

from backdrop import Backdrop

class Settings():
    """A class to store all settings for Goomba Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Backdrop settings.
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (150, 230, 230)

        # Load backdrop image
        self.backdrop = Backdrop('screen')

        
        # Mario health.
        self.health_limit = 2
            
        # GreenShell shooting settings.
        self.green_shells_allowed = 3
        
        # RedShell shooting settings.
        self.red_shells_allowed = 3

        # Enemy settings.
        self.fleet_drop_speed = 11
            
        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        # How quickly the alien point values increase.
        self.score_scale = 1.5
    
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.mario_speed_factor = 1.5
        self.luigi_speed_factor = 1.5
        self.green_shell_speed_factor = 3
        self.red_shell_speed_factor = 4
        self.alien_speed_factor = 1
        
        # Scoring.
        self.alien_points = 50
    
        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1
        
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.mario_speed_factor *= self.speedup_scale
        self.luigi_speed_factor *= self.speedup_scale
        self.green_shell_speed_factor *= self.speedup_scale
        self.red_shell_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)