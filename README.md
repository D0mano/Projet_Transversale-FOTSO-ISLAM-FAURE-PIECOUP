# CanonMaster - README

## Aperçu du jeu

CanonMaster est un jeu d'artillerie en tour par tour où deux joueurs s'affrontent en duel de canons. Le but est simple : ajustez l'angle et la puissance de vos tirs pour atteindre votre adversaire tout en évitant les obstacles en mouvement. Le jeu propose trois niveaux différents, chacun avec sa propre gravité et environnement.

## Fonctionnalités

- **Gameplay en tour par tour** : Les joueurs tirent à tour de rôle
- **Trois niveaux distincts** : Chaque niveau possède une gravité différente et des obstacles uniques
- **Simulation physique réaliste** : La trajectoire des projectiles est influencée par la gravité et les collisions
- **Mode multijoueur local** : Deux joueurs s'affrontent sur le même écran
- **Interface intuitive** : Paramètres de tir faciles à ajuster
- **Système de santé** : Chaque joueur dispose d'une barre de vie qui diminue lorsqu'il est touché

## Installation

### Prérequis

- Python 3.12
- Pygame

### Installation des dépendances

```bash
pip install pygame
```

### Lancement du jeu

```bash
python main.py
```

## Comment jouer

1. **Menu principal** : Au lancement du jeu, cliquez sur "Play" pour commencer
2. **Sélection du niveau** : Choisissez parmi les trois niveaux disponibles
3. **Contrôles pendant le jeu** :
   - Pour le joueur 1 Touches fléchées **haut/bas** :Ajuster l'angle du canon
   - Pour le joueur 2 Touches **Z/S**: Ajuster l'angle du canon
   - Pour le joueur 1 Touches fléchées **gauche/droite** : Ajuster la puissance du tir
   - Pour le joueur 2 Touches **Q/D**  : Ajuster la puissance du tir
   - **Espace** : Tirer
   - **Échap** : Mettre le jeu en pause
   - **F** : Quitter la partie

## Structure des fichiers

- `main.py` : Point d'entrée principal du jeu
- `game.py` : Gestion des mécaniques de jeu et des menus
- `player.py` : Logique des joueurs et des canons
- `level.py` : Configuration des niveaux et de la physique
- `obstacle.py` : Gestion des obstacles
- `boulet_canon.py` : Comportement des projectiles
- `power.py` : Gestion des différents pouvoirs
- `anime_power.py` : Gestion des animations des pouvoirs

## Les niveaux

1. **Niveau terrestre** : Gravité Normal, muraille mobile
2. **Niveau spatial** : Gravité faible, météorite mobile
3. **Niveau aquatique** : Gravité très élevée, caurails sous-marin

## Fonctionnement du jeu

### Système de tour

Le jeu fonctionne en tour par tour. Après avoir ajusté l'angle et la puissance, le joueur tire et le tour passe à son adversaire.

### Physique des projectiles

La trajectoire des projectiles est calculée en prenant en compte :
- La gravité spécifique à chaque niveau
- L'angle de tir
- La puissance du tir
- Les obstacles en mouvement

### Conditions de victoire

La partie se termine lorsque l'un des joueurs n'a plus de points de vie. Le canon est alors détruit et le joueur adverse est déclaré vainqueur.

## Menu pause et options

Pendant le jeu, vous pouvez appuyer sur **Échap** pour ouvrir le menu pause, qui offre les options suivantes :
- **Resume** : Reprendre la partie
- **Options** : Accéder aux paramètres (volume, sélection de niveau)
- **Quit** : Quitter la partie et retourner au menu principal

## Structure du projet

```
CanonMaster/
│
├── main.py                  # Point d'entrée du jeu
├── game.py                  # Logique du jeu et menus
├── player.py                # Gestion des joueurs
├── level.py                 # Configuration des niveaux
├── obstacle.py              # Gestion des obstacles
├── boulet_canon.py          # Logique des projectiles
├── power.py                 # Gestion des pouvoirs
├── anim_powers.py           # Gestion des animations des pouvoirs
│
└── assets_game_PT/          # Ressources du jeu
    ├── animations/          # Images de fond
    │     └── explosion_nuke/  # Contions les sprites de l'animation d'explosion
    ├── background/          # Images de fond
    ├── button/              # Images des boutons
    ├── canon/               # Images des canons
    ├── logo/                # Logos du jeu
    ├── obstacles/           # Images des obstacles
    ├── power_images/        # Images des superpouvoirs
    └── sound/               # Effets sonores
```

## Développement

### Ajout de nouveaux niveaux

Pour ajouter un nouveau niveau, modifiez le fichier `level.py` :
1. Ajoutez l'image de fond dans le tableau `self.background`
2. Définissez les propriétés spécifiques au niveau (gravité, position Y, etc.)
3. Configurez les obstacles appropriés

### Ajout de nouveaux obstacles

Pour créer un nouvel obstacle, modifiez le fichier `obstacle.py` :
1. Ajoutez l'image dans le tableau `self.type_obstacle`
2. Définissez son comportement dans la méthode `move_obstacle()`

## Crédits

Ce jeu a été développé par :
- FOTSO Nolann
- ISLAM Rafael
- PIECOUP Tom
- FAURE Mathieu

En utilisant :   
- Python et Pygame pour le moteur de jeu
- Assets graphiques et sonores provenant de sources diverses

## Dépannage

- **Le jeu est lent** : Essayez de réduire la résolution de votre écran ou de fermer d'autres applications
- **Les sons ne fonctionnent pas** : Vérifiez que les fichiers audio sont bien présents dans le dossier `assets_game_PT/sound/`
- **Problèmes d'affichage** : Assurez-vous que tous les fichiers d'images sont présents dans les dossiers appropriés

---

Bon jeu et que le meilleur artilleur gagne !

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