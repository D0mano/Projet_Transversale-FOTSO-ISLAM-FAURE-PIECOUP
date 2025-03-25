import pygame
import math


pygame.init()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player,level,game):
        super().__init__()
        self.level = level
        self.game = game
        self.user = player
        self.image = pygame.image.load("assets_game_PT/canon/boulet_de_canon-removebg-preview.png")
        self.image = pygame.transform.scale(self.image,(20,20))
        self.rect = self.image.get_rect()

        if player.direction == 1:
            canon_length = 13
        else:
            canon_length = 5

        angle_rad = math.radians(player.angle)
        offset_x = canon_length * math.cos(angle_rad)
        offset_y = canon_length * math.sin(angle_rad)

        if player.direction == 1:
            self.rect.x = player.rect.centerx - offset_x
        else:
            self.rect.x = player.rect.centerx + offset_x

        self.rect.y = player.rect.centery - offset_y

        self.gravity = self.level.gravity
        self.power = player.power
        self.vel_x = self.power * math.cos(angle_rad)
        self.vel_y = -self.power * math.sin(angle_rad)
        self.time = 0

    def move(self,dt):
        self.time += dt
        self.rect.x += int(self.vel_x) * self.user.direction
        self.rect.y += int(0.5 * self.gravity* self.time**2 +self.vel_y)

        if self.rect.y >self.level.pos_y + 30 :
            self.kill()

        for player in self.game.check_collision(self,self.game.all_players):
            if player != self.user:
                self.kill()
                player.damage(self.user.attack)
        for obstacle in self.game.check_collision(self,self.level.all_obstacle):
            self.kill()