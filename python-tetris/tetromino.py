"""
Tetromino pieces definitions and behavior for Python Tetris.
This module defines the seven standard Tetromino pieces and their rotations.
"""

# Constants for directions
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
MIN_DIR, MAX_DIR = 0, 3

class Tetromino:
    """
    Represents a Tetromino piece with its shape, color, and rotation states.
    Uses the same bit representation as the JavaScript version for consistency.
    """
    
    def __init__(self, size, blocks, color):
        """
        Initialize a new Tetromino piece.
        
        Args:
            size (int): The size of the piece (2, 3, or 4)
            blocks (list): List of 4 integers representing the 4 rotations of the piece
            color (str): The color of the piece
        """
        self.size = size
        self.blocks = blocks
        self.color = color
    
    def each_block(self, x, y, dir):
        """
        Iterate through each occupied block in the piece.
        
        Args:
            x (int): The x position of the piece
            y (int): The y position of the piece
            dir (int): The rotation direction (0-3)
            
        Returns:
            list: List of (x, y) coordinates for each block in the piece
        """
        result = []
        bit = 0x8000
        row = 0
        col = 0
        blocks = self.blocks[dir]
        
        while bit > 0:
            if blocks & bit:
                result.append((x + col, y + row))
            if col + 1 == 4:
                col = 0
                row += 1
            else:
                col += 1
            bit >>= 1
        
        return result

# Define the seven standard Tetromino pieces
# Using the same bit representation as the JavaScript version
I_PIECE = Tetromino(4, [0x0F00, 0x2222, 0x00F0, 0x4444], 'cyan')
J_PIECE = Tetromino(3, [0x44C0, 0x8E00, 0x6440, 0x0E20], 'blue')
L_PIECE = Tetromino(3, [0x4460, 0x0E80, 0xC440, 0x2E00], 'orange')
O_PIECE = Tetromino(2, [0xCC00, 0xCC00, 0xCC00, 0xCC00], 'yellow')
S_PIECE = Tetromino(3, [0x06C0, 0x8C40, 0x6C00, 0x4620], 'green')
T_PIECE = Tetromino(3, [0x0E40, 0x4C40, 0x4E00, 0x4640], 'purple')
Z_PIECE = Tetromino(3, [0x0C60, 0x4C80, 0xC600, 0x2640], 'red')

# List of all pieces for random selection
ALL_PIECES = [I_PIECE, J_PIECE, L_PIECE, O_PIECE, S_PIECE, T_PIECE, Z_PIECE]