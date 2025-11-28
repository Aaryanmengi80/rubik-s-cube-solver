"""
Unit tests for the Cube class.
Tests cube state, rotations, and move applications.
"""

import pytest  # type: ignore
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cube.cube import Cube
from cube.moves import MoveCommand


class TestCubeBasics:
    """Test basic Cube functionality."""
    
    def test_cube_initialization_default(self) -> None:
        """Test default cube is solved."""
        cube = Cube()
        assert cube.is_solved()
        assert len(cube.state) == 54
    
    def test_cube_initialization_with_state(self) -> None:
        """Test cube initialization with custom state."""
        state = "RWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY"
        cube = Cube(state)
        assert cube.state == state
        assert not cube.is_solved()
    
    def test_cube_initialization_invalid_length(self) -> None:
        """Test cube rejects invalid state length."""
        with pytest.raises(ValueError):  # type: ignore
            Cube("WWWWWWWWW")
    
    def test_cube_initialization_invalid_chars(self) -> None:
        """Test cube rejects invalid characters."""
        invalid_state = "X" * 54
        with pytest.raises(ValueError):  # type: ignore
            Cube(invalid_state)
    
    def test_cube_copy(self) -> None:
        """Test cube copy is independent."""
        cube1 = Cube("RWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY")
        cube2 = cube1.copy()
        
        assert cube1.state == cube2.state
        assert cube1 is not cube2


class TestCubeRotations:
    """Test face rotations."""
    
    def test_rotate_face_clockwise(self) -> None:
        """Test clockwise face rotation."""
        cube = Cube()
        original = cube.get_face(0)  # White face
        
        cube.rotate_face_clockwise(0)
        rotated = cube.get_face(0)
        
        # After rotation: 0->2, 1->5, 2->8, 3->1, 4->4, 5->7, 6->0, 7->3, 8->6
        expected = (original[6] + original[3] + original[0] +
                    original[7] + original[4] + original[1] +
                    original[8] + original[5] + original[2])
        assert rotated == expected
    
    def test_rotate_face_counterclockwise_is_inverse(self) -> None:
        """Test that counterclockwise is the inverse of clockwise."""
        cube = Cube()
        original = cube.state
        
        cube.rotate_face_clockwise(0)
        cube.rotate_face_counterclockwise(0)
        
        assert cube.state == original
    
    def test_rotate_face_180_twice_is_identity(self) -> None:
        """Test that two 180-degree rotations restore original state."""
        cube = Cube()
        original = cube.state
        
        cube.rotate_face_180(0)
        cube.rotate_face_180(0)
        
        assert cube.state == original


class TestCubeMoves:
    """Test standard cube moves."""
    
    def test_move_U_cycle(self) -> None:
        """Test U move cycles through 4 top rows."""
        cube = Cube()
        original = cube.state
        
        # Apply U move 4 times should restore original
        for _ in range(4):
            cube.move_U()
        
        assert cube.state == original
    
    def test_move_U_prime_is_inverse(self) -> None:
        """Test U' is the inverse of U."""
        cube = Cube()
        original = cube.state
        
        cube.move_U()
        cube.move_U_prime()
        
        assert cube.state == original
    
    def test_move_U2_same_as_two_U(self) -> None:
        """Test U2 is equivalent to two U moves."""
        cube1 = Cube()
        cube2 = Cube()
        
        cube1.move_U2()
        cube2.move_U()
        cube2.move_U()
        
        assert cube1.state == cube2.state
    
    def test_all_moves_exist(self) -> None:
        """Test that all standard moves are implemented."""
        cube = Cube()
        cmd = MoveCommand(cube)
        
        moves = ['U', 'U\'', 'U2', 'D', 'D\'', 'D2',
                 'L', 'L\'', 'L2', 'R', 'R\'', 'R2',
                 'F', 'F\'', 'F2', 'B', 'B\'', 'B2']
        
        for move in moves:
            original = cube.state
            cmd.execute(move)
            assert cube.state != original or cube.is_solved()


class TestMoveCommand:
    """Test the MoveCommand command pattern."""
    
    def test_execute_single_move(self) -> None:
        """Test executing a single move."""
        cube = Cube()
        cmd = MoveCommand(cube)
        original = cube.state
        
        cmd.execute('U')
        assert cube.state != original
    
    def test_execute_sequence(self) -> None:
        """Test executing a move sequence."""
        cube = Cube()
        cmd = MoveCommand(cube)
        original = cube.state
        
        cmd.execute_sequence("U R U' R'")
        assert cube.state != original
        assert len(cmd.get_history()) == 4
    
    def test_undo_last_move(self) -> None:
        """Test undoing the last move."""
        cube = Cube()
        cmd = MoveCommand(cube)
        
        cmd.execute('U')
        _ = cube.state
        cmd.undo_last()
        
        assert cube.state == "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY"
    
    def test_undo_all_moves(self) -> None:
        """Test undoing all moves."""
        cube = Cube()
        cmd = MoveCommand(cube)
        
        cmd.execute_sequence("U R U' R' F2")
        cmd.undo_all()
        
        assert cube.is_solved()
        assert len(cmd.get_history()) == 0
    
    def test_get_solution_string(self) -> None:
        """Test getting solution as a string."""
        cube = Cube()
        cmd = MoveCommand(cube)
        
        cmd.execute_sequence("U R U' R'")
        solution = cmd.get_solution_string()
        
        assert solution == "U R U' R'"


class TestCubeEquality:
    """Test cube equality comparison."""
    
    def test_equal_cubes(self) -> None:
        """Test that identical cubes are equal."""
        state = "RWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY"
        cube1 = Cube(state)
        cube2 = Cube(state)
        
        assert cube1 == cube2
    
    def test_different_cubes_not_equal(self) -> None:
        """Test that different cubes are not equal."""
        cube1 = Cube("RWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY")
        cube2 = Cube("OWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY")
        
        assert cube1 != cube2


if __name__ == '__main__':  # type: ignore
    pytest.main([__file__, '-v'])