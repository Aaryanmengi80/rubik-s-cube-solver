#!/bin/bash
# Setup script for Rubik's Cube Solver project
# Runs on both Windows PowerShell and bash

echo "🎲 Rubik's Cube Solver - Setup Script"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python --version
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv
echo ""

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "Activating venv for Windows..."
    source venv/Scripts/activate
else
    echo "Activating venv for Unix..."
    source venv/bin/activate
fi
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Run tests
echo "Running tests..."
python -m pytest tests/ -v
echo ""

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate venv: source venv/bin/activate (Unix) or venv\\Scripts\\activate (Windows)"
echo "2. Run solver: python cli/cli.py -s \"RWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYY\" -m ida"
echo "3. Start UI: python ui/app.py"
echo "4. Benchmark: python tools/benchmark.py --solvers ida --depths 5 8"
