import pygame


# Split frames into a spritesheet


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, col, row, frame_width, frame_height, size=1):
        """
        Initialize an explosion animation sprite.

        Args:
            x, y: Position coordinates for the explosion center
            col, row: Number of columns and rows in the spritesheet
            frame_width, frame_height: Width and height of each frame in pixels
            size: Scale factor for the explosion (default 1)
        """
        super().__init__()
        # Load the main explosion spritesheet image
        self.img = pygame.image.load("assets_game_PT/animations/explosion_nuke/Explosion.png")
        self.images = []

        # Extract individual frames from the spritesheet
        # Load explosion images (you'll need to create or download them)
        for r in range(row):
            for c in range(col):
                # Define rectangle for the current frame
                rect = pygame.Rect(r * frame_width, c * frame_height, frame_width, frame_height)
                # Extract the frame from the spritesheet
                frame = self.img.subsurface(rect)
                # Scale the frame based on the size parameter
                frame = pygame.transform.scale(frame, (int(64 * size), int(64 * size)))
                # Add the frame to our animation sequence
                self.images.append(frame)

        # Initialize animation properties
        self.index = 0  # Current frame index
        self.image = self.images[self.index]  # Current displayed image
        self.rect = self.image.get_rect()  # Rectangle for collision detection
        self.rect.center = (x, y - 100)  # Position the explosion (offset by 100px vertically)
        self.counter = 0  # Counter for animation timing
        self.animation_speed = 5  # Lower value = faster animation

    def update(self):
        """
        Update the explosion animation - called every frame.
        Advances to next frame based on animation_speed and
        automatically removes the sprite when animation completes.
        """
        # Update the counter
        self.counter += 1

        # Change image when counter reaches the animation speed threshold
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1

            # If we've reached the end of the animation, remove the sprite
            if self.index >= len(self.images):
                self.kill()  # Remove sprite from all groups
            else:
                self.image = self.images[self.index]  # Update to next frame