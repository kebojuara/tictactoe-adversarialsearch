import time
import tracemalloc
from typing import List, Tuple, Optional

LINES = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

def new_board() -> List[str]:
    return [' '] * 9

def available_moves(board: List[str]) -> List[int]:
    return [i for i, v in enumerate(board) if v == ' ']

def winner(board: List[str]) -> Optional[str]:
    for a,b,c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def is_terminal(board: List[str]) -> bool:
    return winner(board) is not None or all(v != ' ' for v in board)

def other(p: str) -> str:
    return 'O' if p == 'X' else 'X'

def utility(board: List[str], me: str, depth: int) -> int:
    w = winner(board)
    if w == me:
        return 100 - depth
    elif w is None and all(v != ' ' for v in board):
        return 0
    elif w is None:
        return 0
    else:
        return depth - 100

class SearchStats:
    def __init__(self):
        self.nodes = 0
        self.depth = 0
        self.runtime = 0.0
        self.peak_bytes = 0

def ordered_moves(board: List[str]) -> List[int]:
    return available_moves(board)

def minimax(board: List[str], me: str, to_move: str, stats: SearchStats, depth: int = 0) -> Tuple[int, Optional[int]]:
    stats.nodes += 1
    stats.depth = max(stats.depth, depth)
    if is_terminal(board):
        return utility(board, me, depth), None
    best_move = None
    if to_move == me:
        best_val = -10000
        for m in ordered_moves(board):
            board[m] = to_move
            val, _ = minimax(board, me, other(to_move), stats, depth + 1)
            board[m] = ' '
            if val > best_val:
                best_val, best_move = val, m
        return best_val, best_move
    else:
        best_val = 10000
        for m in ordered_moves(board):
            board[m] = to_move
            val, _ = minimax(board, me, other(to_move), stats, depth + 1)
            board[m] = ' '
            if val < best_val:
                best_val, best_move = val, m
        return best_val, best_move

def alphabeta(board: List[str], me: str, to_move: str, stats: SearchStats, alpha: int = -10000, beta: int = 10000, depth: int = 0) -> Tuple[int, Optional[int]]:
    stats.nodes += 1
    stats.depth = max(stats.depth, depth)
    if is_terminal(board):
        return utility(board, me, depth), None
    best_move = None
    if to_move == me:
        v = -10000
        for m in ordered_moves(board):
            board[m] = to_move
            val, _ = alphabeta(board, me, other(to_move), stats, alpha, beta, depth + 1)
            board[m] = ' '
            if val > v:
                v, best_move = val, m
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, best_move
    else:
        v = 10000
        for m in ordered_moves(board):
            board[m] = to_move
            val, _ = alphabeta(board, me, other(to_move), stats, alpha, beta, depth + 1)
            board[m] = ' '
            if val < v:
                v, best_move = val, m
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v, best_move

def ai_move(board: List[str], ai_symbol: str, algorithm: str = "Alpha-Beta"):
    stats = SearchStats()
    tracemalloc.start()
    start = time.time()
    if algorithm == "Minimax":
        _, move = minimax(board, ai_symbol, ai_symbol, stats, 0)
    elif algorithm == "Alpha-Beta":
        _, move = alphabeta(board, ai_symbol, ai_symbol, stats, -10000, 10000, 0)
    else:
        _, move = alphabeta(board, ai_symbol, ai_symbol, stats, -10000, 10000, 0)
    stats.runtime = (time.time() - start) * 1000.0
    _, peak = tracemalloc.get_traced_memory()
    stats.peak_bytes = int(peak)
    tracemalloc.stop()
    return (move if move is not None else -1), stats
