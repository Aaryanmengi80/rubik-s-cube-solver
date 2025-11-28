"""
Flask web application for Rubik's Cube solver visualization.
"""

import json
from pathlib import Path
from typing import Any, Dict, Tuple, Union
import os
from flask import Flask, render_template, jsonify, request  # type: ignore

# Get the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(basedir, 'templates')
static_dir = os.path.join(basedir, 'static')

# Create Flask app with correct template and static folders
app: Flask = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
)
app.config["JSON_SORT_KEYS"] = False


@app.route("/")  # type: ignore
def index() -> str:
    """Render the main index page.
    
    Returns:
        str: Rendered HTML template
    """
    return render_template("index.html")


@app.route("/api/solution")  # type: ignore
def get_solution() -> Union[Dict[str, Any], Tuple[Dict[str, Any], int]]:
    """Get the latest solution from solution.json file.
    
    Returns:
        Union[Dict, Tuple]: Solution data or error response with 404 status
    """
    solution_file = Path("solution.json")
    if not solution_file.exists():
        return jsonify({"error": "No solution found"}), 404
    
    try:
        with open(solution_file, "r") as f:
            data: Dict[str, Any] = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/solve", methods=["POST"])  # type: ignore
def solve_cube() -> Union[Dict[str, Any], Tuple[Dict[str, Any], int]]:
    """Solve a cube and return the solution.
    
    Returns:
        Union[Dict, Tuple]: Solution data or error response
    """
    try:
        data: Dict[str, Any] = request.get_json()
        
        if not data or "state" not in data:
            return jsonify({"error": "Missing cube state"}), 400
        
        cube_state = data.get("state", "").strip()
        
        # Validate input
        if len(cube_state) != 54:
            return jsonify({
                "error": f"Invalid cube state length: {len(cube_state)}. Expected 54 characters."
            }), 400
        
        valid_chars = set(['W', 'O', 'G', 'R', 'B', 'Y'])
        for char in cube_state:
            if char not in valid_chars:
                return jsonify({
                    "error": f"Invalid character: {char}. Use only W, O, G, R, B, Y"
                }), 400
        
        # Import solver
        from solvers.ida_solver import IDASolver
        from cube.cube import Cube
        
        # Create and solve cube
        cube = Cube(cube_state)
        solver = IDASolver(heuristic="misplaced")
        moves, nodes = solver.solve(cube)
        
        # Prepare response
        response = {
            "state": cube_state,
            "moves": moves,
            "move_count": len(moves),
            "nodes_explored": nodes,
            "algorithm": "IDA*"
        }
        
        return jsonify(response), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid cube state: {str(e)}"}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.errorhandler(404)  # type: ignore
def not_found(error: Any) -> Tuple[Dict[str, str], int]:
    """Handle 404 errors.
    
    Args:
        error: The error object
        
    Returns:
        JSON error response with 404 status
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)  # type: ignore
def server_error(error: Any) -> Tuple[Dict[str, str], int]:
    """Handle 500 errors.
    
    Args:
        error: The error object
        
    Returns:
        JSON error response with 500 status
    """
    return jsonify({"error": "Server error"}), 500


if __name__ == "__main__":  # type: ignore
    print("Starting Rubik's Cube Solver Web UI...")
    print("Visit: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
