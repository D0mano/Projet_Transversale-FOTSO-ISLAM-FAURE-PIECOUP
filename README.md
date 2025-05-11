# CanonMaster - README

## Game Overview

CanonMaster is a turn-based artillery game where two players face off in a cannon duel. The goal is simple: adjust the angle and power of your shots to hit your opponent while avoiding moving obstacles. The game offers three different levels, each with its own gravity and environment.

## Features

- **Turn-based gameplay**: Players take turns firing
- **Three distinct levels**: Each level has different gravity and unique obstacles
- **Realistic physics simulation**: Projectile trajectory is influenced by gravity and collisions
- **Local multiplayer mode**: Two players compete on the same screen
- **Intuitive interface**: Easy-to-adjust firing parameters
- **Health system**: Each player has a life bar that decreases when hit

## Installation

### Prerequisites

- Python 3.12
- Pygame

### Installing Dependencies

```bash
pip install pygame
```

### Launching the Game

```bash
python main.py
```

## How to Play

1. **Main menu**: At game launch, click "Play" to start
2. **Level selection**: Choose from the three available levels
3. **In-game controls**:
   - **Up/down** arrow keys: Adjust the cannon angle
   - **Left/right** arrow keys: Adjust the firing power
   - **Space**: Fire
   - **Esc**: Pause the game
   - **F**: Quit the game

## File Structure

- `main.py`: Main entry point of the game
- `game.py`: Game mechanics and menu management
- `player.py`: Player and cannon logic
- `level.py`: Level configuration and physics
- `obstacle.py`: Obstacle management
- `boulet_canon.py`: Projectile behavior
- `power.py`: Power-up management
- `anim_power`: Power-up animations managements

## The Levels

1. **Earth level**: High gravity, mobile wall
2. **Space level**: Low gravity, mobile meteorite
3. **Underwater level**: Very high gravity, mobile underwater obstacle

## Game Mechanics

### Turn System

The game works in turns. After adjusting the angle and power, the player fires and the turn passes to their opponent.

### Projectile Physics

The trajectory of projectiles is calculated taking into account:
- The gravity specific to each level
- The firing angle
- The firing power
- Moving obstacles

### Victory Conditions

The game ends when one of the players has no more health points. The cannon is then destroyed and the opposing player is declared the winner.

## Pause Menu and Options

During the game, you can press **Esc** to open the pause menu, which offers the following options:
- **Resume**: Continue the game
- **Options**: Access settings (volume, level selection)
- **Quit**: Exit the game and return to the main menu

## Project Structure

```
CanonMaster/
│
├── main.py                  # Game entry point
├── game.py                  # Game logic and menus
├── player.py                # Player management
├── level.py                 # Level configuration
├── obstacle.py              # Obstacle management
├── boulet_canon.py          # Projectile logic
├── power.py                 # Power-up management
│
└── assets_game_PT/          # Ressources du jeu
    ├── animations/          # Power-up animations managements
    │   └── explosion_nuke/  # Explosion frames 
    ├── background/          # Background images
    ├── button/              # Button images
    ├── canon/               # Cannon images
    ├── logo/                # Game logos
    ├── obstacles/           # Obstacle images
    ├── power_images/        # Power-up images
    └── sound/               # Sound effects
```

## Development

### Adding New Levels

To add a new level, modify the `level.py` file:
1. Add the background image to the `self.background` array
2. Define the level-specific properties (gravity, Y position, etc.)
3. Configure the appropriate obstacles

### Adding New Obstacles

To create a new obstacle, modify the `obstacle.py` file:
1. Add the image to the `self.type_obstacle` array
2. Define its behavior in the `move_obstacle()` method

## Credits

This game was developed by:
- FOTSO Nolann
- ISLAM Rafael
- PIECOUP Tom
- FAURE Mathieu

Using:
- Python and Pygame for the game engine
- Graphic and sound assets from various sources

## Troubleshooting

- **The game is slow**: Try reducing your screen resolution or closing other applications
- **Sounds don't work**: Check that the audio files are present in the `assets_game_PT/sound/` folder
- **Display problems**: Make sure all image files are present in the appropriate folders


---

Have fun and may the best artilleryman win!