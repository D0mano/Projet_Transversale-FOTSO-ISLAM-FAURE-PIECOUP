import pygame
import sys
from obstacle import Obstacle

pygame.init()


class Level:
    """
    Level class responsible for managing game level properties including
    background, ground position, gravity, and obstacles.
    """

    def __init__(self, screen, level=1):
        """
        Initialize a level with specific properties based on the level number.

        Args:
            screen: The pygame display surface where the level will be rendered
            level: The level number (1, 2, or 3), defaults to 1
        """
        self.lv_number = level
        # List of background images for different levels
        self.background = ["assets_game_PT/background/Background_1-fotor2.png",
                           "assets_game_PT/background/Background_space.png",
                           "assets_game_PT/background/Background_under_water.png"]
        self.screen = screen

        # Load and scale the background image to fit the screen
        self.true_image = pygame.image.load(self.background[self.lv_number - 1]).convert_alpha()
        self.image = pygame.transform.scale(self.true_image, (self.screen.get_width(), self.screen.get_height()))

        # Set level-specific properties based on the level number
        if self.lv_number == 1:
            # Ground position for level 1
            self.pos_y = screen.get_height() / 1.38
            # Gravity strength for level 1
            self.gravity = 50
            # Create an obstacle at the center of the screen
            self.obstacle = Obstacle(self, screen.get_width() / 2 - 20, self.screen.get_height() / 2)

        elif self.lv_number == 2:
            # Ground position for level 2 (space level)
            self.pos_y = screen.get_height() / 1.22
            # Lower gravity for space level
            self.gravity = 20
            # Create an obstacle at the center of the screen
            self.obstacle = Obstacle(self, screen.get_width() / 2 - 40, self.screen.get_height() / 2)
        elif self.lv_number == 3:
            # Ground position for level 3 (underwater level)
            self.pos_y = screen.get_height() / 1.22
            # Higher gravity for underwater level
            self.gravity = 80
            # Create an obstacle at the center of the screen
            self.obstacle = Obstacle(self, screen.get_width() / 2 - 40, self.screen.get_height() / 2)

        # Create a sprite group to manage all obstacles in the level
        self.all_obstacle = pygame.sprite.Group()
        self.all_obstacle.add(self.obstacle)

    def load_level(self):
        """
        Render the level on the screen.
        This method draws the background and updates obstacle positions.
        """
        # Draw the background image on the screen
        self.screen.blit(self.image, (0, 0))
        # Draw the obstacle at its current position
        self.screen.blit(self.obstacle.image, (self.obstacle.rect.x, self.obstacle.rect.y))
        # Update obstacle movement
        self.obstacle.move_obstacle()