"""
Basic solver tests.
Verifies that solvers correctly solve simple scrambles.
"""

import pytest  # type: ignore
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cube.cube import Cube
from cube.moves import MoveCommand
from solvers.ida_solver import IDASolver
from solvers.bfs_solver import BFSSolver


class TestSolverInterface:
    """Test solver interface compliance."""
    
    def test_ida_solver_exists(self) -> None:
        """Test that IDA* solver can be instantiated."""
        solver = IDASolver()
        assert solver is not None
        assert solver.name == 'IDASolver'
    
    def test_bfs_solver_exists(self) -> None:
        """Test that BFS solver can be instantiated."""
        solver = BFSSolver()
        assert solver is not None


class TestSolverOutput:
    """Test that solvers return proper output format."""
    
    def test_ida_returns_tuple(self) -> None:
        """Test IDA* returns (moves, nodes_explored)."""
        solver = IDASolver()
        cube = Cube()  # Already solved
        
        moves, nodes = solver.solve(cube)
        
        assert isinstance(moves, list)
        assert isinstance(nodes, int)
    
    def test_bfs_returns_tuple(self) -> None:
        """Test BFS returns (moves, nodes_explored)."""
        solver = BFSSolver()
        cube = Cube()  # Already solved
        
        moves, nodes = solver.solve(cube)
        
        assert isinstance(moves, list)
        assert isinstance(nodes, int)


class TestSolverBasicCases:
    """Test solvers on simple cases."""
    
    def test_ida_solves_solved_cube(self) -> None:
        """Test IDA* recognizes a solved cube."""
        solver = IDASolver()
        cube = Cube()
        
        moves, _ = solver.solve(cube)  # type: ignore
        
        assert len(moves) == 0
    
    def test_bfs_solves_solved_cube(self) -> None:
        """Test BFS recognizes a solved cube."""
        solver = BFSSolver()
        cube = Cube()
        
        moves, _ = solver.solve(cube)  # type: ignore
        
        assert len(moves) == 0
    
    def test_ida_solves_one_move_scramble(self) -> None:
        """Test IDA* solves a cube scrambled by one move."""
        solver = IDASolver()
        cube = Cube()
        
        # Scramble with one move
        cube.move_U()
        
        moves, _ = solver.solve(cube)  # type: ignore
        
        # Should find solution with at least 1 move
        assert len(moves) >= 1
        
        # Verify solution is correct
        test_cube = Cube()
        test_cube.move_U()
        cmd = MoveCommand(test_cube)
        for move in moves:
            cmd.execute(move)
        assert test_cube.is_solved()
    
    def test_ida_solves_two_move_scramble(self) -> None:
        """Test IDA* solves a two-move scramble."""
        solver = IDASolver()
        cube = Cube()
        
        # Scramble with two moves
        cube.move_U()
        cube.move_R()
        
        moves, _ = solver.solve(cube)  # type: ignore
        
        # Verify solution
        test_cube = Cube()
        test_cube.move_U()
        test_cube.move_R()
        cmd = MoveCommand(test_cube)
        for move in moves:
            cmd.execute(move)
        assert test_cube.is_solved()
    
    def test_ida_solves_known_pattern(self) -> None:
        """Test IDA* solves a known simple pattern."""
        solver = IDASolver()
        cube = Cube()
        
        # Apply a known pattern: R U R' U'
        pattern = ['R', 'U', 'R\'', 'U\'']
        cmd = MoveCommand(cube)
        for move in pattern:
            cmd.execute(move)
        
        # Should solve it
        moves, _ = solver.solve(cube)  # type: ignore
        
        # Apply solution and verify
        cmd2 = MoveCommand(cube)
        for move in moves:
            cmd2.execute(move)
        assert cube.is_solved()


class TestSolverDifferentHeuristics:
    """Test IDA* with different heuristics."""
    
    def test_misplaced_heuristic(self) -> None:
        """Test IDA* with misplaced heuristic."""
        solver = IDASolver(heuristic='misplaced')
        cube = Cube()
        cube.move_U()
        cube.move_R()
        
        moves, nodes = solver.solve(cube)
        
        # Should find a solution
        assert len(moves) > 0
        assert nodes > 0
    
    def test_wrong_face_heuristic(self) -> None:
        """Test IDA* with wrong_face heuristic."""
        solver = IDASolver(heuristic='wrong_face')
        cube = Cube()
        cube.move_U()
        cube.move_R()
        
        moves, nodes = solver.solve(cube)
        
        # Should find a solution
        assert len(moves) > 0
        assert nodes > 0
    
    def test_invalid_heuristic_raises(self) -> None:
        """Test that invalid heuristic raises error."""
        with pytest.raises(ValueError):  # type: ignore
            IDASolver(heuristic='invalid')


if __name__ == '__main__':  # type: ignore
    pytest.main([__file__, '-v'])