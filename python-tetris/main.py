"""
Entry point for Python Tetris.
This module initializes the game, handles the game loop, and processes user input.
"""

import sys
import time
import pygame
from game import Game
from renderer import Renderer
from performance import PerformanceMonitor

# Constants
FPS = 60
AI_MODE = False  # Set to True to enable AI mode

def main():
    """Main entry point for the game."""
    # Initialize Pygame
    pygame.init()

    # Create game and renderer
    game = Game()
    renderer = Renderer()

    # Create performance monitor
    performance_monitor = PerformanceMonitor(10, 10, 120, 50, 16)

    # Set up the clock for controlling frame rate
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    last_time = time.time()

    while running:
        # Calculate delta time
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                handle_keydown(event.key, game)

        # Update game state
        game.update(dt)

        # Render the game
        renderer.draw(game)

        # Update and draw performance monitor
        performance_monitor.update()
        performance_monitor.draw(renderer.screen)

        # Cap the frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()

def handle_keydown(key, game):
    """
    Handle keyboard input.

    Args:
        key (int): The key that was pressed
        game (Game): The game object
    """
    if game.game_over:
        # If game is over, only respond to space to restart
        if key == pygame.K_SPACE:
            game.reset()
    elif game.paused:
        # If game is paused, only respond to P to unpause
        if key == pygame.K_p:
            game.toggle_pause()
    else:
        # Normal gameplay controls
        if key == pygame.K_LEFT:
            game.add_action(2)  # LEFT
        elif key == pygame.K_RIGHT:
            game.add_action(1)  # RIGHT
        elif key == pygame.K_UP:
            game.add_action(0)  # UP (rotate)
        elif key == pygame.K_DOWN:
            game.add_action(3)  # DOWN
        elif key == pygame.K_SPACE:
            # Hard drop - move down until collision
            while game.move(3):  # DOWN
                pass
            game.drop()
        elif key == pygame.K_p:
            game.toggle_pause()
        elif key == pygame.K_ESCAPE:
            game.game_over = True

if __name__ == "__main__":
    main()
