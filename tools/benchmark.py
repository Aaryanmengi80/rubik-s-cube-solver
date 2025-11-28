"""
Benchmark tool for testing solver performance.
Runs multiple scrambles and collects timing and move count statistics.
"""

import json
import time
import random
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from cube.cube import Cube
from cube.moves import MoveCommand
from solvers.bfs_solver import BFSSolver
from solvers.ida_solver import IDASolver
from solvers.kociemba_wrapper import KociembaWrapper


class BenchmarkRunner:
    """
    Benchmark runner for Rubik's Cube solvers.
    """
    
    ALL_MOVES = ['U', 'U\'', 'U2', 'D', 'D\'', 'D2',
                 'L', 'L\'', 'L2', 'R', 'R\'', 'R2',
                 'F', 'F\'', 'F2', 'B', 'B\'', 'B2']
    
    def __init__(self, seed: int = 42) -> None:
        """
        Initialize benchmark runner.
        
        Args:
            seed (int): Random seed for reproducibility.
        """
        self.seed = seed
        random.seed(seed)
    
    def generate_scramble(self, num_moves: int = 10) -> list[str]:
        """
        Generate a random scramble.
        
        Args:
            num_moves (int): Number of moves in scramble.
        
        Returns:
            list[str]: List of move names.
        """
        scramble: list[str] = []
        for _ in range(num_moves):
            scramble.append(random.choice(self.ALL_MOVES))
        return scramble
    
    def apply_scramble(self, cube: Cube, scramble: list[str]) -> None:
        """
        Apply a scramble to a cube.
        
        Args:
            cube (Cube): The cube to scramble.
            scramble (list[str]): List of moves.
        """
        cmd = MoveCommand(cube)
        for move in scramble:
            cmd.execute(move)
    
    def benchmark_solver(
        self,
        solver: Any,
        num_trials: int = 5,
        scramble_depth: int = 10
    ) -> dict[str, Any]:
        """
        Benchmark a single solver.
        
        Args:
            solver: The solver to benchmark.
            num_trials (int): Number of trials to run.
            scramble_depth (int): Number of moves in each scramble.
        
        Returns:
            dict[str, Any]: Benchmark results.
        """
        results: dict[str, Any] = {
            'solver': solver.__class__.__name__,
            'num_trials': num_trials,
            'scramble_depth': scramble_depth,
            'trials': []
        }
        
        for trial_idx in range(num_trials):
            print(f"  Trial {trial_idx + 1}/{num_trials}...", end=' ', flush=True)
            
            # Generate scramble
            scramble = self.generate_scramble(scramble_depth)
            cube = Cube()
            self.apply_scramble(cube, scramble)
            
            # Solve
            start_time = time.time()
            try:
                moves, nodes_explored = solver.solve(cube)
                elapsed = time.time() - start_time
                
                trial_result: dict[str, Any] = {
                    'scramble': scramble,
                    'num_moves': len(moves),
                    'time_seconds': elapsed,
                    'nodes_explored': nodes_explored,
                    'success': True
                }
                results['trials'].append(trial_result)
                print(f"{elapsed:.4f}s, {len(moves)} moves")
            except Exception as e:
                elapsed = time.time() - start_time
                trial_result = {
                    'scramble': scramble,
                    'error': str(e),
                    'time_seconds': elapsed,
                    'success': False
                }
                results['trials'].append(trial_result)
                print(f"FAILED: {e}")
        
        # Compute statistics
        successful_trials: list[Any] = [t for t in results['trials'] if t['success']]
        if successful_trials:
            times: list[Any] = [t['time_seconds'] for t in successful_trials]
            moves: list[Any] = [t['num_moves'] for t in successful_trials]
            
            results['stats'] = {
                'success_rate': len(successful_trials) / num_trials,
                'avg_time_seconds': sum(times) / len(times),
                'min_time_seconds': min(times),
                'max_time_seconds': max(times),
                'avg_solution_length': sum(moves) / len(moves),
                'min_solution_length': min(moves),
                'max_solution_length': max(moves),
            }
        else:
            results['stats'] = {'success_rate': 0}
        
        return results
    
    def run_benchmark_suite(
        self,
        solvers: list[Any],
        depths: list[int] | None = None,
        num_trials: int = 5,
        output_file: str = 'benchmark_results.json'
    ) -> None:
        """
        Run benchmark on multiple solvers and depths.
        
        Args:
            solvers (list[Any]): List of solver instances.
            depths (list[int]): Scramble depths to test. Defaults to [5, 8, 10].
            num_trials (int): Number of trials per configuration.
            output_file (str): Output JSON file.
        """
        if depths is None:
            depths = [5, 8, 10]
        
        all_results: dict[str, Any] = {
            'seed': self.seed,
            'configurations': []
        }
        
        for solver in solvers:
            for depth in depths:
                print(f"\nBenchmarking {solver.__class__.__name__} (depth={depth})...")
                result = self.benchmark_solver(solver, num_trials, depth)
                all_results['configurations'].append(result)
        
        # Save results
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\n✓ Benchmark complete. Results saved to {output_file}")
        self._print_summary(all_results)
    
    def _print_summary(self, results: dict[str, Any]) -> None:
        """Print a summary of benchmark results."""
        print("\n" + "=" * 70)
        print("BENCHMARK SUMMARY")
        print("=" * 70)
        
        for config in results['configurations']:
            solver_name = config['solver']
            depth = config['scramble_depth']
            stats = config.get('stats', {})
            
            print(f"\n{solver_name} (depth={depth}):")
            if stats.get('success_rate', 0) == 0:
                print("  Status: FAILED (no successful trials)")
            else:
                print(f"  Success rate: {stats['success_rate']:.1%}")
                print(f"  Avg time: {stats['avg_time_seconds']:.4f}s")
                print(f"  Avg solution length: {stats['avg_solution_length']:.1f} moves")


def main():
    """Main entry point for benchmark script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Benchmark Rubik's Cube solvers"
    )
    parser.add_argument(
        '-n', '--trials',
        type=int,
        default=3,
        help='Number of trials per configuration (default: 3)'
    )
    parser.add_argument(
        '-d', '--depths',
        type=int,
        nargs='+',
        default=[5, 8],
        help='Scramble depths to test (default: 5 8)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='benchmark_results.json',
        help='Output JSON file (default: benchmark_results.json)'
    )
    parser.add_argument(
        '--solvers',
        choices=['ida', 'bfs', 'kociemba', 'all'],
        default='ida',
        help='Which solvers to benchmark (default: ida)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility (default: 42)'
    )
    
    args = parser.parse_args()
    
    # Initialize solvers
    solvers_to_test: list[Any] = []
    if args.solvers in ['ida', 'all']:
        solvers_to_test.append(IDASolver(heuristic='misplaced'))
    if args.solvers in ['bfs', 'all']:
        solvers_to_test.append(BFSSolver())
    if args.solvers in ['kociemba', 'all']:
        solvers_to_test.append(KociembaWrapper(fallback_to_ida=True))
    
    # Run benchmark
    runner = BenchmarkRunner(seed=args.seed)
    runner.run_benchmark_suite(
        solvers_to_test,
        depths=args.depths,
        num_trials=args.trials,
        output_file=args.output
    )


if __name__ == '__main__':
    main()
