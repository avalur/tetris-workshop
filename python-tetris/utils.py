"""
Utility functions for Python Tetris.
This module provides functions for automated gameplay and performance testing.
"""

import time
import pygame
from heuristic_agent import select_best_move

class AutoPlayer:
    """
    Class for automatically playing Tetris using the AI agent.
    """
    
    def __init__(self, game, renderer=None, delay=0.01):
        """
        Initialize the auto player.
        
        Args:
            game (Game): The game object
            renderer (Renderer, optional): The renderer object for visualization
            delay (float): Delay between moves in seconds
        """
        self.game = game
        self.renderer = renderer
        self.delay = delay
        self.total_score = 0
        self.total_rows = 0
        self.games_played = 0
        
    def play_games(self, num_games=5, callback=None):
        """
        Automatically play multiple games and measure performance.
        
        Args:
            num_games (int): Number of games to play
            callback (function, optional): Callback function to be called with results
            
        Returns:
            dict: Performance results
        """
        self.total_score = 0
        self.total_rows = 0
        self.games_played = 0
        
        print(f"Starting auto play with {num_games} games...")
        
        for i in range(num_games):
            print(f"Starting game {i+1} of {num_games}...")
            self.play_single_game()
            print(f"Game {i+1} completed. Score: {self.game.score}, Rows: {self.game.rows}")
        
        # Calculate averages
        avg_score = self.total_score / num_games
        avg_rows = self.total_rows / num_games
        
        results = {
            'games': num_games,
            'total_score': self.total_score,
            'total_rows': self.total_rows,
            'avg_score': avg_score,
            'avg_rows': avg_rows
        }
        
        print(f"All {num_games} games completed.")
        print(f"Average Score: {avg_score:.2f}")
        print(f"Average Rows: {avg_rows:.2f}")
        
        if callback and callable(callback):
            callback(results)
            
        return results
    
    def play_single_game(self):
        """
        Play a single game automatically using the AI agent.
        
        Returns:
            tuple: (score, rows) - The final score and rows cleared
        """
        # Reset the game
        self.game.reset()
        
        # Play until game over
        while not self.game.game_over:
            # Make AI move
            self.make_ai_move()
            
            # Update game state
            self.game.update(self.delay)
            
            # Render if renderer is provided
            if self.renderer:
                self.renderer.draw(self.game)
                pygame.display.flip()
                
                # Process events to keep the window responsive
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return (self.game.score, self.game.rows)
            
            # Add a small delay
            time.sleep(self.delay)
        
        # Record results
        self.total_score += self.game.score
        self.total_rows += self.game.rows
        self.games_played += 1
        
        return (self.game.score, self.game.rows)
    
    def make_ai_move(self):
        """
        Make a single AI move.
        """
        # Get the best move
        best_move = select_best_move(self.game, self.game.current_piece, self.game.next_piece)
        
        if best_move:
            # Apply the move
            self.game.current_piece['x'] = best_move['x']
            self.game.current_piece['y'] = best_move['y']
            self.game.current_piece['dir'] = best_move['piece']['dir']
            self.game.drop()

def run_performance_test(game, renderer=None, num_games=5, callback=None):
    """
    Run a performance test with the current settings.
    
    Args:
        game (Game): The game object
        renderer (Renderer, optional): The renderer object for visualization
        num_games (int): Number of games to play
        callback (function, optional): Callback function to be called with results
        
    Returns:
        dict: Performance results
    """
    print(f"Starting performance test with {num_games} games...")
    
    auto_player = AutoPlayer(game, renderer)
    results = auto_player.play_games(num_games, callback)
    
    return results