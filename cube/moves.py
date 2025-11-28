"""
Move definitions and command interface for applying/undoing moves.

Supports all standard Rubik's Cube moves: U, D, L, R, F, B (and their variants).
"""

from __future__ import annotations
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .cube import Cube


class Move:
    """
    Represents a single move with undo capability.
    
    Attributes:
        name (str): Move name (e.g., 'U', 'R2', 'F\'').
        apply_func (Callable): Function to apply the move to a cube.
        undo_func (Callable): Function to undo the move.
    """
    
    def __init__(
        self,
        name: str,
        apply_func: Callable[[Cube], None],
        undo_func: Callable[[Cube], None] | None = None
    ) -> None:
        """
        Initialize a Move.
        
        Args:
            name (str): Move name.
            apply_func (Callable): Function to apply move.
            undo_func (Callable, optional): Function to undo. Defaults to inverse of apply.
        """
        self.name = name
        self.apply_func = apply_func
        self.undo_func: Callable[[Cube], None] = undo_func if undo_func is not None else lambda cube: None
    
    def __str__(self) -> str:
        """Return the move name."""
        return self.name
    
    def apply(self, cube: Cube) -> None:
        """Apply the move to a cube."""
        self.apply_func(cube)
    
    def undo(self, cube: Cube) -> None:
        """Undo the move from a cube."""
        self.undo_func(cube)


class MoveCommand:
    """
    Command pattern interface for applying moves with history tracking.
    
    This allows easy undo/redo functionality.
    """
    
    # Define all standard moves
    MOVES: dict[str, Move] = {}
    
    def __init__(self, cube: Cube) -> None:
        """
        Initialize command with a cube.
        
        Args:
            cube (Cube): The cube to operate on.
        """
        self.cube = cube
        self.history: list[Move] = []
        
        # Initialize MOVES only once
        if not MoveCommand.MOVES:
            MoveCommand.MOVES = {
                'U': Move('U', lambda c: c.move_U(), lambda c: c.move_U_prime()),
                'U\'': Move('U\'', lambda c: c.move_U_prime(), lambda c: c.move_U()),
                'U2': Move('U2', lambda c: c.move_U2(), lambda c: c.move_U2()),
                
                'D': Move('D', lambda c: c.move_D(), lambda c: c.move_D_prime()),
                'D\'': Move('D\'', lambda c: c.move_D_prime(), lambda c: c.move_D()),
                'D2': Move('D2', lambda c: c.move_D2(), lambda c: c.move_D2()),
                
                'L': Move('L', lambda c: c.move_L(), lambda c: c.move_L_prime()),
                'L\'': Move('L\'', lambda c: c.move_L_prime(), lambda c: c.move_L()),
                'L2': Move('L2', lambda c: c.move_L2(), lambda c: c.move_L2()),
                
                'R': Move('R', lambda c: c.move_R(), lambda c: c.move_R_prime()),
                'R\'': Move('R\'', lambda c: c.move_R_prime(), lambda c: c.move_R()),
                'R2': Move('R2', lambda c: c.move_R2(), lambda c: c.move_R2()),
                
                'F': Move('F', lambda c: c.move_F(), lambda c: c.move_F_prime()),
                'F\'': Move('F\'', lambda c: c.move_F_prime(), lambda c: c.move_F()),
                'F2': Move('F2', lambda c: c.move_F2(), lambda c: c.move_F2()),
                
                'B': Move('B', lambda c: c.move_B(), lambda c: c.move_B_prime()),
                'B\'': Move('B\'', lambda c: c.move_B_prime(), lambda c: c.move_B()),
                'B2': Move('B2', lambda c: c.move_B2(), lambda c: c.move_B2()),
            }
    
    def execute(self, move_name: str) -> None:
        """
        Execute a move and add to history.
        
        Args:
            move_name (str): Name of the move (e.g., 'U', 'R2', 'F\'').
        
        Raises:
            ValueError: If move_name is not recognized.
        """
        if move_name not in self.MOVES:
            raise ValueError(f"Unknown move: {move_name}. Valid moves: {list(self.MOVES.keys())}")
        
        move = self.MOVES[move_name]
        move.apply(self.cube)
        self.history.append(move)
    
    def execute_sequence(self, moves_str: str) -> None:
        """
        Execute a sequence of moves from a space-separated string.
        
        Args:
            moves_str (str): Space-separated move names (e.g., "U R U' R' U2 F").
        """
        moves = moves_str.split()
        for move_name in moves:
            self.execute(move_name)
    
    def undo_last(self) -> None:
        """Undo the last move."""
        if not self.history:
            raise RuntimeError("No moves to undo")
        move = self.history.pop()
        move.undo(self.cube)
    
    def undo_all(self) -> None:
        """Undo all moves in reverse order."""
        while self.history:
            self.undo_last()
    
    def get_history(self) -> list[str]:
        """
        Get list of applied moves.
        
        Returns:
            list[str]: Names of applied moves in order.
        """
        return [move.name for move in self.history]
    
    def get_solution_string(self) -> str:
        """
        Get solution as a single space-separated string.
        
        Returns:
            str: Move sequence string.
        """
        return ' '.join(self.get_history())
