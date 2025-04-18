import pygame
import time
from Boulet_Canon import Projectile

pygame.init()
pygame.font.init()
font = pygame.font.Font(None,36)

class Player(pygame.sprite.Sprite):
    def __init__(self,game,level,x,y,direction = 1,):
        super().__init__()
        self.game = game
        self.level = level
        self.attack = 20
        self.health = 100
        self.max_health = 100
        self.angle = 0
        self.power = 20
        self.all_projectile = pygame.sprite.Group()
        self.pied_canon = pygame.image.load("assets_game_PT/canon/_pied_Canon_1-removebg-preview.png").convert_alpha()
        self.pied_canon = pygame.transform.scale(self.pied_canon,(60,60))
        self.original_canon = pygame.image.load("assets_game_PT/canon/_Canon_2-removebg-preview.png").convert_alpha()
        self.original_canon = pygame.transform.scale(self.original_canon, (60, 60))
        if direction == -1:
            self.original_canon = pygame.transform.flip(self.original_canon,True,False)
            self.pied_canon = pygame.transform.flip(self.pied_canon,True,False)
        self.canon = self.original_canon
        self.rect = self.canon.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_pied = self.pied_canon.get_rect()
        self.rect_pied.x = x
        self.rect_pied.y = y
        self.direction = direction
        self.alive = True

    def update_health_bar(self,surface):
        # We define a color for the health bar
        bar_color = (255,0,0)
        # We define a color for the background of the health bar
        bar_back_color = (116,115,116)

        # we define the position and dimension of the health bar
        if self.direction == 1:
            bar_pos = [self.game.screen.get_width()/20,50,self.health*4,20]
            bar_back_pos = [self.game.screen.get_width()/20,50,self.max_health*4,20]
        else:
            bar_pos = [self.game.screen.get_width()/1.51,50,self.health*4,20]
            bar_back_pos = [self.game.screen.get_width()/1.51,50,self.max_health*4,20]
        # We define the position of the back health bar

        # we draw the health bar
        pygame.draw.rect(surface,bar_back_color,bar_back_pos)
        pygame.draw.rect(surface,bar_color,bar_pos)



    def damage(self, amount):
        if self.health > amount:
            self.health -= amount
        else:
            self.alive = False
            self.game.game_over()
    def cal_pos(self):
        if self.direction == 1:
            self.rect.x = self.game.screen.get_width() / 64
            self.rect_pied.x = self.rect.x
        else:
            self.rect.x = self.game.screen.get_width() / 1.067
            self.rect_pied.x = self.rect.x
        self.rect.y = self.game.screen.get_height()/1.38
        self.rect_pied.y = self.rect.y

    def reinitialize_canon(self):
        self.angle = 0
        self.power = 20
        self.canon = pygame.transform.rotate(self.original_canon, self.angle * self.direction)
        self.rect = self.canon.get_rect(center=self.rect.center)

    def fire(self):
        self.all_projectile.add(Projectile(self,self.level,self.game))
        self.reinitialize_canon()

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
        if self.power < 30:
            self.power += 2

    def power_down(self):
        if self.power > 0:
            self.power -= 2


    def show_info(self):
        angle_text = font.render(f"Angle: {self.angle}°",True,(255,255,255))
        power_text = font.render(f"Power: {self.power}",True,(255,255,255))
        return angle_text,power_text






