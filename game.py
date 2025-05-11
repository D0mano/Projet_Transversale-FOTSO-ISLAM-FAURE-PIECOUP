import sys
import pygame
from player import Player
from level import Level
from power import PowerManager


class Game:
    """
    Main Game class responsible for managing the game state, players, levels,
    and all associated game mechanics.
    """

    def __init__(self, level, ecran):
        """
        Initialize the game with a level and screen.

        Args:
            level: The Level object for the current game
            ecran: The pygame display surface (screen)
        """
        # Game state flags
        self.is_playing = False
        self.all_players = pygame.sprite.Group()
        self.screen = ecran

        # Create two players, one on each side of the screen
        self.player = [Player(self, level, self.screen.get_width() / 64, level.pos_y, 1),  # Player 1 (left)
                       Player(self, level, self.screen.get_width() / 1.067, level.pos_y, -1)]  # Player 2 (right)
        self.level = level
        self.power_manager = PowerManager(self)  # Manages power-ups

        # Add players to sprite group for easier management
        for player in self.player:
            self.all_players.add(player)

        # Additional game state flags
        self.is_paused = False
        self.running = True
        self.waiting = False
        self.in_menu = True

        self.current_player = 0  # Index of the player currently playing (0 for Player 1, 1 for Player 2)

        # Audio settings
        self.volume = 100
        if self.volume == 0:
            self.mute = True
        else:
            self.mute = False

        # Explosions sprite group
        self.all_explosion = pygame.sprite.Group()

        # Sound effects and music
        self.click_sound = pygame.mixer.Sound("assets_game_PT/sound/pop-sound-effect-197846.mp3")
        self.menu_music = "assets_game_PT/sound/cell_music.mp3"
        self.levels_music = ["assets_game_PT/sound/level1_music.mp3",
                             "assets_game_PT/sound/level2_music.mp3",
                             "assets_game_PT/sound/level3_music.mp3"]

    def play_music(self, music_name):
        """
        Play a music track in a loop.

        Args:
            music_name: Path to the music file
        """
        pygame.mixer.music.load(music_name)
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def stop_music(self):
        """Stop the currently playing music."""
        pygame.mixer.music.stop()

    def music_is_playing(self):
        """
        Check if music is currently playing.

        Returns:
            bool: True if music is playing, False otherwise
        """
        return pygame.mixer.music.get_busy()

    def start(self, dt):
        """
        Main game loop function - handles rendering and game updates.

        Args:
            dt: Delta time (time since last frame) for physics calculations
        """
        self.in_menu = False
        # Render the level
        self.level.load_level()

        # Render player cannons and bases
        self.screen.blit(self.player[0].pied_canon, (self.player[0].rect_pied.x, self.player[0].rect_pied.y))
        self.screen.blit(self.player[1].pied_canon, (self.player[1].rect_pied.x, self.player[1].rect_pied.y))
        self.screen.blit(self.player[0].canon, self.player[0].rect.topleft)
        self.screen.blit(self.player[1].canon, self.player[1].rect.topleft)

        # Display the current player's projected trajectory
        self.player[self.current_player].draw_trajectory(self.screen)


        # Display shooting information for the current player
        """
        self.screen.blit(self.player[self.current_player].show_info()[0],
                         (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50,
                          650))
        self.screen.blit(self.player[self.current_player].show_info()[1],
                         (self.player[self.current_player].rect.x + self.player[self.current_player].direction * 50,
                          600))
        """

        # Update and draw power-ups
        self.power_manager.update()
        self.power_manager.draw(self.screen)

        # Update and draw explosions
        self.all_explosion.update()
        self.all_explosion.draw(self.screen)

        # Update projectile positions for all players
        for players in self.player:
            for projectile in players.all_projectile:
                projectile.move(dt)

        # Draw projectiles and health bars for all players
        for players in self.player:
            players.all_projectile.draw(self.screen)
            players.update_health_bar(self.screen)

        # Update the display
        pygame.display.flip()

        # Handle input events
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                # Handle window resize
                self.level.load_level()
                self.level.image = pygame.transform.scale(self.level.true_image,
                                                          (self.screen.get_width(), self.screen.get_height()))
                for players in self.player:
                    players.cal_pos()
                self.level.obstacle.cal_pos_obs()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.QUIT:
                    self.running = False
                if event.key == pygame.K_f:
                    # Force return to menu
                    self.in_menu = True
                    self.game_over()
                if event.key == pygame.K_ESCAPE:
                    # Open pause menu
                    self.is_paused = True
                    self.pause_menu()

                if event.key == pygame.K_SPACE:
                    # Fire cannon and switch turns
                    self.player[self.current_player].fire()
                    self.switch_turn()

                # Player 1 controls (left player)
                if self.current_player == 0:
                    if event.key == pygame.K_d:
                        self.player[self.current_player].power_up()
                    elif event.key == pygame.K_q:
                        self.player[self.current_player].power_down()
                    elif event.key == pygame.K_z:
                        self.player[self.current_player].aim_up()
                    elif event.key == pygame.K_s:
                        self.player[self.current_player].aim_down()
                # Player 2 controls (right player)
                else:
                    if event.key == pygame.K_LEFT:
                        self.player[self.current_player].power_up()
                    elif event.key == pygame.K_RIGHT:
                        self.player[self.current_player].power_down()
                    elif event.key == pygame.K_UP:
                        self.player[self.current_player].aim_up()
                    elif event.key == pygame.K_DOWN:
                        self.player[self.current_player].aim_down()

    def game_over(self):
        """
        Reset the game state when returning to menu or game over.
        Restores player health, resets positions, and clears power-ups.
        """
        # Reset player health and position
        for player in self.player:
            player.health = player.max_health
            player.reinitialize_canon()
            player.cal_pos()

        # Remove all power-ups
        for powers in self.power_manager.all_powers:
            powers.kill()

        # Stop music, reset game state
        self.stop_music()
        self.current_player = 0
        self.is_playing = False
        self.in_menu = True

        # Reset player alive status
        for player in self.all_players:
            player.alive = True

    def menu(self):
        """
        Display and handle the main menu interface.
        """
        # Start menu music if not already playing
        if not self.music_is_playing():
            self.play_music(self.menu_music)

        # Load menu assets
        background = pygame.image.load("assets_game_PT/background/Background_menu.png").convert_alpha()
        background_resize = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))

        # Game logo
        banner = pygame.image.load("assets_game_PT/logo/CANON_MASTER_Logo-removebg-preview.png").convert_alpha()
        banner_resize = pygame.transform.scale(banner,
                                               (self.screen.get_width() / 2.56, self.screen.get_height() / 1.44))
        banner_rect = banner_resize.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 4))

        # Play button assets (normal and hover states)
        play_button_white = pygame.image.load("assets_game_PT/button/play_button_white.png").convert_alpha()
        play_button_white_resize = pygame.transform.scale(play_button_white, (
        self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
        play_button_green = pygame.image.load("assets_game_PT/button/play_button_green.png").convert_alpha()
        play_button_green_resize = pygame.transform.scale(play_button_green, (
        self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
        play_button_rect = play_button_white_resize.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

        # Quit button assets (normal and hover states)
        quit_button_white = pygame.image.load("assets_game_PT/button/quit_button_white.png").convert_alpha()
        quit_button_white_resize = pygame.transform.scale(quit_button_white, (
        self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
        quit_button_red = pygame.image.load("assets_game_PT/button/quit_button_red.png").convert_alpha()
        quit_button_red_resize = pygame.transform.scale(quit_button_red, (
        self.screen.get_width() / 4.26, self.screen.get_height() / 3.6))
        quit_button_rect = quit_button_white_resize.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 1.3))

        play_button = play_button_white_resize
        quit_button = quit_button_white_resize

        # Main menu loop
        while self.running and not self.is_playing:
            # Draw menu elements
            self.screen.blit(background_resize, (0, 0))
            self.screen.blit(banner_resize, banner_rect)
            self.screen.blit(play_button, play_button_rect)
            self.screen.blit(quit_button, quit_button_rect)

            # Handle input events for quitting and menu interaction
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    # Resize elements on window resize
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
                    # Handle button hover effects
                    if play_button_rect.collidepoint(event.pos):
                        play_button = play_button_green_resize
                    else:
                        play_button = play_button_white_resize
                    if quit_button_rect.collidepoint(event.pos):
                        quit_button = quit_button_red_resize
                    else:
                        quit_button = quit_button_white_resize

                elif event.type == pygame.MOUSEBUTTONUP:
                    # Handle button clicks
                    self.click_sound.play()
                    if play_button_rect.collidepoint(event.pos):
                        self.level_menu()  # Open level selection menu
                        self.in_menu = False
                    elif quit_button_rect.collidepoint(event.pos):
                        self.stop_music()
                        self.running = False  # Exit game

            pygame.display.flip()  # Update the display

    def pause_menu(self):
        """
        Display and handle the pause menu interface.
        """
        # Create semi-transparent overlay
        pause_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        pause_overlay.fill((0, 0, 0, 180))  # Black with transparency
        self.screen.blit(pause_overlay, (0, 0))
        backgrounds_copy = self.screen.copy()

        # Load button images
        resume_button_white = pygame.image.load(
            "assets_game_PT/button/RESUME_button_white-removebg-preview.png").convert_alpha()
        options_button_white = pygame.image.load(
            "assets_game_PT/button/OPTION_button_white-removebg-preview.png").convert_alpha()
        quit_button_white = pygame.image.load(
            "assets_game_PT/button/QUIT_button_white2-removebg-preview.png").convert_alpha()

        resume_button_gray = pygame.image.load(
            "assets_game_PT/button/RESUME_button_gray-removebg-preview.png").convert_alpha()
        options_button_gray = pygame.image.load(
            "assets_game_PT/button/OPTION_button_gray-removebg-preview.png").convert_alpha()
        quit_button_gray = pygame.image.load(
            "assets_game_PT/button/QUIT_button_gray-removebg-preview.png").convert_alpha()

        # Position the buttons
        resume_rect = resume_button_white.get_rect(center=(self.screen.get_width() // 2, self.screen.get_width() / 6.4))
        options_rect = options_button_white.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_width() / 3.6))
        quit_rect = quit_button_white.get_rect(center=(self.screen.get_width() // 2, self.screen.get_width() / 2.56))

        resume_button = resume_button_white
        options_button = options_button_white
        quit_button = quit_button_white

        # Pause menu loop
        while self.is_paused:
            self.screen.blit(backgrounds_copy, (0, 0))
            self.screen.blit(resume_button, resume_rect)
            self.screen.blit(options_button, options_rect)
            self.screen.blit(quit_button, quit_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

                elif event.type == pygame.MOUSEMOTION:
                    # Handle button hover effects
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
                    # Handle button clicks
                    self.click_sound.play()
                    if resume_rect.collidepoint(event.pos):
                        self.is_paused = False  # Resume the game
                    elif quit_rect.collidepoint(event.pos):
                        self.game_over()  # Return to main menu
                        self.stop_music()
                        self.play_music(self.menu_music)
                        self.in_menu = True
                        self.is_paused = False
                    elif options_rect.collidepoint(event.pos):
                        self.waiting = True
                        self.options_menu()  # Open options menu

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = False  # Resume game with Escape key

            pygame.display.flip()

    def options_menu(self):
        """
        Display and handle the options menu interface.
        Allows changing volume and level selection.
        """
        # Create background copy and overlay
        backgrounds_copy = self.screen.copy()
        options_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        options_overlay.fill((50, 50, 50, 200))  # Semi-transparent background
        self.screen.blit(options_overlay, (0, 0))
        options_overlay_copy = self.screen.copy()

        # Create header text
        font = pygame.font.Font(None, 50)
        text = font.render("Options Menu - Press ESC to go back", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.screen.get_width() / 3, self.screen.get_height() / 3.6))

        # Load option button images
        volume = pygame.image.load("assets_game_PT/button/volume.png").convert_alpha()
        volume = pygame.transform.scale(volume, (100, 100))
        mute = pygame.image.load("assets_game_PT/button/mute.png").convert_alpha()
        mute = pygame.transform.scale(mute, (100, 100))
        level_select = pygame.image.load("assets_game_PT/button/Selecteur_level.png")
        level_select = pygame.transform.scale(level_select, (100, 100))

        # Position the buttons
        volume_rect = volume.get_rect(center=(self.screen.get_width() / 8.5, self.screen.get_height() / 2.05))
        mute_rect = volume_rect
        level_select_rect = level_select.get_rect(
            center=(self.screen.get_width() / 8.5, self.screen.get_height() / 1.2))

        # Set initial volume button state
        if self.mute == False:
            volume_button = volume
        else:
            volume_button = mute

        pygame.display.flip()

        # Options menu loop
        while self.waiting:
            self.screen.blit(options_overlay_copy, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(volume_button, volume_rect)
            self.screen.blit(level_select, level_select_rect)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    # Handle button clicks
                    self.click_sound.play()
                    if volume_button == volume and volume_rect.collidepoint(event.pos) and not (self.mute):
                        # Toggle mute
                        self.stop_music()
                        volume_button = mute
                        self.mute = True
                    else:
                        # Unmute and play level music
                        self.play_music(self.levels_music[self.level.lv_number - 1])
                        volume_button = volume
                        self.mute = False
                    if level_select_rect.collidepoint(event.pos):
                        # Return to level selection
                        self.stop_music()
                        self.play_music(self.menu_music)
                        self.waiting = False
                        self.is_paused = False
                        self.is_playing = False
                        self.level_menu()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.waiting = False

        # Restore background if returning to pause menu
        if self.is_paused:
            self.screen.blit(backgrounds_copy, (0, 0))
            pygame.display.flip()

    def switch_turn(self):
        """
        Switch the active player (toggle between 0 and 1).
        """
        self.current_player = 1 - self.current_player

    def check_collision(self, sprite, group):
        """
        Check if a sprite collides with any sprite in a group.

        Args:
            sprite: The sprite to check collisions for
            group: The sprite group to check collisions against

        Returns:
            List of collided sprites or empty list
        """
        return pygame.sprite.spritecollide(sprite, group, False)

    def change_level(self, new_level):
        """
        Change the current game level.

        Args:
            new_level: The new Level object to switch to
        """
        self.level = new_level
        # Play the music for the new level
        self.play_music(self.levels_music[self.level.lv_number - 1])

        # Recreate players for the new level
        self.player = [Player(self, self.level, self.screen.get_width() / 64, self.level.pos_y, 1),
                       Player(self, self.level, self.screen.get_width() / 1.067, self.level.pos_y, -1)]
        self.all_players = pygame.sprite.Group()

        # Add players to the sprite group and reset turn
        for player in self.player:
            self.all_players.add(player)
            self.current_player = 0

        # Remove all power-ups
        for powers in self.power_manager.all_powers:
            powers.kill()

    def level_menu(self):
        """
        Display and handle the level selection menu interface.
        """
        self.in_menu = False
        # Start menu music if not already playing
        if not self.music_is_playing():
            self.play_music(self.menu_music)

        # Load menu assets
        background = pygame.image.load("assets_game_PT/background/Background_menu.png").convert_alpha()
        background_resize = pygame.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))

        # Load title image
        titre = pygame.image.load("assets_game_PT/logo/MASTER_horozontal (2).png").convert_alpha()
        titre_resize = pygame.transform.scale(titre, (self.screen.get_width() / 2.56, self.screen.get_height() / 2.4))
        titre_rect = titre_resize.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 6))

        # Create overlay rectangle for level options
        level_overlay_rect = (
        self.screen.get_width() / 3, self.screen.get_height() / 4.5, self.screen.get_width() / 3.1,
        self.screen.get_height() / 1.44)

        # Create Level instances for each available level
        levels = [Level(self.screen, 1),
                  Level(self.screen, 2),
                  Level(self.screen, 3)]

        # Create level selection buttons
        font = pygame.font.Font(None, 50)
        buttons = []
        for i, level in enumerate(levels):
            text = font.render(f"Level {i + 1}", True, (255, 255, 255))
            rect = text.get_rect(center=(
            self.screen.get_width() / 2, self.screen.get_height() / 3.6 + i * self.screen.get_height() / 7.2))
            buttons.append((text, rect, level))

        # Draw menu elements
        self.screen.blit(background_resize, (0, 0))
        pygame.draw.rect(self.screen, (50, 30, 30), level_overlay_rect, border_radius=20)
        self.screen.blit(titre_resize, titre_rect)
        for text, rect, _ in buttons:
            self.screen.blit(text, rect)
            pygame.display.flip()

        pygame.display.flip()

        # Level selection menu loop
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    background_resize = pygame.transform.scale(background,
                                                               (self.screen.get_width(), self.screen.get_height()))
                    pygame.display.flip()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Return to main menu
                        run = False
                        self.in_menu = True

                if event.type == pygame.MOUSEBUTTONUP:
                    # Handle level selection
                    self.click_sound.play()
                    for _, rect, level in buttons:
                        if rect.collidepoint(event.pos):
                            self.stop_music()
                            self.change_level(level)
                            run = False
                            self.is_playing = True

    def end_game(self):
        """
        Display the end game screen showing which player won.
        Provides options to replay or select a different level.
        """
        # Stop music and play victory sound
        self.stop_music()
        pygame.mixer.Sound("assets_game_PT/sound/Happy Wheels victory green screen.mp3").play()

        # Load winning player images
        P1_win = pygame.image.load("assets_game_PT/background/P1_win.png")
        P2_win = pygame.image.load("assets_game_PT/background/P2_win.png")

        # Determine which player won
        for player in self.all_players:
            if player.direction == 1:  # Player 1
                if not player.alive:
                    pancarte = P2_win  # If Player 1 is dead, Player 2 wins
            if player.direction == -1:  # Player 2
                if not player.alive:
                    pancarte = P1_win  # If Player 2 is dead, Player 1 wins

        # Set up victory image
        pancarte.set_colorkey((126, 217, 87))
        pancarte.convert_alpha()
        pancarte_rect = pancarte.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height() / 2))

        # Load button images
        lv_select = pygame.image.load("assets_game_PT/button/Selecteur_level.png").convert_alpha()
        lv_select = pygame.transform.scale(lv_select, (90, 90))
        lv_select_rect = lv_select.get_rect(center=(self.screen.get_width() / 2.4, self.screen.get_height() / 1.7))

        replay_button = pygame.image.load("assets_game_PT/button/Replay_button-removebg-preview.png")
        replay_button = pygame.transform.scale(replay_button, (90, 90))
        replay_button.set_colorkey((0, 0, 0))
        replay_button_rect = replay_button.get_rect(
            center=(self.screen.get_width() / 1.7, self.screen.get_height() / 1.7))


        # End game screen loop
        end = True
        while end:
            self.screen.blit(pancarte, pancarte_rect)
            self.screen.blit(lv_select, lv_select_rect)
            self.screen.blit(replay_button, replay_button_rect)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.click_sound.play()
                    if replay_button_rect.collidepoint(event.pos):
                        # Replay same level
                        end = False
                        self.game_over()
                        self.change_level(self.level)
                        self.in_menu = False
                        self.is_playing = True
                    if lv_select_rect.collidepoint(event.pos):
                        # Go to level selection
                        end = False
                        self.game_over()
                        self.level_menu()

            pygame.display.flip()