import pygame
from obstacle import Obstacle
pygame.init()

class Level:
    def __init__(self,level):
        self.background = ["assets_game_PT/Background_1-fotor2.png",
                           "assets_game_PT/Background_space.png"]

        self.image = pygame.image.load(self.background[level-1]).convert_alpha()
        self.lv_number =  level


        if level == 1:
            self.pos_y = 520
            self.gravity = 10
            self.obstacle = Obstacle(self,640,360)

        elif level == 2:
            self.pos_y = 590
            self.gravity = 3
