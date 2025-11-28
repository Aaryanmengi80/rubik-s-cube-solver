"""
Flask web UI for Rubik's Cube Solver.
Serves a simple interface to visualize cube solutions.
"""

import json
from pathlib import Path
from flask import Flask, render_template, jsonify, send_from_directory  # type: ignore

app = Flask(__name__, template_folder='templates')

# Path to solution JSON
SOLUTION_FILE = Path(__file__).parent.parent / 'solution.json'


@app.route('/')
def index():
    """Serve the main UI page."""
    return render_template('index.html')


@app.route('/api/solution')
def get_solution():
    """
    API endpoint to get the current solution.
    
    Returns:
        JSON: Solution data from solution.json
    """
    if SOLUTION_FILE.exists():
        with open(SOLUTION_FILE, 'r') as f:
            return jsonify(json.load(f))
    else:
        return jsonify({
            'error': 'No solution found. Run solver first.',
            'moves': [],
            'num_moves': 0
        }), 404


@app.route('/api/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    print("Starting Rubik's Cube Solver UI...")
    print("Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
