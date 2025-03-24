import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,level,x,y):
        super().__init__()
        self.level = level
        self.type_obstacle = ["assets_game_PT/muraille.png",
                              "assets_game_PT/meteorite.png"]
        self.image = pygame.image.load(self.type_obstacle[self.level.lv_number-1]).convert_alpha()
        if level.lv_number == 1:
            self.image = pygame.transform.scale(self.image, (40, 120))
        elif level.lv_number == 2:
            self.image = pygame.transform.scale(self.image, (100, 200))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.velocity = 5
        self.direction = 1

    def move_obstacle(self):
        self.rect.y += self.velocity * self.direction

        if self.level.lv_number == 1:
            if self.rect.y < 7 or self.rect.y >= self.level.pos_y - 79:
                self.direction *= -1
        elif self.level.lv_number == 2:
            if self.rect.y < 7 or self.rect.y >= self.level.pos_y - 150:
                self.direction *= -1




