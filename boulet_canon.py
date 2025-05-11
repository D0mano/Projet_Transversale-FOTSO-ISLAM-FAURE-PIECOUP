import pygame
import math
from anim_powers import Explosion

pygame.init()


class Projectile(pygame.sprite.Sprite):
    """
    Represents a projectile (cannonball) fired by a player.
    Handles movement, collisions, and explosions.
    """

    def __init__(self, player, level, game):
        """
        Initialize a projectile.

        Args:
            player: The player who fired the projectile
            level: Current game level, providing gravity and environmental info
            game: Game instance to interact with other game elements
        """
        super().__init__()
        self.visible = True
        self.level = level
        self.game = game

        # Different projectile images based on level number
        self.images = ["assets_game_PT/canon/boulet_de_canon-removebg-preview.png",
                       "assets_game_PT/canon/boulet_canon_space.png",
                       "assets_game_PT/canon/boulet_de_canon-removebg-preview.png"]

        self.user = player  # Reference to the player who fired this projectile

        # Load the appropriate image based on level
        self.image = pygame.image.load(self.images[self.level.lv_number - 1])

        # Scale the projectile based on the player's projectile size setting
        self.image = pygame.transform.scale(self.image,
                                            (20 * self.user.projectile_size, 20 * self.user.projectile_size))

        self.rect = self.image.get_rect()
        self.death_rect = None

        # Load sound effects
        self.canon_sound = pygame.mixer.Sound("assets_game_PT/sound/sf_canon_01.mp3")
        self.explosion_sound = pygame.mixer.Sound("assets_game_PT/sound/medium-explosion-40472.mp3")

        # Explosion properties
        self.explosive = False  # Whether this projectile creates an area explosion on impact
        self.explosion_radius = 200  # Radius of explosion effect in pixels
        self.explosion_damage = 50  # Base damage of the explosion

        # Calculate the starting position based on the player's cannon angle
        if player.direction == 1:
            canon_length = 13  # Cannon length for right-facing player
        else:
            canon_length = 5  # Cannon length for left-facing player

        # Convert angle to radians for trigonometric calculations
        self.angle_rad = math.radians(player.angle)

        # Calculate the offset from player position based on cannon length and angle
        offset_x = canon_length * math.cos(self.angle_rad)
        offset_y = canon_length * math.sin(self.angle_rad)

        # Position the projectile at the end of the cannon
        if player.direction == 1:
            self.rect.x = player.rect.centerx - offset_x
        else:
            self.rect.x = player.rect.centerx + offset_x

        self.rect.y = player.rect.centery - offset_y

        # Physics properties
        self.gravity = self.level.gravity
        self.power = player.power  # Firing power from the player

        # Calculate velocity components using trigonometry
        self.vel_x = self.power * math.cos(self.angle_rad)  # Horizontal velocity
        self.vel_y = -self.power * math.sin(self.angle_rad)  # Vertical velocity (negative because y increases downward)
        self.time = 0  # Time since projectile was fired, used for gravity calculations

    def create_explosion(self):
        """
        Creates an explosion at the projectile's current position.
        Handles both visual effects and damage to nearby players.
        """
        # Visual explosion effect
        explosion = Explosion(self.rect.centerx, self.rect.centery, 3, 3, 666, 666, 3)
        self.game.all_explosion.add(explosion)

        # Check for players within the explosion radius
        for player in self.game.all_players:
            # Calculate distance between explosion center and player
            distance = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 +
                                 (player.rect.centery - self.rect.centery) ** 2)

            # If player is within explosion radius
            if distance <= self.explosion_radius:
                # Damage decreases with distance from explosion center
                damage_factor = 1 - (distance / self.explosion_radius)
                damage = int(self.explosion_damage * damage_factor)

                if player != self.user:  # Don't damage the player who fired the projectile
                    player.damage(damage)

    def move(self, dt):
        """
        Update the projectile's position based on physics.
        Handles collisions with terrain, players, and boundaries.

        Args:
            dt: Delta time (time since last frame)
        """
        # Play the firing sound at the beginning
        if self.time == 0:
            self.canon_sound.play()

        # Update time counter
        self.time += dt

        # Update position using physics equations:
        # Horizontal motion: constant velocity
        self.rect.x += int(self.vel_x * self.user.direction)

        # Vertical motion: initial velocity + acceleration due to gravity
        self.rect.y += int(0.5*self.gravity * self.time **2 + self.vel_y)


        # Check if projectile hit the ground
        if self.rect.y > self.level.pos_y + 30:
            if self.explosive:
                self.create_explosion()
            self.explosion_sound.play()
            self.kill()  # Remove the projectile

        # Check collisions with players
        for player in self.game.check_collision(self, self.game.all_players):
            if player != self.user:  # Don't damage the player who fired the projectile
                if self.explosive:
                    self.create_explosion()
                self.explosion_sound.play()
                self.kill()  # Remove the projectile
                player.damage(self.user.attack)  # Apply direct damage to hit player

        # Check collisions with obstacles
        for obstacle in self.game.check_collision(self, self.level.all_obstacle):
            self.explosion_sound.play()
            if self.explosive:
                self.create_explosion()
            self.explosion_sound.play()
            self.kill()  # Remove the projectile