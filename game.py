import pygame
from player import Player

class Game:
    def __init__(self,level):
        super().__init__()
        self.all_players = pygame.sprite.Group()
        self.player =[Player(self,level,20,level.pos_y,1),Player(self,level,1200,level.pos_y,-1)]

        for player in self.player:
            self.all_players.add(player)

        self.current_player = 0 #Represent the index of the player currently playing

    def switch_turn(self):
        self.current_player = 1 - self.current_player

    def check_collision(self,sprite,group):
       return pygame.sprite.spritecollide(sprite,group,False)