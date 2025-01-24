Pygame RPG Game

This project is a turn-based RPG game built using Pygame, structured following an Object-Oriented Programming (OOP) approach intially by the youtuber ShawCode and his rpg game tutorial series(https://www.youtube.com/watch?v=crUF36OkGDw&list=PLkkm3wcQHjT7gn81Wn-e78cAyhwBW3FIc). The game has been expanded with additional features, including a dynamic battle screen inspired by Pokémon-style combat with moves, health bars, and battle logic.

Features

1. Overworld Gameplay

The player navigates a tile-based map, interacting with the environment and encountering enemies.

Enemies are placed dynamically using a tilemap system.

Sprite management is handled using Pygame’s sprite groups for easy rendering and updates.

2. Dynamic Battle System

When the player collides with an enemy, the game transitions to a separate battle screen.

The battle screen features:

A Pokémon-style turn-based combat system.

Moves with varying effects and damage values.

Health bars for both the player and the enemy that dynamically update during the battle.

A "Run" feature to escape the battle and return to the overworld.

Logic for experience points (XP) and leveling up after defeating an enemy.

3. Object-Oriented Programming (OOP) Structure

Classes are used extensively to manage the game's logic and behavior:

Game: Handles the overall game loop and state transitions.

Character: Represents the player with attributes like health, moves, XP, and leveling logic.

Enemy: Represents enemies with unique moves and stats.

HealthBar: Dynamically updates and displays health or XP bars.

UI: Manages the battle screen's buttons and logs.

Sprites: Handles tile-based elements like blocks, ground, and other sprites.

4. Expanded Tilemap System

The game world and battle screens are generated using a tilemap represented as a 2D array.
5. State Management

The game uses a state variable to manage transitions between the overworld and battle screens.

Supported states:

normal: The main overworld.

battle: The battle screen.

game_over: The game over screen.
Battle Screen

Click buttons to select moves or run away.

Moves deal varying amounts of damage.

The health bars for both the player and the enemy update dynamically.

Running away returns the player to the overworld.
