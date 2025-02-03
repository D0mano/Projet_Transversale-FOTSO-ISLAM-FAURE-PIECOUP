import pygame
import math


pygame.init()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.user = player
        self.image = pygame.image.load("assets_game_PT/boulet_de_canon-removebg-preview.png")
        self.image = pygame.transform.scale(self.image,(20,20))
        self.rect = self.image.get_rect()
        self.rect.x = self.user.rect.x + (50 * player.direction)
        self.rect.y = self.user.rect.y + 20


        self.gravity = 9.81
        self.angle =player.angle
        self.power = player.power
        self.vel_x = self.power * math.cos(math.radians(self.angle))
        self.vel_y = -self.power * math.sin(math.radians(self.angle))
        self.time = 0
    """
    def check_collision(self,sprite,group):
        return pygame.sprite.spritecollide(sprite,group,False,pygame.sprite.collide_mask())
    """
    def move(self):
        self.time += 0.1
        self.rect.x += int(self.vel_x) * self.user.direction
        self.rect.y += int(0.5 * self.gravity* self.time**2 +self.vel_y)

        if self.rect.y > 550:
            self.kill()
