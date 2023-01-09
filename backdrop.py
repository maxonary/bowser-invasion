# This class houses the animated Background Wallpaper for the game
import pygame
import time
class Backdrop():

    def __init__(self, screen):
        """Initialize backdrop attributes."""
        self.screen = screen
        self.png_count = 0
        self.backdrop_str = ""
        self.backdrop_list = []
        # Load the background images, and append them to a list.
        for self.png_count in range(11):
            self.backdrop_str = "backdrops/rainbow_road" + str(self.png_count) + ".png"
            self.backdrop_list.append(pygame.image.load(self.backdrop_str))
            self.png_count += 1


    def draw_backdrop(self):
        # iteate thorugh the backdrop images
        if self.png_count < 110:
            backdrop_image = self.backdrop_list[self.png_count // 10]
            self.png_count += 1
        elif self.png_count == 110:
            self.png_count = 0
            backdrop_image = self.backdrop_list[self.png_count]
        return backdrop_image