import pygame
import random
import time
import math


class Power(pygame.sprite.Sprite):
    """
    Represents a power-up item that players can collect to gain temporary advantages.
    Power-ups have different effects based on their type and animate to attract attention.
    """

    def __init__(self, game, x, y, power_type):
        """
        Initialize a power-up.

        Args:
            game: Reference to the main game instance
            x, y: Position coordinates for the power-up
            power_type: Integer ID determining the power-up's effect
        """
        super().__init__()
        self.game = game
        self.power_type = power_type

        # Dictionary defining different power-up types with their names and image paths
        self.power_types = {
            1: {"name": "damage", "image": "assets_game_PT/powers_images/Attack_boost.png"},  # Increase attack damage
            2: {"name": "heal", "image": "assets_game_PT/powers_images/green_cross.png"},  # Restore health
            4: {"name": "explosion", "image": "assets_game_PT/powers_images/area_damage.png"},
            # Enable explosion damage
            3: {"name": "size", "image": "assets_game_PT/powers_images/Image_Taille_Balle.png"}
            # Increase projectile size
        }

        # Load and scale the power-up image
        self.image = pygame.image.load(self.power_types[power_type]["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Power-up lifetime tracking (10 seconds by default)
        self.spawn_time = time.time()
        self.duration = 10  # Duration in seconds the power-up remains visible

        # Animation properties
        self.animation_angle = 0  # Current rotation angle
        self.float_offset = 0  # Current floating offset
        self.original_y = y  # Original y position for floating animation reference

    def update(self):
        """
        Update the power-up's animation and check if it should be removed.
        Creates floating and rotating effects to make the power-up more visible.
        """
        # Rotation animation
        self.animation_angle += 2
        if self.animation_angle >= 360:
            self.animation_angle = 0

        # Vertical floating effect using sine wave
        self.float_offset = math.sin(time.time() * 2) * 5  # Oscillate 5 pixels up and down
        self.rect.y = self.original_y + self.float_offset

        # Rotate the image around its center
        original_center = self.rect.center
        new_image = pygame.transform.rotate(self.image, self.animation_angle)
        self.rect = new_image.get_rect(center=original_center)

        # Check if the power-up has expired
        if time.time() - self.spawn_time > self.duration:
            self.kill()  # Remove the power-up if it's been visible too long

    def apply_power(self, player):
        """
        Apply the power-up effect to the player who collected it.

        Args:
            player: The player who collects the power-up
        """
        # Get the power type name
        power_name = self.power_types[self.power_type]["name"]


        # Apply effect based on power-up type
        if power_name == "damage":
            # Double damage for 3 turns
            player.attack = player.attack * 2
            player.power_effects.append({"type": "damage", "duration": 3})

        elif power_name == "heal":
            # Restore 50% of max health
            heal_amount = player.max_health * 0.5
            player.health = min(player.max_health, player.health + heal_amount)

        elif power_name == "explosion":
            # Enable explosion mode for the next shot
            player.explosion_mode = True

        elif power_name == "size":
            # Increase projectile size for 2 turns
            player.projectile_size = 2  # Size multiplier
            player.power_effects.append({"type": "size", "duration": 2})

        self.kill()  # Remove the power-up after use


class PowerManager:
    """
    Manages all power-ups in the game, including spawning, updating, and collision detection.
    Controls when and where new power-ups appear.
    """

    def __init__(self, game):
        """
        Initialize the power-up manager.

        Args:
            game: Reference to the main game instance
        """
        self.game = game
        self.all_powers = pygame.sprite.Group()  # Group to store all active power-ups
        self.spawn_timer = 0
        self.spawn_interval = 15  # Time between power-up spawns in seconds
        self.last_spawn_time = time.time()

    def update(self):
        """
        Update all power-ups and check for collisions with player projectiles.
        Also handles spawning new power-ups at regular intervals.
        """
        current_time = time.time()

        # Update all existing power-ups
        for power in self.all_powers:
            power.update()

        # Check for collisions between projectiles and power-ups
        for player in self.game.all_players:
            for projectile in player.all_projectile:
                for power in pygame.sprite.spritecollide(projectile, self.all_powers, False):
                    power.apply_power(player)  # Apply power-up effect to the player who hit it

        # Check if it's time to spawn a new power-up
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_power()
            self.last_spawn_time = current_time

    def spawn_power(self):
        """
        Create a new power-up at a random position on the screen.
        Avoids spawning too close to edges or directly on players.
        """
        # Define random spawn area (avoiding screen edges)
        min_x = self.game.screen.get_width() * 0.2
        max_x = self.game.screen.get_width() * 0.8
        min_y = self.game.screen.get_height() * 0.2
        max_y = self.game.screen.get_height() * 0.7

        # Generate random position within defined area
        x = random.randint(int(min_x), int(max_x))
        y = random.randint(int(min_y), int(max_y))

        # Choose a random power-up type (1-4)
        power_type = random.randint(1, 4)

        # Create the power-up and add it to the group
        power = Power(self.game, x, y, power_type)
        self.all_powers.add(power)

    def draw(self, screen):
        """
        Draw all active power-ups on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        self.all_powers.draw(screen)