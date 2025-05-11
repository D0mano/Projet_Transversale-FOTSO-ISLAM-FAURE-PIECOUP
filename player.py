import pygame
import time
import math
from boulet_canon import Projectile

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)


class Player(pygame.sprite.Sprite):
    """
    Represents a player in the cannon battle game.
    Handles player movement, cannon aiming, firing, health management, and power-up effects.
    """

    def __init__(self, game, level, x, y, direction=1):
        """
        Initialize a player with a cannon.

        Args:
            game: Reference to the main game instance
            level: Current game level
            x, y: Initial position coordinates
            direction: 1 for facing right, -1 for facing left
        """
        super().__init__()
        self.direction = direction
        self.game = game
        self.level = level

        # Player stats
        self.attack = 20  # Base attack damage
        self.health = 100  # Current health
        self.max_health = 100  # Maximum health
        self.angle = 0  # Current cannon angle in degrees
        self.power = 20  # Current firing power
        self.alive = True  # Player alive status

        # Projectile management
        self.all_projectile = pygame.sprite.Group()  # Group to store player's projectiles
        self.projectile_size = 1  # Default projectile size multiplier

        # Load and scale cannon base image
        self.pied_canon = pygame.image.load("assets_game_PT/canon/_pied_Canon_1-removebg-preview.png").convert_alpha()
        self.pied_canon = pygame.transform.scale(self.pied_canon, (60, 60))

        # Load and scale cannon barrel image
        self.original_canon = pygame.image.load("assets_game_PT/canon/_Canon_2-removebg-preview.png").convert_alpha()
        self.original_canon = pygame.transform.scale(self.original_canon, (60, 60))

        # Flip images if player is facing left
        if direction == -1:
            self.original_canon = pygame.transform.flip(self.original_canon, True, False)
            self.pied_canon = pygame.transform.flip(self.pied_canon, True, False)

        self.canon = self.original_canon

        # Setup collision rectangles for cannon and base
        self.rect = self.canon.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_pied = self.pied_canon.get_rect()
        self.rect_pied.x = x
        self.rect_pied.y = y

        # Power-up effects management
        self.power_effects = []  # List to track active power-up effects
        self.explosion_mode = False  # Whether next projectile will explode

    def update_health_bar(self, surface):
        """
        Draw the player's health bar on the screen.

        Args:
            surface: Pygame surface to draw on
        """
        # Define colors for the health bar
        bar_color = (255, 0, 0)  # Red for current health
        bar_back_color = (116, 115, 116)  # Gray for health bar background

        # Set position and dimensions based on player direction
        if self.direction == 1:  # Right-facing player (left side of screen)
            bar_pos = [self.game.screen.get_width() / 20, 50, self.health * 4, 20]
            bar_back_pos = [self.game.screen.get_width() / 20, 50, self.max_health * 4, 20]
        else:  # Left-facing player (right side of screen)
            bar_pos = [self.game.screen.get_width() / 1.51, 50, self.health * 4, 20]
            bar_back_pos = [self.game.screen.get_width() / 1.51, 50, self.max_health * 4, 20]

        # Draw the health bar background and foreground
        pygame.draw.rect(surface, bar_back_color, bar_back_pos)
        pygame.draw.rect(surface, bar_color, bar_pos)

    def update_power_effects(self):
        """
        Update and manage active power-up effects.
        Reduces duration of effects after player fires and removes expired effects.
        """
        effects_to_remove = []

        # Process each active power effect
        for effect in self.power_effects:
            effect["duration"] -= 1

            # Check if effect has expired
            if effect["duration"] <= 0:
                effects_to_remove.append(effect)

                # Reset stats when effects expire
                if effect["type"] == "damage":
                    self.attack = 20  # Reset to base attack value
                elif effect["type"] == "size":
                    self.projectile_size = 1  # Reset to base projectile size

        # Remove expired effects
        for effect in effects_to_remove:
            self.power_effects.remove(effect)

    def damage(self, amount):
        """
        Apply damage to the player and check if they're defeated.

        Args:
            amount: Amount of damage to apply
        """
        if self.health > amount:
            self.health -= amount
        else:
            # Player is defeated
            self.alive = False
            self.game.end_game()  # Trigger game end

    def cal_pos(self):
        """
        Calculate and set the player's position on screen.
        Positions are set based on screen dimensions and player direction.
        """
        if self.direction == 1:  # Right-facing player (left side)
            self.rect.x = self.game.screen.get_width() / 64
            self.rect_pied.x = self.rect.x
        else:  # Left-facing player (right side)
            self.rect.x = self.game.screen.get_width() / 1.067
            self.rect_pied.x = self.rect.x

        # Set vertical position
        self.rect.y = self.game.screen.get_height() / 1.38
        self.rect_pied.y = self.rect.y

    def reinitialize_canon(self):
        """
        Reset the cannon angle and power to default values.
        Used after firing to prepare for the next shot.
        """
        self.angle = 0
        self.power = 20
        self.canon = pygame.transform.rotate(self.original_canon, self.angle * self.direction)
        self.rect = self.canon.get_rect(center=self.rect.center)

    def fire(self):
        """
        Fire a projectile from the cannon.
        Creates a new projectile, applies power-up effects, and resets the cannon.
        """
        # Create a new projectile
        projectile = Projectile(self, self.level, self.game)
        self.all_projectile.add(projectile)

        # Reset cannon and update power effects
        self.reinitialize_canon()
        self.update_power_effects()

        # Apply size power-up if active
        if self.projectile_size > 1:
            projectile.image = pygame.transform.scale(
                projectile.image,
                (int(20 * self.projectile_size), int(20 * self.projectile_size))
            )
            projectile.rect = projectile.image.get_rect(center=projectile.rect.center)

        # Apply explosion power-up if active
        if self.explosion_mode:
            projectile.explosive = True
            self.explosion_mode = False  # Disable after use

    def aim_up(self):
        """
        Increase the cannon's angle (aim higher).
        Limited to a maximum of 90 degrees.
        """
        if self.angle < 90:
            self.angle += 5
            self.canon = pygame.transform.rotate(self.original_canon, self.angle * self.direction)
            self.rect = self.canon.get_rect(center=self.rect.center)

    def aim_down(self):
        """
        Decrease the cannon's angle (aim lower).
        Limited to a minimum of 0 degrees.
        """
        if self.angle > 0:
            self.angle -= 5
            self.canon = pygame.transform.rotate(self.original_canon, self.angle * self.direction)
            self.rect = self.canon.get_rect(center=self.rect.center)

    def power_up(self):
        """
        Increase the firing power.
        Limited to a maximum of 30.
        """
        if self.power < 30:
            self.power += 2

    def power_down(self):
        """
        Decrease the firing power.
        Limited to a minimum of 0.
        """
        if self.power > 0:
            self.power -= 2

    def show_info(self):
        """
        Create text surfaces showing the current angle and power.

        Returns:
            Tuple of text surfaces (angle_text, power_text)
        This methode is only use for debugging
        """
        angle_text = font.render(f"Angle: {self.angle}°", True, (255, 255, 255))
        power_text = font.render(f"Power: {self.power}", True, (255, 255, 255))
        return angle_text, power_text

    def draw_trajectory(self, surface):
        """
        Draw a predicted trajectory path for the projectile.
        Shows a series of points indicating where the projectile might travel.

        Args:
            surface: Pygame surface to draw on
        """
        points = []
        velocity = self.power
        angle_rad = math.radians(self.angle)

        # Starting position of the projectile
        start_x = self.rect.centerx
        start_y = self.rect.centery

        # Calculate velocity components
        vx = velocity * math.cos(angle_rad) * self.direction
        vy = -velocity * math.sin(angle_rad)

        # Set gravity based on current level
        if self.level.lv_number == 1:
            gravity = 0.25
        if self.level.lv_number == 2:
            gravity = 0.1
        if self.level.lv_number == 3:
            gravity = 0.5

        # Calculate trajectory points
        for t in range(1, 10):
            # Physics formulas for projectile motion
            dx = vx * t
            dy = vy * t + 0.5 * gravity * t ** 2
            point = (int(start_x + dx), int(start_y + dy))

            # Stop calculating if point is off-screen
            if point[1] > self.game.screen.get_height() or point[0] < 0 or point[0] > self.game.screen.get_width():
                break

            points.append(point)

        # Draw each point as a small yellow circle
        for point in points:
            pygame.draw.circle(surface, (255, 255, 0), point, 3)