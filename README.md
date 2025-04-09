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

- Python 3.x
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
   - Touches fléchées **haut/bas** : Ajuster l'angle du canon
   - Touches fléchées **gauche/droite** : Ajuster la puissance du tir
   - **Espace** : Tirer
   - **Échap** : Mettre le jeu en pause
   - **F** : Quitter la partie

## Structure des fichiers

- `main.py` : Point d'entrée principal du jeu
- `game.py` : Gestion des mécaniques de jeu et des menus
- `player.py` : Logique des joueurs et des canons
- `level.py` : Configuration des niveaux et de la physique
- `obstacle.py` : Gestion des obstacles
- `Boulet_Canon.py` : Comportement des projectiles

## Les niveaux

1. **Niveau terrestre** : Gravité élevée, muraille mobile
2. **Niveau spatial** : Gravité faible, météorite mobile
3. **Niveau aquatique** : Gravité très élevée, obstacle mobile sous-marin

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
├── Boulet_Canon.py          # Logique des projectiles
│
└── assets_game_PT/          # Ressources du jeu
    ├── background/          # Images de fond
    ├── button/              # Images des boutons
    ├── canon/               # Images des canons
    ├── logo/                # Logos du jeu
    ├── obstacles/           # Images des obstacles
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

Ce jeu a été développé en utilisant :
- Python et Pygame pour le moteur de jeu
- Assets graphiques et sonores provenant de sources diverses

## Dépannage

- **Le jeu est lent** : Essayez de réduire la résolution de votre écran ou de fermer d'autres applications
- **Les sons ne fonctionnent pas** : Vérifiez que les fichiers audio sont bien présents dans le dossier `assets_game_PT/sound/`
- **Problèmes d'affichage** : Assurez-vous que tous les fichiers d'images sont présents dans les dossiers appropriés

## Améliorations futures

- Ajout de pouvoirs spéciaux comme mentionné dans votre description (augmentation des dégâts, capacité de soin, altération du terrain)
- Système de high scores
- Mode solo contre l'IA
- Personnalisation des canons
- Effets visuels améliorés pour les explosions

---

Bon jeu et que le meilleur artilleur gagne !
