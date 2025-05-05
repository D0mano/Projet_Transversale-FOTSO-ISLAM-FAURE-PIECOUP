import pygame

# Initialisation
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

# Charger la sprite sheet
sprite_sheet = pygame.image.load("mon_animation.png").convert_alpha()

# Paramètres (ADAPTE à ton image !)
SPRITE_WIDTH = 100  # Largeur d'une frame
SPRITE_HEIGHT = 100  # Hauteur d'une frame
NUM_FRAMES = 6  # Nombre total de frames
current_frame = 0

# Découper les frames
frames = []
for i in range(NUM_FRAMES):
    frame = sprite_sheet.subsurface((i * SPRITE_WIDTH, 0, SPRITE_WIDTH, SPRITE_HEIGHT))
    frames.append(frame)

# Boucle principale
running = True
while running:
    screen.fill((0, 0, 0))  # Fond noir
    screen.blit(frames[current_frame], (100, 100))  # Afficher la frame actuelle
    current_frame = (current_frame + 1) % NUM_FRAMES  # Changer de frame

    pygame.display.flip()
    clock.tick(10)  # Vitesse de l’animation

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
