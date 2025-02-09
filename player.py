import pygame
from Boulet_Canon import Projectile

pygame.init()
pygame.font.init()
font = pygame.font.Font(None,36)

class Player(pygame.sprite.Sprite):
    def __init__(self,level,x,y,direction = 1,):
        super().__init__()
        self.level = level
        self.health = 100
        self.max_health = 100
        self.angle = 0
        self.power = 20
        self.all_projectile = pygame.sprite.Group()
        self.original_canon = pygame.image.load("assets_game_PT/Canon_1-removebg-preview.png").convert_alpha()
        self.original_canon = pygame.transform.scale(self.original_canon,(60,60))
        if direction == -1:
            self.original_canon = pygame.transform.flip(self.original_canon,True,False)
        self.canon = self.original_canon
        self.rect = self.canon.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

    def update_health_bar(self,surface):
        # We define a color for the health bar
        bar_color = (255,0,0)
        # We define a color for the background of the health bar
        bar_back_color = (116,115,116)

        # we define the position and dimension of the health bar
        if self.direction == 1:
            bar_pos = [30,50,self.health*4,20]
            bar_back_pos = [30,50,self.max_health*4,20]
        else:
            bar_pos = [850,50,self.health*4,20]
            bar_back_pos = [850,50,self.max_health*4,20]
        # We define the position of the back health bar

        # we draw the health bar
        pygame.draw.rect(surface,bar_back_color,bar_back_pos)
        pygame.draw.rect(surface,bar_color,bar_pos)



    def damage(self, amount):
        self.health -= amount


    def fire(self):
        self.all_projectile.add(Projectile(self,self.level))

    def aim_up(self):
        if self.angle < 90:
            self.angle += 5
            self.canon = pygame.transform.rotate(self.original_canon, self.angle * self.direction)
            self.rect = self.canon.get_rect(center=self.rect.center)

    def aim_down(self):
        if self.angle > 0:
            self.angle -= 5
            self.canon = pygame.transform.rotate(self.original_canon, self.angle * self.direction)
            self.rect = self.canon.get_rect(center=self.rect.center)

    def power_up(self):
        if self.power < 100:
            self.power += 5

    def power_down(self):
        if self.power > 0:
            self.power -= 5


    def show_info(self):
        angle_text = font.render(f"Angle: {self.angle}°",True,(255,255,255))
        power_text = font.render(f"Power: {self.power}",True,(255,255,255))
        return angle_text,power_text






