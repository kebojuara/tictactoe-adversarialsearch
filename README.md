# TicTacToe - Adversarial Search

A desktop Tic-Tac-Toe game in which you play against an AI opponent that chooses its moves with adversarial search. The AI can use either Minimax or Minimax with Alpha-Beta pruning, and the interface reports search statistics after each AI move so the two algorithms can be compared.

The project was developed as university coursework.

## Features

- Play as X against the AI, or let the AI move first (you then play O).
- Choose the search algorithm from a dropdown: Alpha-Beta (default) or Minimax.
- Per-move analysis panel showing:
  - nodes expanded
  - maximum search depth reached
  - runtime in milliseconds
  - peak memory in KB, measured with `tracemalloc`
- Depth-aware utility function: wins score `100 - depth`, losses score `depth - 100`, and draws score `0`, so the AI prefers faster wins and slower losses.
- Buttons to start a new game or reset the board.

## Tech Stack

- Language: Python 3
- GUI: [Pygame](https://www.pygame.org/)
- Standard library: `time`, `tracemalloc`, `typing`, `sys`

## Project Structure

```text
.
├── main.py       # Game engine: board helpers, Minimax, Alpha-Beta, search statistics
├── interface.py  # Pygame GUI and game loop (entry point)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3
- Pygame

The repository has no dependency manifest, so Pygame must be installed manually.

### Installation

```bash
pip install pygame
```

### Running the Project

Run the GUI from the repository root:

```bash
python interface.py
```

## Usage

1. Select a search algorithm in the dropdown on the right.
2. Click a cell to place your mark. By default you play X and the AI plays O.
3. Click **New Game (AI First)** to let the AI open as X. You then play O.
4. Click **New Game (You=X)** to start a new game where you move first.
5. Click **Reset Board** to clear the board.
6. After each AI move, read the analysis panel to see the cost of the selected algorithm.

## Architecture

- [`main.py`](main.py) is independent of the GUI. The board is a list of nine strings (`'X'`, `'O'` or `' '`). `minimax` and `alphabeta` return a score and best move, and `ai_move` wraps the chosen algorithm with timing and memory measurement, returning the move and a `SearchStats` object.
- [`interface.py`](interface.py) imports `main` as the engine and handles rendering, mouse input, and turn management.
