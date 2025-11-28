"""
Wrapper for the fast Kociemba solver (optional).
Gracefully falls back to IDA* if kociemba package is not installed.
"""

from typing import Tuple, Optional
from cube.cube import Cube
from cube.moves import MoveCommand
from .solver_interface import Solver
from .ida_solver import IDASolver


class KociembaWrapper(Solver):
    """
    Wrapper for the Kociemba two-phase algorithm.
    
    If kociemba package is available, uses it for fast solving.
    Otherwise, falls back to IDA* solver.
    
    Kociemba typically solves any cube in ≤ 20 moves and is much faster than IDA*.
    """
    
    def __init__(self, fallback_to_ida: bool = True) -> None:
        """
        Initialize Kociemba wrapper.
        
        Args:
            fallback_to_ida (bool): If True, use IDA* if kociemba unavailable.
        """
        super().__init__()
        self.fallback_to_ida = fallback_to_ida
        self.kociemba_available = False
        self.backup_solver: Optional[IDASolver] = None
        
        try:
            import kociemba
            self.kociemba = kociemba
            self.kociemba_available = True
        except ImportError:
            if fallback_to_ida:
                self.backup_solver = IDASolver(heuristic="misplaced")
            self.kociemba = None
    
    def _cube_to_kociemba_string(self, cube: Cube) -> str:
        """
        Convert 54-char cube state to Kociemba format (URFDLB).
        
        Kociemba expects a 54-char string in order: U R F D L B
        Our internal format is: W(U) O(L) G(F) R(R) B(B) Y(D)
        
        We need to reorder: W O G R B Y -> U R F D L B
        
        Args:
            cube (Cube): The cube to convert.
        
        Returns:
            str: 54-char string in Kociemba format.
        """
        # Map our indices to Kociemba indices
        # Our: W(0-8) O(9-17) G(18-26) R(27-35) B(36-44) Y(45-53)
        # Koc: U(0-8) R(9-17) F(18-26) D(27-35) L(36-44) B(45-53)
        
        mapping = {
            'W': 0,  # Up
            'R': 1,  # Right
            'G': 2,  # Front
            'Y': 3,  # Down
            'O': 4,  # Left
            'B': 5,  # Back
        }
        
        face_order = [
            (0, 'W'),   # U face
            (3, 'R'),   # R face
            (2, 'G'),   # F face
            (5, 'Y'),   # D face
            (1, 'O'),   # L face
            (4, 'B'),   # B face
        ]
        
        result = []
        for face_idx, expected_color in face_order:
            result.append(cube.get_face(face_idx))
        
        return ''.join(result)
    
    def _kociemba_string_to_cube(self, state: str) -> Cube:
        """Convert Kociemba format back to our 54-char format."""
        # Koc: U R F D L B
        # Our: W O G R B Y
        
        k_u = state[0:9]   # U face
        k_r = state[9:18]  # R face
        k_f = state[18:27] # F face
        k_d = state[27:36] # D face
        k_l = state[36:45] # L face
        k_b = state[45:54] # B face
        
        # Reconstruct to our format
        return Cube(k_u + k_l + k_f + k_r + k_b + k_d)
    
    def solve(self, cube: Cube) -> Tuple[list[str], int]:
        """
        Solve using Kociemba algorithm (or fallback to IDA*).
        
        Args:
            cube (Cube): The cube to solve.
        
        Returns:
            Tuple[list[str], int]: (list of moves, nodes explored)
        
        Raises:
            RuntimeError: If no solver available.
        """
        if cube.is_solved():
            return [], 1
        
        if self.kociemba_available:
            try:
                koc_state = self._cube_to_kociemba_string(cube)
                solution = self.kociemba.solve(koc_state)
                
                if solution:
                    moves = solution.split()
                    # Normalize move names
                    normalized_moves: list[str] = []
                    for move in moves:
                        if move.endswith('\''):
                            normalized_moves.append(move)
                        elif move.endswith('2'):
                            normalized_moves.append(move)
                        else:
                            normalized_moves.append(move)
                    return normalized_moves, 1
                else:
                    return [], 1
            except Exception as e:
                if self.fallback_to_ida and self.backup_solver:
                    print(f"Kociemba failed: {e}. Falling back to IDA*...")
                    return self.backup_solver.solve(cube)
                raise
        
        if self.fallback_to_ida and self.backup_solver:
            return self.backup_solver.solve(cube)
        
        raise RuntimeError(
            "Kociemba not available and fallback disabled. "
            "Install kociemba: pip install kociemba"
        )
