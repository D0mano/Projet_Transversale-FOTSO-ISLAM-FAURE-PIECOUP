import pygame
import math
from anim_powers import Explosion
pygame.init()

class Projectile(pygame.sprite.Sprite):
    def __init__(self, player,level,game):
        super().__init__()
        self.visible = True
        self.level = level
        self.game = game
        self.images = ["assets_game_PT/canon/boulet_de_canon-removebg-preview.png","assets_game_PT/canon/boulet_canon_space.png","assets_game_PT/canon/boulet_de_canon-removebg-preview.png"]
        self.user = player
        self.image = pygame.image.load(self.images[self.level.lv_number-1])
        self.image = pygame.transform.scale(self.image,(20 * self.user.projectile_size,20 * self.user.projectile_size))
        self.rect = self.image.get_rect()
        self.death_rect = None
        self.canon_sound = pygame.mixer.Sound("assets_game_PT/sound/sf_canon_01.mp3")
        self.explosion_sound = pygame.mixer.Sound("assets_game_PT/sound/medium-explosion-40472.mp3")
        self.explosive = False
        self.explosion_radius = 200
        self.explosion_damage = 30

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


    def create_explosion(self):
        # Effet visuel de l'explosion
        explosion = Explosion(self.rect.centerx,self.rect.centery,4)
        self.game.all_explosion.add(explosion)

        # Vérifier les joueurs dans la zone d'explosion
        for player in self.game.all_players:
            # Calculer la distance entre le centre de l'explosion et le joueur
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)

            # Si le joueur est dans le rayon d'explosion
            if distance <= self.explosion_radius:
                # Les dégâts diminuent avec la distance
                damage_factor = 1 - (distance / self.explosion_radius)
                damage = int(self.explosion_damage * damage_factor)
                if player != self.user:  # Ne pas endommager le joueur qui tire
                    player.damage(damage)


    def move(self,dt):
        if self.time == 0:
            self.canon_sound.play()
        
        self.time += dt
        self.rect.x += int(self.vel_x) * self.user.direction
        self.rect.y += int(0.5 * self.gravity* self.time**2 +self.vel_y)

        if self.rect.y > self.level.pos_y + 30 :
            if self.explosive:
                self.create_explosion()
            self.explosion_sound.play()
            self.kill()

        for player in self.game.check_collision(self,self.game.all_players):
            if player != self.user:
                if self.explosive:
                    self.create_explosion()
                self.explosion_sound.play()
                self.kill()
                player.damage(self.user.attack)

        for obstacle in self.game.check_collision(self,self.level.all_obstacle):
            self.explosion_sound.play()
            if self.explosive:
                self.create_explosion()
            self.explosion_sound.play()
            self.kill()


