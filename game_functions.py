import sys
from time import sleep

import pygame
from pygame.version import PygameVersion

from green_shell import GreenShell
from bowser import Bowser
from backdrop import Backdrop
from red_shell import RedShell

def check_keydown_events(event, ai_settings, screen, mario, luigi, green_shells, red_shells):
    """Respond to keypresses."""
    # move to the left
    if event.key == pygame.K_LEFT:
        mario.moving_left = True
    elif event.key == pygame.K_a:
        luigi.moving_left = True
    # move to the right
    elif event.key == pygame.K_RIGHT:
        mario.moving_right = True
    elif event.key == pygame.K_d:
        luigi.moving_right = True
    # shoot projectiles
    elif event.key == pygame.K_SPACE:
        fire_green_shell(ai_settings, screen, luigi, green_shells)
    elif event.key == pygame.K_UP:
        fire_red_shell(ai_settings, screen, mario, red_shells)
    # quit the game
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, mario, luigi):
    """Respond to key releases."""
    # key release left
    if event.key == pygame.K_LEFT:
        mario.moving_left = False
    elif event.key == pygame.K_a:
        luigi.moving_left = False
    # key release right
    elif event.key == pygame.K_RIGHT:
        mario.moving_right = False
    elif event.key == pygame.K_d:
        luigi.moving_right = False

def check_events(ai_settings, screen, stats, sb, play_button, mario, luigi,aliens, green_shells, red_shells):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, mario, luigi, green_shells, red_shells)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, mario, luigi)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                mario, luigi, aliens, green_shells, red_shells, mouse_x, mouse_y)
            
def check_play_button(ai_settings, screen, stats, sb, play_button, mario, luigi, aliens, green_shells, red_shells, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()
        
        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)
        
        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True
        
        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_marios()
        
        # Empty the list of aliens and green_shells.
        aliens.empty()
        green_shells.empty()
        red_shells.empty()
        
        # Create a new fleet and center mario and lugi.
        create_fleet(ai_settings, screen, mario, aliens)
        mario.center_mario()
        luigi.center_luigi()

def fire_green_shell(ai_settings, screen, luigi, green_shells):
    """Fire a green_shell, if limit not reached yet."""
    # Create a new green_shell, add to green_shells group.
    if len(green_shells) < ai_settings.green_shells_allowed:
        new_green_shell = GreenShell(ai_settings, screen, luigi)
        green_shells.add(new_green_shell)
        
def fire_red_shell(ai_settings, screen, mario, red_shells):
    """Fire a red_shell, if limit not reached yet."""
    # Create a new red_shell, add to red_shells group.
    if len(red_shells) < ai_settings.red_shells_allowed:
        new_red_shell = RedShell(ai_settings, screen, mario)
        red_shells.add(new_red_shell)

def update_screen(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells ,play_button):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Construct the backdrop image.
    
    new_backround = ai_settings.backdrop.draw_backdrop()
    # Rescale image to screen size.
    new_backround = pygame.transform.scale(new_backround, (ai_settings.screen_width, ai_settings.screen_height))
    screen.blit(new_backround,   [0,0])


    # Redraw all green_shells, behind mario, luigi and the enemies.
    for green_shell in green_shells.sprites():
        # blitme function in green_shell.py
        green_shell.draw_green_shell()
    # Redraw all red_shells, behind mario, luigi and the enemies.
    for red_shell in red_shells.sprites():
        # blitme function in red_shell.py
        red_shell.draw_red_shell()
    mario.blitme()
    luigi.blitme()
    aliens.draw(screen)
    
    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_ok_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()
    
def update_green_shells(ai_settings, screen, stats, sb, luigi, aliens, green_shells):
    """Update position of green_shells, and get rid of old green_shells."""
    # Update green_shell positions.
    green_shells.update()

    # Get rid of green_shells that have disappeared.
    for green_shell in green_shells.copy():
        if green_shell.rect.bottom <= 0:
            green_shells.remove(green_shell)
            
    check_green_shell_alien_collisions(ai_settings, screen, stats, sb, luigi, aliens, green_shells)

def update_red_shells(ai_settings, screen, stats, sb, mario, aliens, red_shells):
    """Update position of red_shells, and get rid of old red_shells."""
    # Update red_shell positions.
    red_shells.update()

    # Get rid of red_shells that have disappeared.
    for red_shell in red_shells.copy():
        if red_shell.rect.bottom <= 0:
            red_shells.remove(red_shell)
            
    check_red_shell_alien_collisions(ai_settings, screen, stats, sb, mario, aliens, red_shells)
        
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
            
def check_green_shell_alien_collisions(ai_settings, screen, stats, sb, luigi, aliens, green_shells):
    """Respond to green_shell-alien collisions."""
    # Remove any green_shells and aliens that have collided.
    collisions = pygame.sprite.groupcollide(green_shells, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        green_shells.empty()
        ai_settings.increase_speed()
        
        # Increase level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, luigi, aliens)

def check_red_shell_alien_collisions(ai_settings, screen, stats, sb, mario, aliens, red_shells):
    """Respond to red_shell-alien collisions."""
    # Remove any red_shells and aliens that have collided.
    collisions = pygame.sprite.groupcollide(red_shells, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        red_shells.empty()
        ai_settings.increase_speed()
        
        # Increase level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, mario, aliens)
    
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def mario_hit(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells):
    """Respond to mario being hit by alien."""
    if stats.marios_left > 0:
        # Decrement marios_left.
        stats.marios_left -= 1
        
        # Update scoreboard.
        sb.prep_marios()
        
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    # Empty the list of aliens and green_shells and red_shells.
    aliens.empty()
    green_shells.empty()
    red_shells.empty()
    
    # Create a new fleet, and center the mario.
    create_fleet(ai_settings, screen, mario, aliens)
    mario.center_mario()
    luigi.center_luigi()
    
    # Pause.
    sleep(0.5)
    
def check_aliens_bottom(ai_settings, screen, stats, sb, mario, luigi, aliens,
        green_shells, red_shells):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the mario got hit.
            mario_hit(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells)
            break
            
def update_aliens(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells):
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-mario collisions.
    if pygame.sprite.spritecollideany(mario, aliens):
        mario_hit(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, mario, luigi, aliens, green_shells, red_shells)
            
def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, mario_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - mario_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Bowser(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, mario, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Bowser(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, mario.rect.height, alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)