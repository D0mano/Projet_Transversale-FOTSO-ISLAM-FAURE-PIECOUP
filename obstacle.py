import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,level,x,y):
        super().__init__()
        self.level = level
        self.type_obstacle = ["assets_game_PT/blue_wall.png"]
        self.image = pygame.image.load(self.type_obstacle[self.level.lv_number-1]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (10, 100))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.velocity = 5
        self.direction = 1

    def move_obstacle(self):
        self.rect.y += self.velocity * self.direction

        if self.rect.y < 10 or self.rect.y >= self.level.pos_y - 60:
            self.direction *= -1





