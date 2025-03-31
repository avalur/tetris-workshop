"""
Pygame rendering logic for Python Tetris.
This module handles drawing the game board, pieces, and UI elements.
"""

import pygame

class Renderer:
    """
    Handles rendering the Tetris game using Pygame.
    """
    
    def __init__(self, width=800, height=600, block_size=30):
        """
        Initialize the renderer.
        
        Args:
            width (int): Width of the window in pixels
            height (int): Height of the window in pixels
            block_size (int): Size of each tetris block in pixels
        """
        pygame.init()
        self.width = width
        self.height = height
        self.block_size = block_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Python Tetris")
        
        # Colors
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'gray': (128, 128, 128),
            'light_gray': (200, 200, 200),
            'dark_gray': (50, 50, 50),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'background': (240, 240, 240)
        }
        
        # Fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Calculate board position to center it
        self.board_width_px = block_size * 10  # 10 blocks wide
        self.board_height_px = block_size * 20  # 20 blocks high
        self.board_left = (width - self.board_width_px) // 2 - 100  # Offset to the left for UI
        self.board_top = (height - self.board_height_px) // 2
        
        # Next piece preview
        self.preview_size = block_size * 5  # 5x5 blocks
        self.preview_left = self.board_left + self.board_width_px + 20
        self.preview_top = self.board_top
        
    def draw(self, game):
        """
        Draw the entire game.
        
        Args:
            game (Game): The game object to render
        """
        # Clear the screen
        self.screen.fill(self.colors['background'])
        
        # Draw the board with gray grid background
        self.draw_board(game)
        
        # Draw the next piece preview
        self.draw_next_piece(game.next_piece)
        
        # Draw score and rows
        self.draw_score(game.visual_score, game.rows)
        
        # Draw game over or paused message if needed
        if game.game_over:
            self.draw_game_over()
        elif game.paused:
            self.draw_paused()
            
        # Update the display
        pygame.display.flip()
        
    def draw_board(self, game):
        """
        Draw the game board with a gray grid background.
        
        Args:
            game (Game): The game object containing the board state
        """
        # Draw the board background (gray grid)
        board_rect = pygame.Rect(
            self.board_left, 
            self.board_top, 
            self.board_width_px, 
            self.board_height_px
        )
        
        # Fill with light gray background
        pygame.draw.rect(self.screen, self.colors['light_gray'], board_rect)
        
        # Draw grid lines
        for x in range(game.width + 1):
            pygame.draw.line(
                self.screen,
                self.colors['gray'],
                (self.board_left + x * self.block_size, self.board_top),
                (self.board_left + x * self.block_size, self.board_top + self.board_height_px),
                1
            )
            
        for y in range(game.height + 1):
            pygame.draw.line(
                self.screen,
                self.colors['gray'],
                (self.board_left, self.board_top + y * self.block_size),
                (self.board_left + self.board_width_px, self.board_top + y * self.block_size),
                1
            )
        
        # Draw the border
        pygame.draw.rect(self.screen, self.colors['dark_gray'], board_rect, 2)
        
        # Draw the blocks on the board
        board_with_piece = game.get_board_with_piece()
        for x in range(game.width):
            for y in range(game.height):
                block = board_with_piece[x][y]
                if block:
                    self.draw_block(
                        x, 
                        y, 
                        self.get_color(block.color)
                    )
    
    def draw_block(self, x, y, color):
        """
        Draw a single block on the board.
        
        Args:
            x (int): X position in blocks
            y (int): Y position in blocks
            color (tuple): RGB color tuple
        """
        rect = pygame.Rect(
            self.board_left + x * self.block_size,
            self.board_top + y * self.block_size,
            self.block_size,
            self.block_size
        )
        
        # Fill the block
        pygame.draw.rect(self.screen, color, rect)
        
        # Draw a border
        pygame.draw.rect(self.screen, self.colors['dark_gray'], rect, 1)
        
        # Draw a highlight (3D effect)
        pygame.draw.line(
            self.screen,
            self.lighten_color(color),
            rect.topleft,
            rect.topright,
            1
        )
        pygame.draw.line(
            self.screen,
            self.lighten_color(color),
            rect.topleft,
            rect.bottomleft,
            1
        )
        pygame.draw.line(
            self.screen,
            self.darken_color(color),
            rect.bottomleft,
            rect.bottomright,
            1
        )
        pygame.draw.line(
            self.screen,
            self.darken_color(color),
            rect.topright,
            rect.bottomright,
            1
        )
    
    def draw_next_piece(self, piece):
        """
        Draw the next piece preview.
        
        Args:
            piece (dict): The next piece to draw
        """
        # Draw the preview box
        preview_rect = pygame.Rect(
            self.preview_left,
            self.preview_top,
            self.preview_size,
            self.preview_size
        )
        pygame.draw.rect(self.screen, self.colors['light_gray'], preview_rect)
        pygame.draw.rect(self.screen, self.colors['dark_gray'], preview_rect, 2)
        
        # Draw the "Next" label
        next_label = self.font_medium.render("Next", True, self.colors['dark_gray'])
        self.screen.blit(
            next_label, 
            (self.preview_left + (self.preview_size - next_label.get_width()) // 2,
             self.preview_top - 40)
        )
        
        # Calculate the center position for the piece
        piece_type = piece['type']
        piece_size = piece_type.size * self.block_size
        center_x = self.preview_left + (self.preview_size - piece_size) // 2
        center_y = self.preview_top + (self.preview_size - piece_size) // 2
        
        # Draw the piece
        for x, y in piece_type.each_block(0, 0, piece['dir']):
            self.draw_block(
                x + (center_x - self.board_left) // self.block_size,
                y + (center_y - self.board_top) // self.block_size,
                self.get_color(piece_type.color)
            )
    
    def draw_score(self, score, rows):
        """
        Draw the score and rows information.
        
        Args:
            score (int): Current score
            rows (int): Number of rows cleared
        """
        # Draw score
        score_label = self.font_medium.render("Score", True, self.colors['dark_gray'])
        score_value = self.font_medium.render(f"{score:08d}", True, self.colors['red'])
        
        self.screen.blit(
            score_label,
            (self.preview_left + (self.preview_size - score_label.get_width()) // 2,
             self.preview_top + self.preview_size + 20)
        )
        
        self.screen.blit(
            score_value,
            (self.preview_left + (self.preview_size - score_value.get_width()) // 2,
             self.preview_top + self.preview_size + 60)
        )
        
        # Draw rows
        rows_label = self.font_medium.render("Rows", True, self.colors['dark_gray'])
        rows_value = self.font_medium.render(str(rows), True, self.colors['blue'])
        
        self.screen.blit(
            rows_label,
            (self.preview_left + (self.preview_size - rows_label.get_width()) // 2,
             self.preview_top + self.preview_size + 100)
        )
        
        self.screen.blit(
            rows_value,
            (self.preview_left + (self.preview_size - rows_value.get_width()) // 2,
             self.preview_top + self.preview_size + 140)
        )
        
        # Draw controls help
        controls = [
            "Controls:",
            "LEFT RIGHT: Move",
            "UP : Rotate",
            "DOWN : Drop",
            "P : Pause",
            "M : On/Off AI Mode",
            "Esc : Quit"
        ]
        
        y_pos = self.preview_top + self.preview_size + 180
        for text in controls:
            control_text = self.font_small.render(text, True, self.colors['dark_gray'])
            self.screen.blit(
                control_text,
                (self.preview_left, y_pos)
            )
            y_pos += 25
    
    def draw_game_over(self):
        """Draw the game over message."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font_large.render("GAME OVER", True, self.colors['white'])
        restart_text = self.font_medium.render("Press SPACE to restart", True, self.colors['white'])
        
        self.screen.blit(
            game_over_text,
            ((self.width - game_over_text.get_width()) // 2,
             (self.height - game_over_text.get_height()) // 2 - 30)
        )
        
        self.screen.blit(
            restart_text,
            ((self.width - restart_text.get_width()) // 2,
             (self.height - restart_text.get_height()) // 2 + 30)
        )
    
    def draw_paused(self):
        """Draw the paused message."""
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        paused_text = self.font_large.render("PAUSED", True, self.colors['white'])
        continue_text = self.font_medium.render("Press P to continue", True, self.colors['white'])
        
        self.screen.blit(
            paused_text,
            ((self.width - paused_text.get_width()) // 2,
             (self.height - paused_text.get_height()) // 2 - 30)
        )
        
        self.screen.blit(
            continue_text,
            ((self.width - continue_text.get_width()) // 2,
             (self.height - continue_text.get_height()) // 2 + 30)
        )
    
    def get_color(self, color_name):
        """
        Convert a color name to an RGB tuple.
        
        Args:
            color_name (str): Name of the color
            
        Returns:
            tuple: RGB color tuple
        """
        color_map = {
            'cyan': (0, 255, 255),
            'blue': (0, 0, 255),
            'orange': (255, 165, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
            'purple': (128, 0, 128),
            'red': (255, 0, 0)
        }
        
        return color_map.get(color_name, (255, 255, 255))  # Default to white
    
    def lighten_color(self, color, amount=50):
        """
        Lighten a color by the given amount.
        
        Args:
            color (tuple): RGB color tuple
            amount (int): Amount to lighten by
            
        Returns:
            tuple: Lightened RGB color tuple
        """
        r, g, b = color
        return (
            min(255, r + amount),
            min(255, g + amount),
            min(255, b + amount)
        )
    
    def darken_color(self, color, amount=50):
        """
        Darken a color by the given amount.
        
        Args:
            color (tuple): RGB color tuple
            amount (int): Amount to darken by
            
        Returns:
            tuple: Darkened RGB color tuple
        """
        r, g, b = color
        return (
            max(0, r - amount),
            max(0, g - amount),
            max(0, b - amount)
        )