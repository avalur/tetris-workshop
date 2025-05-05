## Tetris Workshop

Here is the workshop slides: https://avalur.github.io/talks/TetrisWorkshop.html

This repository contains two implementations of the classic Tetris game:

1. **JavaScript Implementation**: A browser-based version using HTML5 Canvas
2. **Python Implementation**: A desktop version using Pygame

Both implementations share the same core game mechanics and features, including an AI agent that can play the game automatically using heuristic evaluation.

## Features

- Classic Tetris gameplay with all seven standard tetromino pieces
- Score tracking, next piece preview
- AI mode with heuristic-based decision-making
- Performance monitoring and benchmarking tools
- Responsive design

## Installation

### JavaScript Version

No installation required! Simply open `javascript-tetris/index.html` in any modern web browser.

### Python Version

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:
   ```
   pip install pygame
   ```
3. Navigate to the python-tetris directory:
   ```
   cd python-tetris
   ```
4. Run the game:
   ```
   python main.py
   ```

## How to Play

### Controls

Both versions share similar controls:

- **Left/Right Arrow**: Move piece horizontally
- **Down Arrow**: Move piece down faster
- **Up Arrow**: Rotate piece
- **Space**: Hard drop (instantly drop the piece)
- **P**: Pause/unpause game
- **M**: Toggle AI mode (Python version)
- **Escape**: End game

### Scoring

- Points are awarded for clearing lines and dropping pieces
- Clearing multiple lines at once awards bonus points

## Project Structure

### JavaScript Implementation

```
javascript-tetris/
├── game.js              # Core game logic
├── heuristic_agent.js   # AI implementation
├── index.html           # Game UI and entry point
├── stats.js             # Performance monitoring
├── texture.jpg          # Background texture
└── utils.js             # Utility functions
```

### Python Implementation

```
python-tetris/
├── main.py              # Entry point, game initialization
├── game.py              # Core game logic
├── tetromino.py         # Tetromino pieces definitions
├── renderer.py          # Pygame rendering logic
├── heuristic_agent.py   # AI implementation
├── utils.py             # Utility functions
└── performance.py       # Performance monitoring
```

## AI Agent

Both implementations include an AI agent that can play the game automatically.
Actually, the Python version has a few bugs. Try to fix them!
The agent uses a heuristic evaluation function to score potential moves and select the best one. 
The evaluation considers factors such as:

- Height of the stack
- Number of holes
- Line completeness
- Surface smoothness

To enable AI mode:
- In the Python version, press 'M' during gameplay
- In the JavaScript version, use the utility functions in the browser console

## Performance Testing

Both implementations include tools for performance testing:

- JavaScript: Click the "Run Performance Test" button
- Python: Performance metrics are displayed in real-time during gameplay

## Development

This project demonstrates how to implement the same game in different programming languages while maintaining feature parity. The Python implementation was created as a port of the original JavaScript version, following the plan outlined in `python-tetris/plan.md`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
