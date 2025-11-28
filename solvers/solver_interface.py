"""
Solver interface and base class.
All solvers should inherit from Solver.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from cube.cube import Cube


class Solver(ABC):
    """
    Abstract base class for Rubik's Cube solvers.
    
    All concrete solvers must implement the solve() method.
    """
    
    def __init__(self):
        """Initialize the solver."""
        self.name = self.__class__.__name__
    
    @abstractmethod
    def solve(self, cube: Cube) -> Tuple[List[str], int]:
        """
        Solve a Rubik's Cube.
        
        Args:
            cube (Cube): The cube to solve.
        
        Returns:
            Tuple[List[str], int]: (list of move names, number of nodes explored)
        
        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        pass
    
    def is_goal(self, cube: Cube) -> bool:
        """
        Check if a cube is in the goal (solved) state.
        
        Args:
            cube (Cube): The cube to check.
        
        Returns:
            bool: True if solved.
        """
        return cube.is_solved()
