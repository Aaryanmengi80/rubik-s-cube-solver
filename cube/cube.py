"""
Core Cube class representing the state of a Rubik's Cube.

The cube state is represented as a 54-character string:
  - Characters 0-8:   White face (face 0)
  - Characters 9-17:  Orange face (face 1)
  - Characters 18-26: Green face (face 2)
  - Characters 27-35: Red face (face 3)
  - Characters 36-44: Blue face (face 4)
  - Characters 45-53: Yellow face (face 5)

Each face is indexed as:
  0 1 2
  3 4 5
  6 7 8

Example:
    WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYY
"""

from typing import Any

class Cube:
    """
    Represents the state of a Rubik's Cube using a 54-character string.
    
    Attributes:
        state (str): 54-character string representing the cube state.
    """
    
    # Face indices
    WHITE, ORANGE, GREEN, RED, BLUE, YELLOW = range(6)
    
    def __init__(self, state: str | None = None) -> None:
        """
        Initialize a Cube with a given state or a solved state.
        
        Args:
            state (str, optional): 54-character string. Defaults to solved state.
        
        Raises:
            ValueError: If state length is not 54 or contains invalid characters.
        """
        if state is None:
                self.state = "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY"
        else:
            if len(state) != 54:
                raise ValueError(f"State must be 54 characters, got {len(state)}")
            # Validate that state only contains valid colors
            valid_colors = set("WOGRYB")
            if not all(c in valid_colors for c in state):
                raise ValueError(f"Invalid characters in state. Must be W, O, G, R, Y, B")
            self.state = state
    
    def __str__(self) -> str:
        """Return the 54-character state string."""
        return self.state
    
    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"Cube({self.state[:10]}...)"
    
    def __eq__(self, other: Any) -> bool:
        """Check equality based on state."""
        if not isinstance(other, Cube):
            return False
        return self.state == other.state
    
    def copy(self) -> "Cube":
        """Return a deep copy of this cube."""
        return Cube(self.state)
    
    def is_solved(self) -> bool:
        """
        Check if the cube is in a solved state.
        
        Returns:
            bool: True if all faces are uniform color.
        """
        target = "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY"
        return self.state == target
    
    def get_face(self, face_idx: int) -> str:
        """
        Get the 9-character string representing a face.
        
        Args:
            face_idx (int): Face index (0-5).
        
        Returns:
            str: 9-character face state.
        """
        start = face_idx * 9
        return self.state[start:start + 9]
    
    def set_face(self, face_idx: int, face_state: str) -> None:
        """
        Set the state of a face.
        
        Args:
            face_idx (int): Face index (0-5).
            face_state (str): 9-character string for the face.
        """
        if len(face_state) != 9:
            raise ValueError(f"Face state must be 9 characters, got {len(face_state)}")
        start = face_idx * 9
        self.state = self.state[:start] + face_state + self.state[start + 9:]
    
    def rotate_face_clockwise(self, face_idx: int) -> None:
        """
        Rotate a face 90 degrees clockwise.
        
        Args:
            face_idx (int): Face index (0-5).
        """
        face = self.get_face(face_idx)
        # Rotate: 0->2, 1->5, 2->8, 3->1, 4->4, 5->7, 6->0, 7->3, 8->6
        rotated = (face[6] + face[3] + face[0] +
                   face[7] + face[4] + face[1] +
                   face[8] + face[5] + face[2])
        self.set_face(face_idx, rotated)
    
    def rotate_face_counterclockwise(self, face_idx: int) -> None:
        """
        Rotate a face 90 degrees counterclockwise.
        
        Args:
            face_idx (int): Face index (0-5).
        """
        face = self.get_face(face_idx)
        # Rotate: 0->6, 1->3, 2->0, 3->7, 4->4, 5->1, 6->8, 7->5, 8->2
        rotated = (face[2] + face[5] + face[8] +
                   face[1] + face[4] + face[7] +
                   face[0] + face[3] + face[6])
        self.set_face(face_idx, rotated)
    
    def rotate_face_180(self, face_idx: int) -> None:
        """
        Rotate a face 180 degrees.
        
        Args:
            face_idx (int): Face index (0-5).
        """
        self.rotate_face_clockwise(face_idx)
        self.rotate_face_clockwise(face_idx)
    
    def move_U(self) -> None:
        """Apply Up move (clockwise when looking from top)."""
        # Rotate white face
        self.rotate_face_clockwise(self.WHITE)
        
        # Rotate edge pieces: Front -> Left -> Back -> Right -> Front
        top_row_indices = (0, 1, 2)
        
        front = [self.state[18 + i] for i in top_row_indices]
        left = [self.state[9 + i] for i in top_row_indices]
        back = [self.state[36 + i] for i in top_row_indices]
        right = [self.state[27 + i] for i in top_row_indices]
        
        # Rotate: Front <- Right, Left <- Front, Back <- Left, Right <- Back
        new_state = list(self.state)
        for i, idx in enumerate(top_row_indices):
            new_state[18 + idx] = right[i]  # Front gets Right
            new_state[9 + idx] = front[i]   # Left gets Front
            new_state[36 + idx] = left[i]   # Back gets Left
            new_state[27 + idx] = back[i]   # Right gets Back
        self.state = ''.join(new_state)
    
    def move_U_prime(self) -> None:
        """Apply U' move (counterclockwise when looking from top)."""
        self.move_U()
        self.move_U()
        self.move_U()
    
    def move_U2(self) -> None:
        """Apply U2 move (180 degrees)."""
        self.move_U()
        self.move_U()
    
    def move_D(self) -> None:
        """Apply Down move (clockwise when looking from bottom)."""
        self.rotate_face_clockwise(self.YELLOW)
        
        bottom_row_indices = (6, 7, 8)
        
        front = [self.state[18 + i] for i in bottom_row_indices]
        left = [self.state[9 + i] for i in bottom_row_indices]
        back = [self.state[36 + i] for i in bottom_row_indices]
        right = [self.state[27 + i] for i in bottom_row_indices]
        
        new_state = list(self.state)
        for i, idx in enumerate(bottom_row_indices):
            new_state[18 + idx] = left[i]   # Front gets Left
            new_state[9 + idx] = back[i]    # Left gets Back
            new_state[36 + idx] = right[i]  # Back gets Right
            new_state[27 + idx] = front[i]  # Right gets Front
        self.state = ''.join(new_state)
    
    def move_D_prime(self) -> None:
        """Apply D' move."""
        self.move_D()
        self.move_D()
        self.move_D()
    
    def move_D2(self) -> None:
        """Apply D2 move."""
        self.move_D()
        self.move_D()
    
    def move_R(self) -> None:
        """Apply Right move (clockwise when looking from right)."""
        self.rotate_face_clockwise(self.RED)
        
        right_col_indices = (2, 5, 8)
        
        front = [self.state[18 + i] for i in right_col_indices]
        up = [self.state[0 + i] for i in right_col_indices]
        back = [self.state[36 + i] for i in right_col_indices]
        down = [self.state[45 + i] for i in right_col_indices]
        
        new_state = list(self.state)
        for i, idx in enumerate(right_col_indices):
            new_state[18 + idx] = down[i]   # Front gets Down
            new_state[0 + idx] = front[i]   # Up gets Front
            new_state[36 + idx] = up[i]     # Back gets Up
            new_state[45 + idx] = back[i]   # Down gets Back
        self.state = ''.join(new_state)
    
    def move_R_prime(self) -> None:
        """Apply R' move."""
        self.move_R()
        self.move_R()
        self.move_R()
    
    def move_R2(self) -> None:
        """Apply R2 move."""
        self.move_R()
        self.move_R()
    
    def move_L(self) -> None:
        """Apply Left move (clockwise when looking from left)."""
        self.rotate_face_clockwise(self.ORANGE)
        
        left_col_indices = (0, 3, 6)
        
        front = [self.state[18 + i] for i in left_col_indices]
        up = [self.state[0 + i] for i in left_col_indices]
        back = [self.state[36 + i] for i in left_col_indices]
        down = [self.state[45 + i] for i in left_col_indices]
        
        new_state = list(self.state)
        for i, idx in enumerate(left_col_indices):
            new_state[18 + idx] = up[i]     # Front gets Up
            new_state[0 + idx] = back[i]    # Up gets Back
            new_state[36 + idx] = down[i]   # Back gets Down
            new_state[45 + idx] = front[i]  # Down gets Front
        self.state = ''.join(new_state)
    
    def move_L_prime(self) -> None:
        """Apply L' move."""
        self.move_L()
        self.move_L()
        self.move_L()
    
    def move_L2(self) -> None:
        """Apply L2 move."""
        self.move_L()
        self.move_L()
    
    def move_F(self) -> None:
        """Apply Front move (clockwise when looking from front)."""
        self.rotate_face_clockwise(self.GREEN)
        
        front_indices = (6, 7, 8)
        
        up = [self.state[0 + i] for i in front_indices]
        right = [self.state[27 + i] for i in front_indices]
        down = [self.state[45 + i] for i in [2, 1, 0]]  # Reversed
        left = [self.state[9 + i] for i in [8, 5, 2]]  # Reversed
        
        new_state = list(self.state)
        for i, idx in enumerate(front_indices):
            new_state[0 + idx] = left[i]
            new_state[27 + idx] = up[i]
            new_state[45 + [2, 1, 0][i]] = right[i]
            new_state[9 + [8, 5, 2][i]] = down[i]
        self.state = ''.join(new_state)
    
    def move_F_prime(self) -> None:
        """Apply F' move."""
        self.move_F()
        self.move_F()
        self.move_F()
    
    def move_F2(self) -> None:
        """Apply F2 move."""
        self.move_F()
        self.move_F()
    
    def move_B(self) -> None:
        """Apply Back move (clockwise when looking from back)."""
        self.rotate_face_clockwise(self.BLUE)
        
        back_indices = (0, 1, 2)
        
        up = [self.state[0 + i] for i in [0, 3, 6]]  # Left column of up
        left = [self.state[9 + i] for i in back_indices]
        down = [self.state[45 + i] for i in [8, 5, 2]]  # Right column of down, reversed
        right = [self.state[27 + i] for i in [6, 3, 0]]  # Left column of right, reversed
        
        new_state = list(self.state)
        for i, idx in enumerate(back_indices):
            new_state[0 + [0, 3, 6][i]] = right[i]
            new_state[9 + idx] = up[i]
            new_state[45 + [8, 5, 2][i]] = left[i]
            new_state[27 + [6, 3, 0][i]] = down[i]
        self.state = ''.join(new_state)
    
    def move_B_prime(self) -> None:
        """Apply B' move."""
        self.move_B()
        self.move_B()
        self.move_B()
    
    def move_B2(self) -> None:
        """Apply B2 move."""
        self.move_B()
        self.move_B()
