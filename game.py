import pygame
from player import Player

class Game:
    def __init__(self):
        self.all_players = pygame.sprite.Group
        self.player =[Player(20,520,1),Player(1200,520,-1)]

        for player in self.player:
            self.all_players.add(player)

        self.current_player = 0 #Represent the index of the player currently playing

    def switch_turn(self):
        self.current_player = 1 - self.current_player



