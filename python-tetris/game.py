"""
Core game logic for Python Tetris.
This module handles the game board, piece movement, collision detection, and scoring.
"""

import random
import time
from tetromino import ALL_PIECES, UP, RIGHT, DOWN, LEFT, MIN_DIR, MAX_DIR

class Game:
    """
    Main game class that handles the Tetris game logic.
    """
    
    def __init__(self, width=10, height=20):
        """
        Initialize a new Tetris game.
        
        Args:
            width (int): Width of the game board in blocks
            height (int): Height of the game board in blocks
        """
        self.width = width
        self.height = height
        self.reset()
        
    def reset(self):
        """Reset the game to its initial state."""
        self.board = self._initialize_board(self.width, self.height)
        self.score = 0
        self.visual_score = 0
        self.rows = 0
        self.game_over = False
        self.paused = False
        self.actions = []
        self.speed = 0.6  # Initial speed (seconds per drop)
        self.speed_decrement = 0.005  # How much to decrease speed per level
        self.min_speed = 0.1  # Minimum speed
        self.last_time = time.time()
        self.dt = 0  # Delta time
        
        # Initialize pieces
        self.pieces = list(ALL_PIECES) * 4  # 4 of each piece
        random.shuffle(self.pieces)
        
        # Set up current and next piece
        self.next_piece = self._random_piece()
        self.current_piece = self._random_piece()
        
    def _initialize_board(self, width, height):
        """
        Initialize an empty game board.
        
        Args:
            width (int): Width of the board
            height (int): Height of the board
            
        Returns:
            list: 2D list representing the game board
        """
        return [[0 for y in range(height)] for x in range(width)]
    
    def _random_piece(self):
        """
        Get a random piece from the bag.
        If the bag is empty, refill it with 4 of each piece.
        
        Returns:
            dict: A dictionary with piece type, position, and rotation
        """
        if not self.pieces:
            self.pieces = list(ALL_PIECES) * 4
            random.shuffle(self.pieces)
            
        piece_type = self.pieces.pop()
        x = random.randint(0, self.width - piece_type.size)
        
        return {
            'type': piece_type,
            'x': x,
            'y': 0,
            'dir': UP
        }
    
    def is_occupied(self, piece, x, y, dir):
        """
        Check if a piece can fit at the given position.
        
        Args:
            piece (Tetromino): The piece to check
            x (int): X position
            y (int): Y position
            dir (int): Rotation direction
            
        Returns:
            bool: True if the position is occupied, False otherwise
        """
        for block_x, block_y in piece.each_block(x, y, dir):
            if (block_x < 0 or block_x >= self.width or 
                block_y < 0 or block_y >= self.height or 
                self.board[block_x][block_y]):
                return True
        return False
    
    def move(self, direction):
        """
        Move the current piece in the given direction.
        
        Args:
            direction (int): Direction to move (LEFT, RIGHT, DOWN)
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        x, y = self.current_piece['x'], self.current_piece['y']
        
        if direction == LEFT:
            x -= 1
        elif direction == RIGHT:
            x += 1
        elif direction == DOWN:
            y += 1
            
        if not self.is_occupied(self.current_piece['type'], x, y, self.current_piece['dir']):
            self.current_piece['x'] = x
            self.current_piece['y'] = y
            return True
        return False
    
    def rotate(self):
        """
        Rotate the current piece clockwise.
        
        Returns:
            bool: True if the rotation was successful, False otherwise
        """
        new_dir = (self.current_piece['dir'] + 1) % 4
        
        if not self.is_occupied(self.current_piece['type'], 
                               self.current_piece['x'], 
                               self.current_piece['y'], 
                               new_dir):
            self.current_piece['dir'] = new_dir
            return True
        return False
    
    def drop(self):
        """
        Drop the current piece as far as it can go.
        If it can't move down anymore, place it on the board and get a new piece.
        
        Returns:
            bool: True if game continues, False if game over
        """
        if not self.move(DOWN):
            self.add_score(10)  # Points for dropping a piece
            self._drop_piece()
            self._remove_lines()
            self.current_piece = self.next_piece
            self.next_piece = self._random_piece()
            self.actions = []  # Clear pending actions
            
            # Check if the new piece can fit
            if self.is_occupied(self.current_piece['type'], 
                               self.current_piece['x'], 
                               self.current_piece['y'], 
                               self.current_piece['dir']):
                self.game_over = True
                return False
        return True
    
    def _drop_piece(self):
        """Place the current piece on the board."""
        for x, y in self.current_piece['type'].each_block(
            self.current_piece['x'], 
            self.current_piece['y'], 
            self.current_piece['dir']):
            self.board[x][y] = self.current_piece['type']
    
    def _remove_lines(self):
        """
        Remove completed lines and add to score.
        The more lines cleared at once, the higher the score.
        """
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            complete = True
            for x in range(self.width):
                if not self.board[x][y]:
                    complete = False
                    break
                    
            if complete:
                self._remove_line(y)
                lines_cleared += 1
            else:
                y -= 1
                
        if lines_cleared > 0:
            self.add_rows(lines_cleared)
            # Score increases exponentially with more lines
            self.add_score(100 * (2 ** (lines_cleared - 1)))
    
    def _remove_line(self, n):
        """
        Remove a completed line and shift all lines above it down.
        
        Args:
            n (int): The line number to remove
        """
        for y in range(n, 0, -1):
            for x in range(self.width):
                self.board[x][y] = self.board[x][y-1]
                
        # Clear the top line
        for x in range(self.width):
            self.board[x][0] = 0
    
    def add_score(self, points):
        """
        Add points to the score.
        
        Args:
            points (int): Points to add
        """
        self.score += points
    
    def add_rows(self, rows):
        """
        Add to the row count and increase speed.
        
        Args:
            rows (int): Number of rows to add
        """
        self.rows += rows
        # Increase speed as rows are cleared
        self.speed = max(self.min_speed, 0.6 - (self.speed_decrement * self.rows))
    
    def update(self, dt):
        """
        Update the game state.
        
        Args:
            dt (float): Time elapsed since last update
            
        Returns:
            bool: True if game continues, False if game over
        """
        if self.game_over or self.paused:
            return False
            
        # Update visual score (for animation)
        if self.visual_score < self.score:
            self.visual_score += 1
            
        # Handle pending actions
        if self.actions:
            action = self.actions.pop(0)
            self.handle_action(action)
            
        # Update time and check if piece should drop
        self.dt += dt
        if self.dt > self.speed:
            self.dt -= self.speed
            self.drop()
            
        return not self.game_over
    
    def handle_action(self, action):
        """
        Handle a game action.
        
        Args:
            action (int): The action to handle (LEFT, RIGHT, UP, DOWN)
        """
        if action == LEFT:
            self.move(LEFT)
        elif action == RIGHT:
            self.move(RIGHT)
        elif action == UP:
            self.rotate()
        elif action == DOWN:
            self.drop()
    
    def add_action(self, action):
        """
        Add an action to the queue.
        
        Args:
            action (int): The action to add
        """
        self.actions.append(action)
    
    def toggle_pause(self):
        """Toggle the game's paused state."""
        self.paused = not self.paused
    
    def get_board_with_piece(self):
        """
        Get a representation of the board with the current piece.
        Useful for rendering.
        
        Returns:
            list: 2D list representing the board with the current piece
        """
        # Create a copy of the board
        board_copy = [row[:] for row in self.board]
        
        # Add the current piece
        if not self.game_over:
            for x, y in self.current_piece['type'].each_block(
                self.current_piece['x'], 
                self.current_piece['y'], 
                self.current_piece['dir']):
                if 0 <= x < self.width and 0 <= y < self.height:
                    board_copy[x][y] = self.current_piece['type']
                    
        return board_copy