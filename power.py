import pygame
import random
import time
import math


class Power(pygame.sprite.Sprite):
    def __init__(self, game, x, y, power_type):
        super().__init__()
        self.game = game
        self.power_type = power_type


        self.power_types = {
            1: {"name": "damage", "image": "assets_game_PT/powers_images/Attack_boost.png"},
            2: {"name": "heal", "image": "assets_game_PT/powers_images/green_cross.png"},
            4: {"name": "explosion", "image": "assets_game_PT/powers_images/area_damage.png"},
            3: {"name": "size", "image": "assets_game_PT/powers_images/green_cross.png"}
        }


        self.image = pygame.image.load(self.power_types[power_type]["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Temps d'apparition du pouvoir (10 secondes par défaut)
        self.spawn_time = time.time()
        self.duration = 10  # Durée pendant laquelle le pouvoir est visible en secondes

        # Animation du pouvoir
        self.animation_angle = 0
        self.float_offset = 0
        self.original_y = y

    def update(self):
        # Animation de flottement et rotation pour rendre le pouvoir plus visible
        self.animation_angle += 2
        if self.animation_angle >= 360:
            self.animation_angle = 0

        # Effet de flottement vertical
        self.float_offset = math.sin(time.time() * 2) * 5
        self.rect.y = self.original_y + self.float_offset

        # Rotation de l'image
        original_center = self.rect.center
        new_image = pygame.transform.rotate(self.image, self.animation_angle)
        self.rect = new_image.get_rect(center=original_center)

        # Vérifier si le pouvoir a expiré
        if time.time() - self.spawn_time > self.duration:
            self.kill()

    def apply_power(self, player):
        # Appliquer l'effet du pouvoir au joueur qui le collecte
        power_name = self.power_types[self.power_type]["name"]
        """
        # Effet son de collecte du pouvoir
        power_sound = pygame.mixer.Sound("assets_game_PT/sound/power_pickup.mp3")
        power_sound.play()
        """

        # Appliquer l'effet selon le type de pouvoir
        if power_name == "damage":
            # Augmente les dégâts pendant 3 tours
            player.attack = player.attack * 2
            player.power_effects.append({"type": "damage", "duration": 3})

        elif power_name == "heal":
            # Restaure 50% de la vie
            heal_amount = player.max_health * 0.5
            player.health = min(player.max_health, player.health + heal_amount)

        elif power_name == "explosion":
            # Active le mode explosion pour le prochain tir
            player.explosion_mode = True


        elif power_name == "size":
            # Augmente la taille du boulet pour le prochain tir
            player.projectile_size = 2  # Facteur multiplicateur de taille
            player.power_effects.append({"type": "size", "duration": 2})

        self.kill()  # Le pouvoir disparaît après utilisation


class PowerManager:
    def __init__(self, game):
        self.game = game
        self.all_powers = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 15  # Intervalle de spawn en secondes
        self.last_spawn_time = time.time()

    def update(self):
        current_time = time.time()

        # Mettre à jour tous les pouvoirs existants
        for power in self.all_powers:
            power.update()

        # Vérifier les collisions avec les projectiles du joueurs
        for player in self.game.all_players:
            for projectile in player.all_projectile:
                for power in pygame.sprite.spritecollide(projectile, self.all_powers, False):
                    power.apply_power(player)

        # Vérifier si c'est le moment de faire apparaître un nouveau pouvoir
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_power()
            self.last_spawn_time = current_time

    def spawn_power(self):
        # Définir une zone de spawn aléatoire (éviter les bords et les joueurs)
        min_x = self.game.screen.get_width() * 0.2
        max_x = self.game.screen.get_width() * 0.8
        min_y = self.game.screen.get_height() * 0.2
        max_y = self.game.screen.get_height() * 0.7

        x = random.randint(int(min_x), int(max_x))
        y = random.randint(int(min_y), int(max_y))

        # Choisir un type de pouvoir aléatoire
        power_type = random.randint(1, 4)

        # Créer le pouvoir et l'ajouter au groupe
        power = Power(self.game, x, y, power_type)
        self.all_powers.add(power)

    def draw(self, screen):
        self.all_powers.draw(screen)