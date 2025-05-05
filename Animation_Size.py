class Bubble:
    def __init__(self, x, y, bubble_type="normal"):
        self.x = x
        self.y = y
        self.radius = 15
        self.bubble_type = bubble_type
        self.is_popped = False
        self.contains_buff = bubble_type == "buff"

        self.color = (255,255,255)

    def draw(self, screen):
        pass


class Player:
    def __init__(self):
        self.x = 400
        self.y = 500
        self.bullets = []


def game_loop():
    # Initialisation
    player = Player()
    bubbles = []

    for i in range(10):
        bubbles.append(Bubble(random.randint(50, 750), random.randint(50, 300)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Mises à jour
        player.update(bubbles, ball)
        ball.update()