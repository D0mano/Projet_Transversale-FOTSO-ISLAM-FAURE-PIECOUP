import pygame

# Découper les frames


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y,col,row,frame_width,frame_height,size=1):
        super().__init__()
        self.img = pygame.image.load(f"assets_game_PT/animations/explosion_nuke/Explosion.png")
        self.images = []
        # Chargez les images d'explosion (vous devrez les créer ou les télécharger)
        for r in range(row):
            for c in range(col):
                rect = pygame.Rect(r * frame_width, c * frame_height, frame_width, frame_height)
                frame = self.img.subsurface(rect)
                frame = pygame.transform.scale(frame, (int(64 * size), int(64 * size)))
                self.images.append(frame)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-100)
        self.counter = 0
        self.animation_speed = 5  # Plus petit = plus rapide

    def update(self):
        # Mettre à jour le compteur
        self.counter += 1

        # Changer d'image quand le compteur atteint une certaine valeur
        if self.counter >= self.animation_speed:
            self.counter = 0
            self.index += 1

            # Si nous avons atteint la fin de l'animation, supprimez le sprite
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]