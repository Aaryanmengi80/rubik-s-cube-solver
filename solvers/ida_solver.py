"""
Iterative Deepening A* (IDA*) solver for Rubik's Cube.
Production-ready solver with configurable heuristics.
"""

from typing import Tuple, Optional
from cube.cube import Cube
from cube.moves import MoveCommand
from .solver_interface import Solver


class IDASolver(Solver):
    """
    IDA* Solver for Rubik's Cube.
    
    Uses iterative deepening with a heuristic function to explore the search space.
    Configurable heuristics:
      - misplaced_count: Number of misplaced cubelets
      - wrong_face_count: Sum of wrong-face color counts
    """
    
    MOVES = ['U', 'U\'', 'U2', 'D', 'D\'', 'D2', 
             'L', 'L\'', 'L2', 'R', 'R\'', 'R2',
             'F', 'F\'', 'F2', 'B', 'B\'', 'B2']
    
    def __init__(self, heuristic: str = "misplaced") -> None:
        """
        Initialize IDA* solver with a heuristic.
        
        Args:
            heuristic (str): "misplaced" or "wrong_face". Defaults to "misplaced".
        """
        super().__init__()
        self.heuristic_name = heuristic
        
        if heuristic == "misplaced":
            self.heuristic = self._heuristic_misplaced
        elif heuristic == "wrong_face":
            self.heuristic = self._heuristic_wrong_face
        else:
            raise ValueError(f"Unknown heuristic: {heuristic}")
        
        self.nodes_explored = 0
    
    def _heuristic_misplaced(self, cube: Cube) -> int:
        """
        Estimate cost using misplaced cubelets count.
        
        A cubelet is misplaced if it's not on its home face.
        
        Args:
            cube (Cube): The cube to evaluate.
        
        Returns:
            int: Lower bound on remaining moves.
        """
        target = "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYY"
        misplaced = sum(1 for i in range(54) if cube.state[i] != target[i])
        # Divide by 2 because each move affects ~2 cubelets (rough estimate)
        return max(1, misplaced // 8)
    
    def _heuristic_wrong_face(self, cube: Cube) -> int:
        """
        Estimate cost using sum of wrong-face color counts.
        
        For each face, count how many stickers don't match the center color.
        
        Args:
            cube (Cube): The cube to evaluate.
        
        Returns:
            int: Lower bound on remaining moves.
        """
        target_colors = ['W', 'O', 'G', 'R', 'B', 'Y']
        wrong_count = 0
        
        for face_idx in range(6):
            start = face_idx * 9
            center_color = target_colors[face_idx]
            for i in range(9):
                if cube.state[start + i] != center_color:
                    wrong_count += 1
        
        return max(1, wrong_count // 8)
    
    def solve(self, cube: Cube, max_depth: int = 20) -> Tuple[list[str], int]:
        """
        Solve using IDA* algorithm.
        
        Args:
            cube (Cube): The cube to solve.
            max_depth (int): Maximum search depth. Defaults to 20.
        
        Returns:
            Tuple[list[str], int]: (list of moves, nodes explored)
        
        Raises:
            RuntimeError: If no solution found within max_depth.
        """
        if cube.is_solved():
            return [], 1
        
        self.nodes_explored = 0
        
        # Iterative deepening
        for depth_limit in range(0, max_depth + 1):
            result = self._search(cube.copy(), [], 0, depth_limit)
            if result is not None:
                return result, self.nodes_explored
        
        raise RuntimeError(
            f"Solution not found within {max_depth} moves. "
            "Cube may be invalid or unsolvable."
        )
    
    def _search(
        self,
        cube: Cube,
        moves: list[str],
        depth: int,
        depth_limit: int
    ) -> Optional[list[str]]:
        """
        Recursive search function for IDA*.
        
        Args:
            cube (Cube): Current cube state.
            moves (list[str]): Moves applied so far.
            depth (int): Current depth in search tree.
            depth_limit (int): Maximum depth to explore.
        
        Returns:
            Optional[list[str]]: Solution moves if found, None otherwise.
        """
        self.nodes_explored += 1
        
        if cube.is_solved():
            return moves
        
        if depth >= depth_limit:
            return None
        
        h_value = self.heuristic(cube)
        if depth + h_value > depth_limit:
            return None
        
        # Avoid reversing the last move
        last_move = moves[-1] if moves else None
        
        for move_name in self.MOVES:
            # Skip reversing last move
            if last_move:
                base_last = last_move.rstrip('\'2')
                base_current = move_name.rstrip('\'2')
                if base_last == base_current:
                    continue
            
            next_cube = cube.copy()
            cmd = MoveCommand(next_cube)
            cmd.execute(move_name)
            
            result = self._search(next_cube, moves + [move_name], depth + 1, depth_limit)
            if result is not None:
                return result
        
        return None
