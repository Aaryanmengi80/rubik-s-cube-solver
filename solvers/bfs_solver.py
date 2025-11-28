"""
Breadth-first search (BFS) solver for Rubik's Cube.
Educational implementation - guarantees shortest path but slow.
"""

from collections import deque
from typing import Tuple, Set
from cube.cube import Cube
from cube.moves import MoveCommand
from .solver_interface import Solver


class BFSSolver(Solver):
    """
    BFS Solver for Rubik's Cube.
    
    Finds the shortest solution by exploring all move sequences level-by-level.
    Warning: Can be extremely slow for non-trivial scrambles (> 5-10 moves away).
    """
    
    MOVES = ['U', 'U\'', 'U2', 'D', 'D\'', 'D2', 
             'L', 'L\'', 'L2', 'R', 'R\'', 'R2',
             'F', 'F\'', 'F2', 'B', 'B\'', 'B2']
    
    def solve(self, cube: Cube) -> Tuple[list[str], int]:
        """
        Solve using breadth-first search.
        
        Args:
            cube (Cube): The cube to solve.
        
        Returns:
            Tuple[list[str], int]: (list of moves, nodes explored)
        
        Raises:
            RuntimeError: If cube cannot be solved within reasonable depth.
        """
        if cube.is_solved():
            return [], 1
        
        queue: deque[tuple[Cube, list[str]]] = deque([(cube.copy(), [])])
        visited: Set[str] = {cube.state}
        nodes_explored = 0
        
        # Limit search depth to prevent infinite loops
        max_depth = 8
        
        while queue:
            current_cube, moves = queue.popleft()
            nodes_explored += 1
            
            if len(moves) >= max_depth:
                raise RuntimeError(
                    f"Solution not found within {max_depth} moves. "
                    "BFS is too slow for this scramble."
                )
            
            for move_name in self.MOVES:
                next_cube = current_cube.copy()
                cmd = MoveCommand(next_cube)
                cmd.execute(move_name)
                
                if next_cube.is_solved():
                    return moves + [move_name], nodes_explored
                
                if next_cube.state not in visited:
                    visited.add(next_cube.state)
                    queue.append((next_cube, moves + [move_name]))
        
        raise RuntimeError("No solution found (should not happen).")
