import pygame
pygame.init()

class Level:
    def __init__(self,level):
        self.background = ["assets_game_PT/Background_1-fotor2.png",
                           "assets_game_PT/Background_space.png"]

        self.image = pygame.image.load(self.background[level-1]).convert_alpha()



        if level == 1:
            self.pos_y = 520
            self.gravity = 10
            self.blue_wall = pygame.image.load("assets_game_PT/blue_wall.png").convert()
            self.blue_wall = pygame.transform.scale(self.blue_wall, (10, 100))
        elif level == 2:
            self.pos_y = 590
            self.gravity = 3
