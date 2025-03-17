
import pygame
import time
from game import Game
from level import Level

pygame.init()
clock = pygame.time.Clock()

run = True

ecran = pygame.display.set_mode((0,0),pygame.RESIZABLE)
level = Level(1,ecran)
pygame.display.set_caption("CanonMaster")


game = Game(level,ecran)

while run: # Main loop for the game
    dt = clock.tick(60)/1000.0

    # We verify if the game is playing
    if game.is_playing:
        game.start(dt)
    else:
        game.menu()
        run = game.running


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()

