
import pygame
import time
from game import Game
from level import Level

pygame.init()
clock = pygame.time.Clock()

run = True

ecran = pygame.display.set_mode((0,0),pygame.RESIZABLE)
level = Level(2)
pygame.display.set_caption("CanonMaster")

# We load the different asset for the menu
background = pygame.image.load("assets_game_PT/Background_menu.png").convert_alpha()

banner = pygame.image.load("assets_game_PT/CANON_MASTER_Logo-removebg-preview.png").convert_alpha()

banner_rect = banner.get_rect()
banner_rect.x = (ecran.get_width()/2)-250
banner_rect.y = ecran.get_height()-800

play_button_white = pygame.image.load("assets_game_PT/play_button_white.png").convert_alpha()
play_button_green= pygame.image.load("assets_game_PT/play_button_green.png").convert_alpha()
play_button_rect = play_button_green.get_rect()
play_button_rect.x = ecran.get_width()/2-150
play_button_rect.y = ecran.get_height()/3

quit_button_white = pygame.image.load("assets_game_PT/quit_button_white.png").convert_alpha()
quit_button_red = pygame.image.load("assets_game_PT/quit_button_red.png").convert_alpha()
quit_button_rect = quit_button_red.get_rect()
quit_button_rect.x = ecran.get_width()/2 -150
quit_button_rect.y = ecran.get_height()/3+150

game = Game(level)
play_button = play_button_white
quit_button = quit_button_white
while run: # Main loop for the game
    dt = clock.tick(60)/1000.0

    # We verify if the game is playing
    if game.is_playing:
        game.start(ecran,dt)
    else:
        ecran.blit(background, (0, 0))
        ecran.blit(banner,banner_rect)
        ecran.blit(play_button,play_button_rect)
        ecran.blit(quit_button,quit_button_rect)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEMOTION:
            if play_button_rect.collidepoint(event.pos):
                play_button = play_button_green
            else:
                play_button = play_button_white
            if quit_button_rect.collidepoint(event.pos):
                quit_button = quit_button_red
            else:
                quit_button = quit_button_white
        elif event.type == pygame.MOUSEBUTTONUP:
            if play_button_rect.collidepoint(event.pos):
                game.is_playing = True
            elif quit_button_rect.collidepoint(event.pos):
                run = False

    pygame.display.flip()

pygame.quit()

