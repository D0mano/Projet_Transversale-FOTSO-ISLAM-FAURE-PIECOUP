
import pygame
import time

from game import Game
from level import Level
pygame.init()

run = True

ecran = pygame.display.set_mode((800,600),pygame.RESIZABLE)
level = Level(1)
pygame.display.set_caption("CanonMaster")


game = Game(level)

while run: # Main loop for the game

    ecran.blit(level.image,(0,0))

    ecran.blit(game.player[0].pied_canon, (game.player[0].rect_pied.x,game.player[0].rect_pied.y))
    ecran.blit(game.player[1].pied_canon, (game.player[1].rect_pied.x,game.player[1].rect_pied.y))
    ecran.blit(game.player[0].canon, game.player[0].rect.topleft)
    ecran.blit(game.player[1].canon, game.player[1].rect.topleft)

    ecran.blit(game.player[game.current_player].show_info()[0],(game.player[game.current_player].rect.x + game.player[game.current_player].direction*50,650))
    ecran.blit(game.player[game.current_player].show_info()[1],(game.player[game.current_player].rect.x + game.player[game.current_player].direction*50,600))

    for players in game.player:
        for projectile in players.all_projectile:
            projectile.move()

    for players in game.player:
        players.all_projectile.draw(ecran)
        players.update_health_bar(ecran)



    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                run = False

            elif event.key == pygame.K_SPACE:
                game.player[game.current_player].fire()
                game.switch_turn()


            elif event.key == pygame.K_RIGHT:
                game.player[game.current_player].power_up()

            elif event.key == pygame.K_LEFT:
                game.player[game.current_player].power_down()

            elif event.key == pygame.K_UP:
                game.player[game.current_player].aim_up()

            elif event.key == pygame.K_DOWN:
                game.player[game.current_player].aim_down()

    time.sleep(game.player[game.current_player].power * 0.001)


pygame.quit()

