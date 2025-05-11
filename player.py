import pygame
import time
import math
from boulet_canon import Projectile

pygame.init()
pygame.font.init()
font = pygame.font.Font(None,36)

class Player(pygame.sprite.Sprite):
    def __init__(self,game,level,x,y,direction = 1,):
        super().__init__()
        self.direction = direction
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
        self.power_effects = []
        self.explosion_mode = False
        self.alive = True
        self.projectile_size = 1

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

    def update_power_effects(self):
        # Si le joueur a tiré, réduire la durée des effets de pouvoir
        effects_to_remove = []
        for effect in self.power_effects:
            effect["duration"] -= 1
            if effect["duration"] <= 0:
                effects_to_remove.append(effect)
                # Réinitialiser les effets quand ils expirent
                if effect["type"] == "damage":
                    self.attack = 20  # Valeur de base
                elif effect["type"] == "size":
                    self.projectile_size = 1

        # Supprimer les effets expirés
        for effect in effects_to_remove:
            self.power_effects.remove(effect)


    def damage(self, amount):
        if self.health > amount:
            self.health -= amount
        else:
            self.alive = False
            self.game.end_game()


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
        projectile = Projectile(self,self.level,self.game)
        self.all_projectile.add(projectile)
        self.reinitialize_canon()
        self.update_power_effects()
        if self.projectile_size > 1:
            projectile.image = pygame.transform.scale(projectile.image,
                                                      (int(20 * self.projectile_size),
                                                       int(20 * self.projectile_size)))
            projectile.rect = projectile.image.get_rect(center=projectile.rect.center)

            # Activer le mode explosion si nécessaire
        if self.explosion_mode:
            projectile.explosive = True
            self.explosion_mode = False  # Désactiver après utilisation

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


    def draw_trajectory(self, surface):

        points = []
        velocity = self.power
        angle_rad = math.radians(self.angle)


        # Position de départ du projectile
        start_x = self.rect.centerx
        start_y = self.rect.centery
        vx = velocity * math.cos(angle_rad) * self.direction
        vy = -velocity * math.sin(angle_rad)
        if self.level.lv_number == 1:
            gravity = 0.25
        if self.level.lv_number == 2:
            gravity = 0.25
        if self.level.lv_number == 3:
            gravity = 0.25

        for t in range(1, 10):
            dx = vx * t
            dy = vy * t  + 0.5 * gravity * t** 2
            point = (int(start_x + dx), int(start_y + dy))


            if point[1] > self.game.screen.get_height() or point[0] < 0 or point[0] > self.game.screen.get_width():
                break
            points.append(point)

        for point in points:
            pygame.draw.circle(surface, (255, 255, 0), point, 3)






