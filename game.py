import pygame
from player import Player

class Game:
    def __init__(self,level):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.player =[Player(self,level,20,level.pos_y,1),Player(self,level,1200,level.pos_y,-1)]
        self.level = level
        for player in self.player:
            self.all_players.add(player)
        self.is_paused = False
        self.running = True
        self.waiting = False

        self.current_player = 0 #Represent the index of the player currently playing

    def start(self,ecran,dt):
        # Load the background and the obstacle of the Level
        ecran.blit(self.level.image, (0, 0))
        ecran.blit(self.level.obstacle.image, (self.level.obstacle.rect.x, self.level.obstacle.rect.y))
        self.level.obstacle.move_obstacle()

        # Load the player model
        ecran.blit(self.player[0].pied_canon, (self.player[0].rect_pied.x, self.player[0].rect_pied.y))
        ecran.blit(self.player[1].pied_canon, (self.player[1].rect_pied.x, self.player[1].rect_pied.y))
        ecran.blit(self.player[0].canon, self.player[0].rect.topleft)
        ecran.blit(self.player[1].canon, self.player[1].rect.topleft)

        # Load the shooting information
        ecran.blit(self.player[self.current_player].show_info()[0],
                   (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50, 650))
        ecran.blit(self.player[self.current_player].show_info()[1],
                   (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50, 600))

        # Load the canon of all the players
        for players in self.player:
            for projectile in players.all_projectile:
                projectile.move(dt)

        # Load the players healths bar
        for players in self.player:
            players.all_projectile.draw(ecran)
            players.update_health_bar(ecran)

        pygame.display.flip()

        # Loop for the keys
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self.is_playing = False
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = True
                    self.pause_menu(ecran)

                if event.key == pygame.K_SPACE:
                    self.player[self.current_player].fire()
                    self.switch_turn()

                if self.current_player == 0:
                    if event.key == pygame.K_RIGHT:
                        self.player[self.current_player].power_up()

                    elif event.key == pygame.K_LEFT:
                        self.player[self.current_player].power_down()
                else:
                    if event.key == pygame.K_LEFT:
                        self.player[self.current_player].power_up()

                    elif event.key == pygame.K_RIGHT:
                        self.player[self.current_player].power_down()

                if event.key == pygame.K_UP:
                    self.player[self.current_player].aim_up()

                elif event.key == pygame.K_DOWN:
                    self.player[self.current_player].aim_down()

    def menu(self,ecran):
        # We load the different asset for the menu

        background = pygame.image.load("assets_game_PT/Background_menu.png").convert_alpha()
        banner = pygame.image.load("assets_game_PT/CANON_MASTER_Logo-removebg-preview.png").convert_alpha()

        banner_rect = banner.get_rect()
        banner_rect.x = (ecran.get_width() / 2) - 250
        banner_rect.y = ecran.get_height() - 800

        play_button_white = pygame.image.load("assets_game_PT/button/play_button_white.png").convert_alpha()
        play_button_green = pygame.image.load("assets_game_PT/button/play_button_green.png").convert_alpha()
        play_button_rect = play_button_green.get_rect()
        play_button_rect.x = ecran.get_width() / 2 - 150
        play_button_rect.y = ecran.get_height() / 3

        quit_button_white = pygame.image.load("assets_game_PT/button/quit_button_white.png").convert_alpha()
        quit_button_red = pygame.image.load("assets_game_PT/button/quit_button_red.png").convert_alpha()
        quit_button_rect = quit_button_red.get_rect()
        quit_button_rect.x = ecran.get_width() / 2 - 150
        quit_button_rect.y = ecran.get_height() / 3 + 150

        play_button = play_button_white
        quit_button = quit_button_white

        while self.running and not self.is_playing:
            ecran.blit(background, (0, 0))
            ecran.blit(banner, banner_rect)
            ecran.blit(play_button, play_button_rect)
            ecran.blit(quit_button, quit_button_rect)

            # Handle input events for quitting and menu interaction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEMOTION:
                    if play_button_rect.collidepoint(event.pos):
                        play_button = play_button_green
                    else:
                        play_button = play_button_white
                    if quit_button_rect.collidepoint(event.pos):
                        quit_button = quit_button_red
                    else:
                        quit_button = quit_button_white
                elif event.type == pygame.MOUSEBUTTONUP:
                    if play_button_rect.collidepoint(event.pos):
                        self.is_playing = True  # Start the game when play is clicked
                    elif quit_button_rect.collidepoint(event.pos):
                        self.running = False  # Quit the game when quit is clicked
            pygame.display.flip()  # Update the display to the screen

    def pause_menu(self, ecran):
        # Dessiner un fond semi-transparent
        pause_overlay = pygame.Surface(ecran.get_size(), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 180))  # Couleur noire avec transparence
        ecran.blit(pause_overlay, (0, 0))
        backgrounds_copy = ecran.copy()
        # Charger les images des boutons
        resume_button_white = pygame.image.load("assets_game_PT/button/RESUME_button_white-removebg-preview.png").convert_alpha()
        options_button_white = pygame.image.load("assets_game_PT/button/OPTION_button_white-removebg-preview.png").convert_alpha()
        quit_button_white = pygame.image.load("assets_game_PT/button/QUIT_button_white2-removebg-preview.png").convert_alpha()

        resume_button_gray = pygame.image.load(
            "assets_game_PT/button/RESUME_button_gray-removebg-preview.png").convert_alpha()
        options_button_gray = pygame.image.load(
            "assets_game_PT/button/OPTION_button_gray-removebg-preview.png").convert_alpha()
        quit_button_gray = pygame.image.load(
            "assets_game_PT/button/QUIT_button_gray-removebg-preview.png").convert_alpha()

        # Positionner les boutons
        resume_rect = resume_button_white.get_rect(center=(ecran.get_width() // 2,ecran.get_width()/6.4))
        options_rect = options_button_white.get_rect(center=(ecran.get_width() // 2, ecran.get_width()/ 3.6))
        quit_rect = quit_button_white.get_rect(center=(ecran.get_width() // 2, ecran.get_width()/2.56))


        resume_button = resume_button_white
        options_button = options_button_white
        quit_button = quit_button_white
        # Afficher les boutons



        # Boucle du menu pause
        while self.is_paused:
            ecran.blit(backgrounds_copy,(0,0))
            ecran.blit(resume_button, resume_rect)
            ecran.blit(options_button, options_rect)
            ecran.blit(quit_button, quit_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEMOTION:
                    if resume_rect.collidepoint(event.pos):
                        resume_button = resume_button_gray

                    else:
                        resume_button = resume_button_white

                    if options_rect.collidepoint(event.pos):
                        options_button = options_button_gray

                    else:
                        options_button = options_button_white

                    if quit_rect.collidepoint(event.pos):
                        quit_button = quit_button_gray

                    else:
                        quit_button = quit_button_white

                elif event.type == pygame.MOUSEBUTTONUP:
                    if resume_rect.collidepoint(event.pos):
                        self.is_paused = False  # Reprendre le jeu
                    elif quit_rect.collidepoint(event.pos):
                        self.is_playing = False  # Retour au menu principal
                        self.is_paused = False
                    elif options_rect.collidepoint(event.pos):
                        self.waiting = True
                        self.options_menu(ecran)  # Afficher le menu des options


                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = False  # Reprendre le jeu
            pygame.display.flip()

    def options_menu(self, ecran):
        backgrounds_copy = ecran.copy()

        options_overlay = pygame.Surface(ecran.get_size(), pygame.SRCALPHA)
        options_overlay.fill((50, 50, 50, 200))  # Fond semi-transparent
        ecran.blit(options_overlay, (0, 0))

        font = pygame.font.Font(None, 50)
        text = font.render("Options Menu - Press ESC to go back", True, (255, 255, 255))
        ecran.blit(text, (100, 200))
        pygame.display.flip()

        # Attente d'une action pour quitter les options

        while self.waiting:


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.waiting = False
        ecran.blit(backgrounds_copy,(0,0))
        pygame.display.flip()




    def switch_turn(self):
        self.current_player = 1 - self.current_player

    def check_collision(self,sprite,group):
       return pygame.sprite.spritecollide(sprite,group,False)