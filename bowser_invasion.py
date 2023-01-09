import pygame
from pygame.sprite import Group
from luigi import Luigi

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ok_button import OkButton
from mario import Mario
import game_functions as gf

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Mario Kart Bowser Invasion")
    
    # Make the start button.
    play_button = OkButton(ai_settings, screen, "Play")
    
    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    
    # Set the background color.
    bg_color = (230, 230, 230)

    
    # Make mario, luigi, a group of green_shells, red_shells, and a group of enemies.
    mario = Mario(ai_settings, screen)
    luigi = Luigi(ai_settings, screen)
    green_shells = Group()
    red_shells = Group()
    aliens = Group()
    
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, mario, aliens)

    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, mario, luigi, aliens, green_shells, red_shells)
        
        if stats.game_active:
            mario.update()
            luigi.update()
            gf.update_green_shells(ai_settings, screen, stats, sb, luigi, aliens, green_shells)
            gf.update_red_shells(ai_settings, screen, stats, sb, mario, aliens, red_shells)
            gf.update_aliens(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells)
        
        gf.update_screen(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells, play_button)

run_game()