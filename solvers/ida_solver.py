"""
IDA* (Iterative Deepening A*) solver for Rubik's Cube.
Uses heuristic search to find optimal solutions efficiently.
"""

from typing import List, Tuple, Callable, Optional
from cube.cube import Cube
from cube.moves import MoveCommand


class IDASolver:
    """Iterative Deepening A* solver for Rubik's Cube."""
    
    def __init__(self, heuristic: str = "misplaced") -> None:
        """Initialize IDA* solver with specified heuristic.
        
        Args:
            heuristic: Type of heuristic ('misplaced', 'wrong_face', 'manhattan')
        """
        if heuristic not in ["misplaced", "wrong_face", "manhattan"]:
            raise ValueError(f"Unknown heuristic: {heuristic}")
        
        self.heuristic_type = heuristic
        self.name = "IDASolver"
        self.nodes_explored = 0
        
        # Set heuristic function
        if heuristic == "misplaced":
            self.heuristic: Callable[[Cube], int] = self._heuristic_misplaced
        elif heuristic == "wrong_face":
            self.heuristic: Callable[[Cube], int] = self._heuristic_wrong_face
        else:
            self.heuristic: Callable[[Cube], int] = self._heuristic_manhattan
    
    def _heuristic_misplaced(self, cube: Cube) -> int:
        """Count misplaced pieces heuristic.
        
        Args:
            cube: Current cube state
            
        Returns:
            Number of misplaced pieces divided by 8 (as lower bound)
        """
        target = "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYYY"
        
        # Ensure both strings are exactly 54 characters
        if len(cube.state) != 54 or len(target) != 54:
            return 0
        
        misplaced = sum(1 for i in range(54) if cube.state[i] != target[i])
        return misplaced // 8  # Divide by 8 for admissible heuristic
    
    def _heuristic_wrong_face(self, cube: Cube) -> int:
        """Count wrong-face pieces heuristic.
        
        Args:
            cube: Current cube state
            
        Returns:
            Number of pieces on wrong face divided by 12
        """
        target = "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYYY"
        
        # Define which indices belong to which face
        faces = {
            'W': list(range(0, 9)),      # White (top)
            'O': list(range(9, 18)),     # Orange (left)
            'G': list(range(18, 27)),    # Green (front)
            'R': list(range(27, 36)),    # Red (right)
            'B': list(range(36, 45)),    # Blue (back)
            'Y': list(range(45, 54))     # Yellow (bottom)
        }
        
        # Ensure length is correct
        if len(cube.state) != 54 or len(target) != 54:
            return 0
        
        wrong_face = 0
        for face_color, indices in faces.items():
            for idx in indices:
                if cube.state[idx] != face_color:
                    wrong_face += 1
        
        return wrong_face // 12  # Divide by 12 for admissible heuristic
    
    def _heuristic_manhattan(self, cube: Cube) -> int:
        """Simple manhattan distance heuristic.
        
        Args:
            cube: Current cube state
            
        Returns:
            Estimated moves needed (simple estimate)
        """
        target = "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYYY"
        
        if len(cube.state) != 54 or len(target) != 54:
            return 0
        
        misplaced = sum(1 for i in range(54) if cube.state[i] != target[i])
        return max(0, misplaced // 8)
    
    def solve(self, cube: Cube) -> Tuple[List[str], int]:
        """Solve cube using IDA* algorithm.
        
        Args:
            cube: Cube to solve
            
        Returns:
            Tuple of (moves list, nodes explored)
        """
        self.nodes_explored = 0
        
        # Check if already solved
        if cube.is_solved():
            return [], 0
        
        # IDA* with depth limits
        depth_limit = 1
        max_depth = 20  # Maximum depth to search
        
        while depth_limit <= max_depth:
            result = self._search(cube.copy(), [], 0, depth_limit)
            
            if result is not None:
                return result, self.nodes_explored
            
            depth_limit += 1
        
        return [], self.nodes_explored
    
    def _search(
        self, 
        cube: Cube, 
        moves: List[str], 
        current_depth: int, 
        depth_limit: int
    ) -> Optional[Tuple[List[str], int]]:
        """Recursive search function.
        
        Args:
            cube: Current cube state
            moves: Moves applied so far
            current_depth: Current depth in search tree
            depth_limit: Maximum depth for this iteration
            
        Returns:
            Solution moves if found, None otherwise
        """
        self.nodes_explored += 1
        
        # Check if solved
        if cube.is_solved():
            return moves, self.nodes_explored
        
        # Check depth limit
        if current_depth >= depth_limit:
            return None
        
        # Try all possible moves
        all_moves = [
            "U", "U'", "U2",
            "D", "D'", "D2",
            "L", "L'", "L2",
            "R", "R'", "R2",
            "F", "F'", "F2",
            "B", "B'", "B2"
        ]
        
        for move in all_moves:
            # Skip reverse of last move (avoid oscillation)
            if moves and self._is_reverse(moves[-1], move):
                continue
            
            # Make move
            cube_copy = cube.copy()
            cmd = MoveCommand(cube_copy)
            cmd.execute(move)
            
            # Calculate heuristic
            h_value = self.heuristic(cube_copy)
            f_value = current_depth + 1 + h_value
            
            # Prune if exceeds depth limit
            if f_value <= depth_limit:
                result = self._search(
                    cube_copy,
                    moves + [move],
                    current_depth + 1,
                    depth_limit
                )
                
                if result is not None:
                    return result
        
        return None
    
    @staticmethod
    def _is_reverse(move1: str, move2: str) -> bool:
        """Check if two moves are reverses of each other.
        
        Args:
            move1: First move
            move2: Second move
            
        Returns:
            True if moves are reverses
        """
        # Remove modifiers and get base move
        base1 = move1[0]
        base2 = move2[0]
        
        if base1 != base2:
            return False
        
        # Check if one is inverse of the other
        has_prime1 = "'" in move1
        has_prime2 = "'" in move2
        has_2_1 = "2" in move1
        has_2_2 = "2" in move2
        
        # X and X' are reverses
        if has_prime1 != has_prime2 and not has_2_1 and not has_2_2:
            return True
        
        return False
