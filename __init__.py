"""
Rubik's Cube Solver - Main Package
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__description__ = "High-performance Rubik's Cube solver with multiple algorithms"

from cube.cube import Cube
from cube.moves import Move, MoveCommand
from solvers.bfs_solver import BFSSolver
from solvers.ida_solver import IDASolver
from solvers.kociemba_wrapper import KociembaWrapper

__all__ = [
    'Cube',
    'Move',
    'MoveCommand',
    'BFSSolver',
    'IDASolver',
    'KociembaWrapper',
]
