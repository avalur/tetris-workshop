"""
Performance monitoring for Python Tetris.
This module provides a class for tracking and displaying performance metrics.
"""

import time
import pygame

class PerformanceMonitor:
    """
    Class for tracking and displaying performance metrics.
    """
    
    def __init__(self, x=10, y=10, width=80, height=40, font_size=12):
        """
        Initialize the performance monitor.
        
        Args:
            x (int): X position of the monitor
            y (int): Y position of the monitor
            width (int): Width of the monitor
            height (int): Height of the monitor
            font_size (int): Font size for text
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        
        # Performance metrics
        self.fps = 0
        self.frame_time = 0
        self.min_fps = float('inf')
        self.max_fps = 0
        self.min_frame_time = float('inf')
        self.max_frame_time = 0
        
        # Timing variables
        self.last_update = time.time()
        self.frames = 0
        self.last_second = time.time()
        
        # Font for rendering text
        self.font = pygame.font.Font(None, font_size)
        
        # Colors
        self.bg_color = (16, 16, 48, 180)  # Semi-transparent dark blue
        self.text_color = (0, 255, 255)    # Cyan
        
    def update(self):
        """
        Update performance metrics.
        Should be called once per frame.
        """
        current_time = time.time()
        
        # Calculate frame time
        self.frame_time = (current_time - self.last_update) * 1000  # Convert to ms
        self.last_update = current_time
        
        # Update min/max frame time
        self.min_frame_time = min(self.min_frame_time, self.frame_time)
        self.max_frame_time = max(self.max_frame_time, self.frame_time)
        
        # Count frames
        self.frames += 1
        
        # Update FPS once per second
        if current_time - self.last_second >= 1.0:
            self.fps = self.frames / (current_time - self.last_second)
            self.frames = 0
            self.last_second = current_time
            
            # Update min/max FPS
            self.min_fps = min(self.min_fps, self.fps)
            self.max_fps = max(self.max_fps, self.fps)
    
    def draw(self, surface):
        """
        Draw the performance monitor on the given surface.
        
        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Create a semi-transparent background
        bg_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        bg_surface.fill(self.bg_color)
        surface.blit(bg_surface, (self.x, self.y))
        
        # Render FPS text
        fps_text = self.font.render(f"FPS: {self.fps:.1f}", True, self.text_color)
        surface.blit(fps_text, (self.x + 5, self.y + 5))
        
        # Render frame time text
        time_text = self.font.render(f"MS: {self.frame_time:.1f}", True, self.text_color)
        surface.blit(time_text, (self.x + 5, self.y + 5 + self.font_size))
        
    def reset(self):
        """
        Reset performance metrics.
        """
        self.fps = 0
        self.frame_time = 0
        self.min_fps = float('inf')
        self.max_fps = 0
        self.min_frame_time = float('inf')
        self.max_frame_time = 0
        self.last_update = time.time()
        self.frames = 0
        self.last_second = time.time()