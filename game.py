import sys
import pygame
from player import Player
from level import Level

class Game:
    def __init__(self,level,ecran):
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.screen = ecran
        self.player =[Player(self,level,self.screen.get_width()/64,level.pos_y,1),Player(self,level,self.screen.get_width()/1.067,level.pos_y,-1)]
        self.level = level
        for player in self.player:
            self.all_players.add(player)
        self.is_paused = False
        self.running = True
        self.waiting = False
        self.in_menu = True

        self.current_player = 0 #Represent the index of the player currently playing
        self.volume = 100
        if self.volume == 0:
            self.mute = True
        else:
            self.mute = False

    def start(self,dt):
        self.in_menu = False

        self.level.load_level()
        # Load the player model
        self.screen.blit(self.player[0].pied_canon, (self.player[0].rect_pied.x, self.player[0].rect_pied.y))
        self.screen.blit(self.player[1].pied_canon, (self.player[1].rect_pied.x, self.player[1].rect_pied.y))
        self.screen.blit(self.player[0].canon, self.player[0].rect.topleft)
        self.screen.blit(self.player[1].canon, self.player[1].rect.topleft)

        # Load the shooting information
        self.screen.blit(self.player[self.current_player].show_info()[0],
                   (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50, 650))
        self.screen.blit(self.player[self.current_player].show_info()[1],
                   (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50, 600))

        # Load the canon of all the players
        for players in self.player:
            for projectile in players.all_projectile:
                projectile.move(dt)

        # Load the players healths bar
        for players in self.player:
            players.all_projectile.draw(self.screen)
            players.update_health_bar(self.screen)

        pygame.display.flip()

        # Loop for the keys
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self.level.load_level()
                self.level.image = pygame.transform.scale(self.level.true_image, (self.screen.get_width(), self.screen.get_height()))
                for players in self.player:
                    players.cal_pos()
                self.level.obstacle.cal_pos_obs()
            if event.type == pygame.KEYUP:
                if event.key == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.key == pygame.K_f:
                    self.in_menu = True
                    self.game_over()
                if event.key == pygame.K_ESCAPE:
                    self.is_paused = True
                    self.pause_menu()

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


    def game_over(self):
        for player in self.player:
            player.health = player.max_health
            player.reinitialize_canon()
            player.cal_pos()
        self.current_player = 0
        self.is_playing = False
        self.in_menu = True


    def menu(self):
        # We load the different asset for the menu

        background = pygame.image.load("assets_game_PT/background/Background_menu.png").convert_alpha()
        background_resize = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))

        banner = pygame.image.load("assets_game_PT/logo/CANON_MASTER_Logo-removebg-preview.png").convert_alpha()
        banner_resize = pygame.transform.scale(banner,(self.screen.get_width()/2.56,self.screen.get_height()/1.44))

        banner_rect = banner_resize.get_rect(center = (self.screen.get_width()/2,self.screen.get_height()/4))

        play_button_white = pygame.image.load("assets_game_PT/button/play_button_white.png").convert_alpha()
        play_button_white_resize = pygame.transform.scale(play_button_white,(self.screen.get_width()/4.26,self.screen.get_height()/3.6))
        play_button_green = pygame.image.load("assets_game_PT/button/play_button_green.png").convert_alpha()
        play_button_green_resize = pygame.transform.scale(play_button_green,(self.screen.get_width()/4.26,self.screen.get_height()/3.6))
        play_button_rect = play_button_white_resize.get_rect(center = (self.screen.get_width()/2,self.screen.get_height()/2))

        quit_button_white = pygame.image.load("assets_game_PT/button/quit_button_white.png").convert_alpha()
        quit_button_white_resize = pygame.transform.scale(quit_button_white,(self.screen.get_width()/4.26,self.screen.get_height()/3.6))
        quit_button_red = pygame.image.load("assets_game_PT/button/quit_button_red.png").convert_alpha()
        quit_button_red_resize = pygame.transform.scale(quit_button_red,(self.screen.get_width()/4.26,self.screen.get_height()/3.6))
        quit_button_rect = quit_button_white_resize.get_rect(center = (self.screen.get_width()/2,self.screen.get_height()/1.3))


        play_button = play_button_white_resize
        quit_button = quit_button_white_resize
        while self.running and not self.is_playing:
            self.screen.blit(background_resize, (0, 0))
            self.screen.blit(banner_resize, banner_rect)
            self.screen.blit(play_button, play_button_rect)
            self.screen.blit(quit_button, quit_button_rect)

            # Handle input events for quitting and menu interaction
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    background_resize = pygame.transform.scale(background,
                                                               (self.screen.get_width(), self.screen.get_height()))
                    banner_resize = pygame.transform.scale(banner, (
                        self.screen.get_width() / 2.56, self.screen.get_height() / 1.44))
                    banner_rect = banner_resize.get_rect(
                        center=(self.screen.get_width() / 2, self.screen.get_height() / 4))

                    quit_button_red_resize = pygame.transform.scale(quit_button_red, (
                    self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
                    quit_button_white_resize = pygame.transform.scale(quit_button_white, (
                    self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
                    quit_button_rect = quit_button_white_resize.get_rect(
                        center=(self.screen.get_width() / 2, self.screen.get_height() / 1.3))

                    play_button_white_resize = pygame.transform.scale(play_button_white, (
                    self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
                    play_button_green_resize = pygame.transform.scale(play_button_green, (
                    self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
                    play_button_rect = play_button_white_resize.get_rect(
                        center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    if play_button_rect.collidepoint(event.pos):
                        play_button = play_button_green_resize
                    else:
                        play_button = play_button_white_resize
                    if quit_button_rect.collidepoint(event.pos):
                        quit_button = quit_button_red_resize
                    else:
                        quit_button = quit_button_white_resize
                elif event.type == pygame.MOUSEBUTTONUP:
                    if play_button_rect.collidepoint(event.pos):

                        self.level_menu()  # Let you select the level you wants
                        self.in_menu = False
                    elif quit_button_rect.collidepoint(event.pos):
                        self.running = False  # Quit the game when quit is clicked
            pygame.display.flip()  # Update the display to the screen

    def pause_menu(self):
        # Dessiner un fond semi-transparent
        pause_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 180))  # Couleur noire avec transparence
        self.screen.blit(pause_overlay, (0, 0))
        backgrounds_copy = self.screen.copy()
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
        resume_rect = resume_button_white.get_rect(center=(self.screen.get_width() // 2,self.screen.get_width()/6.4))
        options_rect = options_button_white.get_rect(center=(self.screen.get_width() // 2, self.screen.get_width()/ 3.6))
        quit_rect = quit_button_white.get_rect(center=(self.screen.get_width() // 2, self.screen.get_width()/2.56))


        resume_button = resume_button_white
        options_button = options_button_white
        quit_button = quit_button_white
        # Afficher les boutons



        # Boucle du menu pause
        while self.is_paused:
            self.screen.blit(backgrounds_copy,(0,0))
            self.screen.blit(resume_button, resume_rect)
            self.screen.blit(options_button, options_rect)
            self.screen.blit(quit_button, quit_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

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
                        self.game_over() # Retour au menu principal
                        self.in_menu = True
                        self.is_paused = False
                    elif options_rect.collidepoint(event.pos):
                        self.waiting = True
                        self.options_menu()  # Afficher le menu des options


                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = False  # Reprendre le jeu
            pygame.display.flip()

    def options_menu(self):
        backgrounds_copy = self.screen.copy()
        options_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        options_overlay.fill((50, 50, 50, 200))  # Fond semi-transparent
        self.screen.blit(options_overlay, (0, 0))
        options_overlay_copy = self.screen.copy()

        font = pygame.font.Font(None, 50)
        text = font.render("Options Menu - Press ESC to go back", True, (255, 255, 255))
        text_rect = text.get_rect(center = (self.screen.get_width()/ 3,self.screen.get_height() / 3.6) )
        volume = pygame.image.load("assets_game_PT/button/volume.png").convert_alpha()
        volume = pygame.transform.scale(volume,(100,100))
        mute = pygame.image.load("assets_game_PT/button/mute.png").convert_alpha()
        mute = pygame.transform.scale(mute,(100,100))
        level_select = pygame.image.load("assets_game_PT/button/Selecteur_level.png")
        level_select = pygame.transform.scale(level_select,(100,100))

        volume_rect = volume.get_rect(center = (self.screen.get_width() / 8.5 ,self.screen.get_height() / 2.05))
        level_select_rect = level_select.get_rect(center = (self.screen.get_width()/8.5,self.screen.get_height() / 1.2))
        if self.mute == False:
            volume_button = volume
        else:
            volume_button = mute
        pygame.display.flip()

        # Waiting for an input to close the options

        while self.waiting:
            self.screen.blit(options_overlay_copy,(0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(volume_button, volume_rect)
            self.screen.blit(level_select, level_select_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if volume_button == volume and volume_rect.collidepoint(event.pos) and not(self.mute):
                        volume_button = mute
                        self.mute = True
                    else:
                        volume_button = volume
                        self.mute = False
                    if level_select_rect.collidepoint(event.pos):
                        self.waiting = False
                        self.is_paused = False
                        self.is_playing = False
                        self.level_menu()




                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.waiting = False
        if self.is_paused:
            self.screen.blit(backgrounds_copy,(0,0))
            pygame.display.flip()


    def switch_turn(self):
        self.current_player = 1 - self.current_player

    def check_collision(self,sprite,group):
       return pygame.sprite.spritecollide(sprite,group,False)

    def change_level(self,new_level):
        self.level = new_level
        self.player = [Player(self, self.level, self.screen.get_width() / 64, self.level.pos_y, 1),
                       Player(self, self.level, self.screen.get_width() / 1.067, self.level.pos_y, -1),
                       ]
        self.all_players = pygame.sprite.Group()
        for player in self.player:
            self.all_players.add(player)
            self.current_player = 0


    def level_menu(self):
        self.in_menu = False
        background = pygame.image.load("assets_game_PT/background/Background_menu.png").convert_alpha()
        background_resize = pygame.transform.scale(background,(self.screen.get_width(),self.screen.get_height()))

        titre = pygame.image.load("assets_game_PT/logo/MASTER_horozontal (2).png").convert_alpha()
        titre_resize = pygame.transform.scale(titre,(self.screen.get_width()/2.56,self.screen.get_height()/2.4))
        titre_rect = titre_resize.get_rect(center = (self.screen.get_width()/2,self.screen.get_height()/6))

        level_overlay_rect = (self.screen.get_width() /3,self.screen.get_height()/4.5,self.screen.get_width()/3.1,self.screen.get_height()/1.44)

        levels = [Level(self.screen,1),
                  Level(self.screen,2),
                  Level(self.screen,3)]

        font = pygame.font.Font(None, 50)
        buttons = []

        for i,level in enumerate(levels):
            text = font.render(f"Level {i+1}", True, (255, 255, 255))
            rect = text.get_rect(center = (self.screen.get_width()/2,200 + i*100))
            buttons.append((text,rect,level))

        self.screen.blit(background_resize,(0,0))
        pygame.draw.rect(self.screen, (50,30,30), level_overlay_rect, border_radius=20)
        self.screen.blit(titre_resize,titre_rect)
        for text,rect,_ in buttons:
            self.screen.blit(text,rect)
            pygame.display.flip()

        pygame.display.flip()
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    background_resize = pygame.transform.scale(background,(self.screen.get_width(), self.screen.get_height()))
                    pygame.display.flip()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        self.in_menu = True
                if event.type == pygame.MOUSEBUTTONUP:
                    for _,rect,level in buttons:
                        if rect.collidepoint(event.pos):
                            self.change_level(level)
                            run = False
                            self.is_playing = True