import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size=1):
        super().__init__()
        self.images = []
        # Chargez les images d'explosion (vous devrez les créer ou les télécharger)
        for i in range(1, 9):  # Supposons que vous avez 8 images d'explosion
            img = pygame.image.load(f"assets_game_PT/animations/explosion_nuke/Explosion_{i}.jpg").convert_alpha()
            # Redimensionner selon la taille souhaitée
            #img = pygame.transform.scale(img, (int(64 * size), int(64 * size)))
            self.images.append(img)

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y-50)
        self.counter = 0
        self.animation_speed = 3  # Plus petit = plus rapide

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