import pygame
from obstacle import Obstacle
pygame.init()

class Level:
    def __init__(self,level,screen):
        self.background = ["assets_game_PT/Background_1-fotor2.png",
                           "assets_game_PT/Background_space.png"]

        self.image = pygame.image.load(self.background[level-1]).convert_alpha()
        self.screen = screen
        self.image = pygame.transform.scale(self.image, (self.screen.get_width(), self.screen.get_height()))
        self.lv_number =  level

        if level == 1:
            self.pos_y = screen.get_height()/1.38
            self.gravity = 50
            self.obstacle = Obstacle(self,screen.get_width()/2-20,360)

        elif level == 2:
            self.pos_y = screen.get_height()/1.22
            self.gravity = 20
            self.obstacle = Obstacle(self,screen.get_width()/2-40,360)
        self.all_obstacle = pygame.sprite.Group()
        self.all_obstacle.add(self.obstacle)
