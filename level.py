import pygame
import sys
from obstacle import Obstacle
pygame.init()

class Level:
    def __init__(self,screen,level=2):
        self.lv_number = level
        self.background = ["assets_game_PT/background/Background_1-fotor2.png",
                           "assets_game_PT/background/Background_space.png",
                           "assets_game_PT/background/Background_under_water.png"]
        self.screen = screen

        self.true_image = pygame.image.load(self.background[self.lv_number-1]).convert_alpha()
        self.image = pygame.transform.scale(self.true_image, (self.screen.get_width(), self.screen.get_height()))


        if self.lv_number == 1:
            self.pos_y = screen.get_height()/1.38
            self.gravity = 50
            self.obstacle = Obstacle(self,screen.get_width()/2-20,self.screen.get_height()/2)

        elif self.lv_number == 2:
            self.pos_y = screen.get_height()/1.22
            self.gravity = 20
            self.obstacle = Obstacle(self,screen.get_width()/2-40,self.screen.get_height()/2)
        elif self.lv_number == 3:
            self.pos_y = screen.get_height()/1.22
            self.gravity = 80
            self.obstacle = Obstacle(self,screen.get_width()/2,self.screen.get_height()/2)
        self.all_obstacle = pygame.sprite.Group()
        self.all_obstacle.add(self.obstacle)

    def load_level(self):
        # Load the background and the obstacle of the Level
        self.screen.blit(self.image, (0, 0))
        self.screen.blit(self.obstacle.image, (self.obstacle.rect.x, self.obstacle.rect.y))
        self.obstacle.move_obstacle()