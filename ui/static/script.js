/**
 * Rubik's Cube Solver - Advanced Frontend
 */

// Templates
const TEMPLATES = {
    solved: 'WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYYY',
    oneMove: 'WWWWWWOWWOOROOOOOYGGGGGGGGRRRRRRRRBBBRBBBBBYYYYYYYYRY',
    twoMoves: 'WOWWWWWWWOYGOOOOOOGGRGGGGGYRRRRRRGBRBBBBRYBYYBYYYYYYY'
};

let currentSolution = null;

async function solveCube() {
    const cubeState = document.getElementById('cubeState').value.trim();
    
    // Validation
    if (!validateCubeState(cubeState)) {
        return;
    }
    
    // Hide welcome card
    document.getElementById('welcome').classList.add('hidden');
    
    // Show loading
    hideError();
    hideResult();
    showLoading();
    
    try {
        const response = await fetch('/api/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ state: cubeState })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            showError(data.error || 'Failed to solve cube');
            hideLoading();
            return;
        }
        
        // Store solution
        currentSolution = data;
        
        // Display results
        displayResult(data);
        hideLoading();
        
    } catch (error) {
        console.error('Fetch error:', error);
        showError(`Error: ${error.message}`);
        hideLoading();
    }
}

function validateCubeState(state) {
    if (!state) {
        showError('Please enter a cube state');
        return false;
    }
    
    if (state.length !== 54) {
        showError(`Invalid cube state length: ${state.length}. Expected 54 characters.`);
        return false;
    }
    
    const validChars = ['W', 'O', 'G', 'R', 'B', 'Y'];
    for (let char of state) {
        if (!validChars.includes(char)) {
            showError(`Invalid character: '${char}'. Use only W, O, G, R, B, Y`);
            return false;
        }
    }
    
    return true;
}

function displayResult(data) {
    document.getElementById('moveCount').textContent = data.move_count;
    document.getElementById('algorithm').textContent = data.algorithm;
    document.getElementById('nodesExplored').textContent = data.nodes_explored.toLocaleString();
    document.getElementById('moveSequence').textContent = 
        data.moves.length > 0 ? data.moves.join(' ') : 'Already solved!';
    
    // Visualize cube
    visualizeCubeState(data.state);
    
    showResult();
}

function visualizeCubeState(state) {
    const vis = document.getElementById('cubeVisualization');
    vis.innerHTML = '';
    
    // Create face representations
    const faces = {
        'Top': state.slice(0, 9),
        'Front': state.slice(18, 27),
        'Right': state.slice(27, 36),
        'Left': state.slice(9, 18),
        'Back': state.slice(36, 45),
        'Bottom': state.slice(45, 54)
    };
    
    for (const [faceName, colors] of Object.entries(faces)) {
        const faceDiv = document.createElement('div');
        faceDiv.className = 'cube-face';
        faceDiv.innerHTML = `<div class="face-name">${faceName}</div>`;
        
        const grid = document.createElement('div');
        grid.className = 'face-grid';
        
        for (let i = 0; i < 9; i++) {
            const tile = document.createElement('div');
            tile.className = `face-tile ${getColorClass(colors[i])}`;
            grid.appendChild(tile);
        }
        
        faceDiv.appendChild(grid);
        vis.appendChild(faceDiv);
    }
}

function getColorClass(char) {
    const colorMap = {
        'W': 'white',
        'O': 'orange',
        'G': 'green',
        'R': 'red',
        'B': 'blue',
        'Y': 'yellow'
    };
    return colorMap[char] || 'white';
}

function resetForm() {
    document.getElementById('cubeState').value = '';
    hideResult();
    hideError();
    hideLoading();
    document.getElementById('welcome').classList.remove('hidden');
    document.getElementById('cubeState').focus();
}

function generateRandom() {
    const chars = ['W', 'O', 'G', 'R', 'B', 'Y'];
    let state = '';
    
    // Create 9 of each color (54 total)
    for (let i = 0; i < 6; i++) {
        for (let j = 0; j < 9; j++) {
            state += chars[i];
        }
    }
    
    // Shuffle the state
    state = state.split('').sort(() => 0.5 - Math.random()).join('');
    
    document.getElementById('cubeState').value = state;
    document.getElementById('cubeState').focus();
}

function loadSolved() {
    document.getElementById('cubeState').value = TEMPLATES.solved;
    document.getElementById('cubeState').focus();
}

function loadSingleMove() {
    document.getElementById('cubeState').value = TEMPLATES.oneMove;
    document.getElementById('cubeState').focus();
}

function loadTwoMoves() {
    document.getElementById('cubeState').value = TEMPLATES.twoMoves;
    document.getElementById('cubeState').focus();
}

function copyMoves() {
    if (!currentSolution || !currentSolution.moves || currentSolution.moves.length === 0) {
        showNotification('No moves to copy');
        return;
    }
    
    const moves = currentSolution.moves.join(' ');
    navigator.clipboard.writeText(moves).then(() => {
        showNotification('✓ Moves copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showNotification('Failed to copy');
    });
}

function showNotification(message) {
    const notif = document.createElement('div');
    notif.className = 'notification';
    notif.textContent = message;
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.classList.add('fadeOut');
        setTimeout(() => notif.remove(), 300);
    }, 2500);
}

function showError(message) {
    const error = document.getElementById('error');
    document.getElementById('errorMessage').textContent = message;
    error.classList.remove('hidden');
    
    // Scroll to error
    setTimeout(() => {
        error.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function showResult() {
    document.getElementById('result').classList.remove('hidden');
    
    // Scroll to result
    setTimeout(() => {
        document.getElementById('result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);
}

function hideResult() {
    document.getElementById('result').classList.add('hidden');
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

// Event listeners
window.addEventListener('load', function() {
    const textarea = document.getElementById('cubeState');
    if (textarea) {
        textarea.focus();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Allow Ctrl+Enter to solve
    const textarea = document.getElementById('cubeState');
    if (textarea) {
        textarea.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                solveCube();
            }
        });
    }
});

// Add notification styles dynamically
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #4caf50, #45a049);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        animation: slideIn 0.3s ease;
        z-index: 1000;
        font-weight: 600;
    }
    
    .notification.fadeOut {
        animation: slideOut 0.3s ease forwards;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .cube-face {
        background: white;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .face-name {
        text-align: center;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 8px;
        font-size: 0.9em;
    }
    
    .face-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 5px;
    }
    
    .face-tile {
        width: 35px;
        height: 35px;
        border-radius: 4px;
        border: 1px solid #ddd;
    }
    
    .face-tile.white { background: white; }
    .face-tile.orange { background: #ff9800; }
    .face-tile.green { background: #4caf50; }
    .face-tile.red { background: #f44336; }
    .face-tile.blue { background: #2196f3; }
    .face-tile.yellow { background: #ffeb3b; }
`;
document.head.appendChild(style);