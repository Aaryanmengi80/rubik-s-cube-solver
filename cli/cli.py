"""
Command-line interface for the Rubik's Cube solver.
Accepts a 54-character cube state, selects a solver, and outputs the solution.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from cube.cube import Cube
from solvers.bfs_solver import BFSSolver
from solvers.ida_solver import IDASolver
from solvers.kociemba_wrapper import KociembaWrapper


def load_cube_from_file(filepath: str) -> Cube:
    """
    Load cube state from a JSON file.
    
    Expected JSON format:
    {
        "state": "WWWWWWWWW..."
    }
    
    Args:
        filepath (str): Path to the JSON file.
    
    Returns:
        Cube: The loaded cube.
    
    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If JSON format is invalid.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    if 'state' not in data:
        raise ValueError("JSON must contain 'state' key")
    
    return Cube(data['state'])


def save_solution(moves: list[str], nodes_explored: int, output_file: str) -> None:
    """
    Save solution to a JSON file.
    
    Args:
        moves (list[str]): List of move names.
        nodes_explored (int): Number of nodes explored by solver.
        output_file (str): Output file path.
    """
    solution: dict[str, int | list[str] | str] = {
        "moves": moves,
        "num_moves": len(moves),
        "nodes_explored": nodes_explored,
        "solution_string": " ".join(moves) if moves else "Cube already solved"
    }
    
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w') as f:
        json.dump(solution, f, indent=2)
    
    print(f"Solution saved to {output_file}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Rubik's Cube Solver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Solve a cube from command line
  python cli.py -s "WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYY"
  
  # Solve from a JSON file
  python cli.py -f input.json
  
  # Use IDA* solver with wrong_face heuristic
  python cli.py -s "RWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYY" \\
                -m ida --heuristic wrong_face
        """
    )
    
    # Input arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-s', '--state',
        type=str,
        help='54-character cube state string'
    )
    input_group.add_argument(
        '-f', '--file',
        type=str,
        help='JSON file containing cube state'
    )
    
    # Solver selection
    parser.add_argument(
        '-m', '--method',
        choices=['bfs', 'ida', 'kociemba'],
        default='ida',
        help='Solving method (default: ida)'
    )
    
    # IDA* specific options
    parser.add_argument(
        '--heuristic',
        choices=['misplaced', 'wrong_face'],
        default='misplaced',
        help='Heuristic for IDA* solver (default: misplaced)'
    )
    
    # Output
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='solution.json',
        help='Output JSON file (default: solution.json)'
    )
    
    # Verbosity
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Load cube state
    try:
        if args.state:
            cube = Cube(args.state)
            if args.verbose:
                print(f"Loaded cube state: {args.state[:20]}...")
        else:
            cube = load_cube_from_file(args.file)
            if args.verbose:
                print(f"Loaded cube from file: {args.file}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading cube: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Check if already solved
    if cube.is_solved():
        print("Cube is already solved!")
        save_solution([], 1, args.output)
        return
    
    # Select solver
    try:
        if args.method == 'bfs':
            solver = BFSSolver()
            if args.verbose:
                print("Using BFS solver...")
        elif args.method == 'ida':
            solver = IDASolver(heuristic=args.heuristic)
            if args.verbose:
                print(f"Using IDA* solver with '{args.heuristic}' heuristic...")
        else:  # kociemba
            solver = KociembaWrapper(fallback_to_ida=True)
            if args.verbose:
                print("Using Kociemba solver (with IDA* fallback)...")
    except Exception as e:
        print(f"Error initializing solver: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Solve
    try:
        if args.verbose:
            print("Solving...")
        moves, nodes_explored = solver.solve(cube)
        
        if args.verbose:
            print(f"Solution found: {len(moves)} moves")
            print(f"Nodes explored: {nodes_explored}")
            print(f"Moves: {' '.join(moves)}")
        else:
            print(f"Solution: {' '.join(moves) if moves else 'Cube already solved'}")
            print(f"Moves: {len(moves)}")
        
        # Save solution
        save_solution(moves, nodes_explored, args.output)
    
    except Exception as e:
        print(f"Error solving cube: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
