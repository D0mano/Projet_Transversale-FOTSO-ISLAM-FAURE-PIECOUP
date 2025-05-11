import pygame


class Obstacle(pygame.sprite.Sprite):
    """
    Represents a moving obstacle in the game that players must avoid or shoot around.
    Different obstacle types are used based on the current level.
    """

    def __init__(self, level, x, y):
        """
        Initialize an obstacle.

        Args:
            level: Current game level that provides environment info
            x: Initial x-coordinate position
            y: Initial y-coordinate position
        """
        super().__init__()
        self.level = level

        # List of obstacle image paths for different levels
        self.type_obstacle = ["assets_game_PT/obstacles/muraille.png",  # Level 1: Wall
                              "assets_game_PT/obstacles/meteorite.png",  # Level 2: Meteorite
                              "assets_game_PT/obstacles/coraux.png"]  # Level 3: Coral

        # Load the appropriate obstacle image based on current level
        self.image = pygame.image.load(self.type_obstacle[self.level.lv_number - 1]).convert_alpha()

        # Scale the obstacle image based on the level
        if level.lv_number == 1:
            self.image = pygame.transform.scale(self.image, (40, 120))  # Thinner and taller for wall
        elif level.lv_number == 2:
            self.image = pygame.transform.scale(self.image, (100, 200))  # Wider for meteorite
        elif level.lv_number == 3:
            self.image = pygame.transform.scale(self.image, (100, 200))  # Same size for coral

        # Set up the collision rectangle
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Movement properties
        self.velocity = 5  # Speed of obstacle movement
        self.direction = 1  # 1 = moving down, -1 = moving up

    def move_obstacle(self):
        """
        Updates the obstacle position and handles movement boundaries.
        Obstacles move vertically and reverse direction when hitting top or bottom boundaries.
        """
        # Move the obstacle vertically based on velocity and direction
        self.rect.y += self.velocity * self.direction

        # Check boundaries and reverse direction when needed
        # Each level has different boundaries for obstacle movement
        if self.level.lv_number == 1:
            # Level 1: Wall - Smaller movement range
            if self.rect.y < self.level.screen.get_height() / 102 or self.rect.y >= self.level.pos_y - self.level.screen.get_height() / 9:
                self.direction *= -1  # Reverse direction
        elif self.level.lv_number == 2:
            # Level 2: Meteorite - Larger movement range
            if self.rect.y < self.level.screen.get_height() / 102 or self.rect.y >= self.level.pos_y - self.level.screen.get_height() / 4.8:
                self.direction *= -1  # Reverse direction
        elif self.level.lv_number == 3:
            # Level 3: Coral - Same range as level 2
            if self.rect.y < self.level.screen.get_height() / 102 or self.rect.y >= self.level.pos_y - self.level.screen.get_height() / 4.8:
                self.direction *= -1  # Reverse direction

    def cal_pos_obs(self):
        """
        Resets the obstacle to the center of the screen.
        This method is used to reset or initialize the obstacle position.
        """
        # Position the obstacle at the center of the screen
        self.rect.x = self.level.screen.get_width() / 2
        self.rect.y = self.level.screen.get_height() / 2