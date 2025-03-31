"""
AI agent for Python Tetris using heuristic evaluation.
This module provides functions for evaluating board states and selecting optimal moves.
"""

import copy
from tetromino import UP, RIGHT, DOWN, LEFT

def evaluate_board(board, width, height):
    """
    Evaluate a board state using heuristic features.
    
    Args:
        board (list): 2D list representing the game board
        width (int): Width of the board
        height (int): Height of the board
        
    Returns:
        float: Heuristic score for the board state
    """
    aggregate_height = 0
    complete_lines = 0
    holes = 0
    bumpiness = 0
    column_heights = [0] * width
    
    # Calculate aggregate height and column heights
    for x in range(width):
        for y in range(height):
            if board[x][y]:
                column_heights[x] = height - y
                aggregate_height += column_heights[x]
                break
    
    # Calculate complete lines
    for y in range(height):
        complete = True
        for x in range(width):
            if not board[x][y]:
                complete = False
                break
        if complete:
            complete_lines += 1
    
    # Calculate holes
    for x in range(width):
        block_found = False
        for y in range(height):
            if board[x][y]:
                block_found = True
            elif block_found and not board[x][y]:
                holes += 1
    
    # Calculate bumpiness
    for x in range(width - 1):
        bumpiness += abs(column_heights[x] - column_heights[x + 1])
    
    # Combine features into a heuristic score
    # Using the same weights as the JavaScript version
    return -0.51 * aggregate_height + 0.76 * complete_lines - 0.36 * holes - 0.18 * bumpiness

def copy_board(board, width, height):
    """
    Create a deep copy of the game board.
    
    Args:
        board (list): 2D list representing the game board
        width (int): Width of the board
        height (int): Height of the board
        
    Returns:
        list: Deep copy of the board
    """
    return copy.deepcopy(board)

def get_drop_position(game, piece, x):
    """
    Determine where a piece will land if dropped from a given position.
    
    Args:
        game (Game): The game object
        piece (dict): The piece to drop
        x (int): X position to drop from
        
    Returns:
        int: Y position where the piece will land
    """
    y = 0
    while not game.is_occupied(piece['type'], x, y + 1, piece['dir']):
        y += 1
    return y

def get_possible_moves(game, piece, board_state=None):
    """
    Generate all possible moves for the current piece.
    
    Args:
        game (Game): The game object
        piece (dict): The piece to evaluate
        board_state (list, optional): Custom board state to use. Defaults to the game's current board.
        
    Returns:
        list: List of possible moves with their resulting board states
    """
    moves = []
    rotations = [0, 1, 2, 3]  # All possible rotations
    current_state = board_state if board_state is not None else game.board
    width, height = game.width, game.height
    
    # For each rotation of the piece
    for dir in rotations:
        # Create a copy of the piece with the new rotation
        rotated_piece = {
            'type': piece['type'],
            'dir': dir,
            'x': piece['x'],
            'y': piece['y']
        }
        
        # For each horizontal position
        for x in range(-3, width + 3):  # Allow for piece to extend beyond edges
            y = get_drop_position(game, rotated_piece, x)
            
            # Check if the piece can be placed here
            if not game.is_occupied(rotated_piece['type'], x, y, dir):
                # Create a copy of the board
                new_board = copy_board(current_state, width, height)
                
                # Place the piece on the board
                for block_x, block_y in rotated_piece['type'].each_block(x, y, dir):
                    if 0 <= block_x < width and 0 <= block_y < height:
                        new_board[block_x][block_y] = rotated_piece['type']
                
                moves.append({
                    'piece': rotated_piece,
                    'x': x,
                    'y': y,
                    'board': new_board
                })
    
    return moves

def select_best_move_greedy(game, piece):
    """
    Select the best move based on immediate heuristic evaluation.
    
    Args:
        game (Game): The game object
        piece (dict): The piece to evaluate
        
    Returns:
        dict: The best move
    """
    moves = get_possible_moves(game, piece)
    best_move = None
    best_score = float('-inf')
    
    for move in moves:
        score = evaluate_board(move['board'], game.width, game.height)
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

def select_best_move(game, piece, next_piece):
    """
    Select the best move considering the current piece and the next piece.
    
    Args:
        game (Game): The game object
        piece (dict): The current piece
        next_piece (dict): The next piece
        
    Returns:
        dict: The best move for the current piece
    """
    # First turn: generate all possible moves for the current piece
    moves = get_possible_moves(game, piece)
    for move in moves:
        move['father'] = move
    
    # Second turn: for each first move, generate all possible moves for the next piece
    new_moves = []
    for move in moves:
        board_after_first_move = move['board']
        next_moves = get_possible_moves(game, next_piece, board_after_first_move)
        
        for next_move in next_moves:
            next_move['father'] = move['father']
            next_move['score'] = evaluate_board(next_move['board'], game.width, game.height)
            new_moves.append(next_move)
    
    # Sort by score and return the father of the best move
    new_moves.sort(key=lambda x: x['score'], reverse=True)
    
    if new_moves:
        return new_moves[0]['father']
    elif moves:  # Fallback if no next moves
        return moves[0]
    else:
        return None  # No valid moves