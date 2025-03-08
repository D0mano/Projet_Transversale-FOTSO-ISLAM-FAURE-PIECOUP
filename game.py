import pygame
from player import Player

class Game:
    def __init__(self,level):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player =[Player(self,level,20,level.pos_y,1),Player(self,level,1200,level.pos_y,-1)]
        self.level = level
        for player in self.player:
            self.all_players.add(player)

        self.current_player = 0 #Represent the index of the player currently playing

    def start(self,ecran,dt):
        # Load the background and the obstacle of the Level
        ecran.blit(self.level.image, (0, 0))
        ecran.blit(self.level.obstacle.image, (self.level.obstacle.rect.x, self.level.obstacle.rect.y))
        self.level.obstacle.move_obstacle()

        # Load the player model
        ecran.blit(self.player[0].pied_canon, (self.player[0].rect_pied.x, self.player[0].rect_pied.y))
        ecran.blit(self.player[1].pied_canon, (self.player[1].rect_pied.x, self.player[1].rect_pied.y))
        ecran.blit(self.player[0].canon, self.player[0].rect.topleft)
        ecran.blit(self.player[1].canon, self.player[1].rect.topleft)

        # Load the shooting information
        ecran.blit(self.player[self.current_player].show_info()[0],
                   (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50, 650))
        ecran.blit(self.player[self.current_player].show_info()[1],
                   (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50, 600))

        # Load the canon of all the players
        for players in self.player:
            for projectile in players.all_projectile:
                projectile.move(dt)

        # Load the players healths bar
        for players in self.player:
            players.all_projectile.draw(ecran)
            players.update_health_bar(ecran)

        pygame.display.flip()

        # Loop for the keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.is_playing = False

                if event.key == pygame.K_SPACE:
                    self.player[self.current_player].fire()
                    self.switch_turn()


                elif event.key == pygame.K_RIGHT:
                    self.player[self.current_player].power_up()

                elif event.key == pygame.K_LEFT:
                    self.player[self.current_player].power_down()

                elif event.key == pygame.K_UP:
                    self.player[self.current_player].aim_up()

                elif event.key == pygame.K_DOWN:
                    self.player[self.current_player].aim_down()

    def switch_turn(self):
        self.current_player = 1 - self.current_player

    def check_collision(self,sprite,group):
       return pygame.sprite.spritecollide(sprite,group,False)