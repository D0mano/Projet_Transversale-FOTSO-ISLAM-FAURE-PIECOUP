import pygame
from game import Game
from level import Level

# Initialize pygame library
pygame.init()
# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Main game loop control flag
run = True

# Set up the display window in fullscreen mode
ecran = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
# Initialize the level object with the screen surface
level = Level(ecran)
# Set the window caption/title
pygame.display.set_caption("CanonMaster")

# Initialize the main game object with level and screen references
game = Game(level, ecran)

while run:  # Main game loop
    # Calculate delta time in seconds (for frame-independent movement)
    dt = clock.tick(60)/1000.0  # Target 60 FPS

    # Check game state and handle accordingly
    if game.is_playing:
        # If currently in gameplay state, update game logic
        game.start(dt)
    else:
        # If not playing, show the menu screen
        game.menu()
        # Update run flag based on game.running (allows menu to exit game)
        run = game.running

    # Event handling loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game if the window close button is clicked
            run = False

    # Update the entire display surface to the screen
    pygame.display.flip()

# Clean up pygame resources when exiting
pygame.quit()