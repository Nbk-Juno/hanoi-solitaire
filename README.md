# Hanoi Solitaire

A GUI-based card game implementing Hanoi Solitaire with a built-in solver.

## About the Game

Hanoi Solitaire is a card game version of the classic Tower of Hanoi puzzle. Using 9 cards (Ace through 9), the goal is to move all cards from the starting piles to a single destination pile, stacked in descending order (9 at the bottom, Ace at the top).

### Rules

- Move only one card at a time
- Only the top card of a pile can be moved
- A smaller card can only be placed on a larger card or an empty pile
- Win by getting all cards on a single pile in descending order

## Project Status

🚧 **Under Development** 🚧

This project is being built incrementally following a structured plan:

- [x] Phase 1: Project Setup
- [x] Phase 2: Core Game Logic
- [ ] Phase 3: Basic GUI
- [ ] Phase 4: Game Polish
- [ ] Phase 5: Solver Algorithm
- [ ] Phase 6: Solver Visualization
- [ ] Phase 7: Enhanced Features
- [ ] Phase 8: Testing
- [ ] Phase 9: Documentation

## How to Run

### Prerequisites

- Python 3.12 or higher
- tkinter (comes with Python)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/hanoi-solitaire.git
cd hanoi-solitaire

# (Optional) Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Game

```bash
python src/gui.py
```

### Running Tests

```bash
pytest tests/
```

## Features (Planned)

- ✨ Playable GUI using Python's tkinter
- 🤖 Automated solver using recursive algorithm
- ↩️ Undo/Redo functionality
- 📊 Move counter
- 🎨 Visual card animations

## Development

### Project Structure

```
hanoi-solitaire/
├── src/
│   ├── __init__.py
│   ├── game.py      # Game logic and rules
│   ├── solver.py    # Solving algorithm
│   └── gui.py       # tkinter GUI
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

### Testing the Game Logic

```bash
python src/game.py
```

## Learning Goals

This project focuses on:
- Recursion and algorithmic thinking
- Game state management
- GUI programming with tkinter
- Event handling and user interaction
- Data structures (stacks/lists)

## License

This project is for educational purposes.

## Acknowledgments

Based on the classic Tower of Hanoi puzzle, adapted as a card game.
