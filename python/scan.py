"""
OpenCV-based color scanner for Rubik's Cube.
Reads 6 images (one per face) and detects cube colors, outputting a 54-character state.
"""

import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

if TYPE_CHECKING:
    import cv2
    import numpy as np

try:
    import cv2
    import numpy as np
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False  # type: ignore


class CubeScanner:
    """
    OpenCV-based scanner for Rubik's Cube faces.
    Detects sticker colors from images.
    """
    
    # Define color ranges in HSV (easier for color detection)
    COLOR_RANGES = {
        'W': ((0, 0, 200), (180, 30, 255)),        # White
        'Y': ((15, 100, 200), (35, 255, 255)),     # Yellow
        'O': ((5, 100, 200), (15, 255, 255)),      # Orange
        'R': ((0, 100, 200), (10, 255, 255)),      # Red
        'G': ((35, 100, 200), (85, 255, 255)),     # Green
        'B': ((100, 100, 200), (130, 255, 255)),   # Blue
    }
    
    def __init__(self) -> None:
        """Initialize the scanner."""
        if not HAS_OPENCV:
            raise RuntimeError(
                "OpenCV not available. Install with: pip install opencv-python"
            )
    
    def detect_color(self, image: "np.ndarray", region: tuple[int, int, int, int]) -> str:  # type: ignore
        """
        Detect the dominant color in an image region.
        
        Args:
            image (np.ndarray): Image in BGR format.
            region (tuple[int, int, int, int]): ROI as (x, y, width, height).
        
        Returns:
            str: Detected color code (W, O, G, R, B, Y) or '?' if unknown.
        """
        x, y, w, h = region
        roi = image[y:y+h, x:x+w]
        
        # Convert BGR to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Try to match colors
        best_match = None
        best_score = 0
        
        for color, (lower, upper) in self.COLOR_RANGES.items():
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)
            
            mask = cv2.inRange(hsv, lower, upper)
            score = cv2.countNonZero(mask)
            
            if score > best_score:
                best_score = score
                best_match = color
        
        return best_match if best_match else '?'
    
    def scan_face(self, image_path: str) -> Optional[str]:
        """
        Scan a single cube face image.
        
        Expects a 3x3 grid of stickers. Detects each and returns 9-char string.
        
        Args:
            image_path (str): Path to the image file.
        
        Returns:
            Optional[str]: 9-character string of colors, or None if scan failed.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Error: Could not read image {image_path}")
                return None
            
            h, w = image.shape[:2]
            sticker_size = min(h, w) // 3
            
            colors = []
            for row in range(3):
                for col in range(3):
                    x = col * sticker_size
                    y = row * sticker_size
                    color = self.detect_color(image, (x, y, sticker_size, sticker_size))
                    colors.append(color)
            
            return ''.join(colors)
        
        except Exception as e:
            print(f"Error scanning {image_path}: {e}")
            return None
    
    def scan_all_faces(self, image_dir: str) -> Optional[str]:
        """
        Scan all 6 faces from a directory.
        
        Expects files: U.jpg, O.jpg, G.jpg, R.jpg, B.jpg, Y.jpg
        (or .png, .jpg, .jpeg)
        
        Args:
            image_dir (str): Directory containing face images.
        
        Returns:
            Optional[str]: 54-character cube state, or None if any scan failed.
        """
        dir_path = Path(image_dir)
        if not dir_path.is_dir():
            print(f"Error: {image_dir} is not a directory")
            return None
        
        face_names = ['W', 'O', 'G', 'R', 'B', 'Y']
        state_parts = []
        
        for face in face_names:
            # Try different image extensions
            image_file = None
            for ext in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                candidate = dir_path / f"{face}{ext}"
                if candidate.exists():
                    image_file = str(candidate)
                    break
            
            if image_file is None:
                print(f"Error: Could not find image for face {face}")
                return None
            
            print(f"Scanning face {face}...", end=' ', flush=True)
            face_colors = self.scan_face(image_file)
            
            if face_colors is None:
                return None
            
            state_parts.append(face_colors)
            print(f"{face_colors}")
        
        return ''.join(state_parts)


def save_scan_result(state: str, faces: list[str], output_file: str) -> None:
    """
    Save scan result to JSON.
    
    Args:
        state (str): 54-character cube state.
        faces (list[str]): List of 9-char face strings.
        output_file (str): Output file path.
    """
    result: dict[str, object] = {
        'state': state,
        'faces': faces,
        'face_names': ['White', 'Orange', 'Green', 'Red', 'Blue', 'Yellow']
    }
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Scan result saved to {output_file}")


def main():
    """Main entry point for scanner script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Scan Rubik's Cube faces with OpenCV"
    )
    parser.add_argument(
        'image_dir',
        type=str,
        help='Directory containing cube face images (W.jpg, O.jpg, G.jpg, R.jpg, B.jpg, Y.jpg)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='scan_result.json',
        help='Output JSON file (default: scan_result.json)'
    )
    
    args = parser.parse_args()
    
    try:
        scanner = CubeScanner()
        print(f"Scanning cube faces from {args.image_dir}...")
        state = scanner.scan_all_faces(args.image_dir)
        
        if state:
            print(f"\nScanned state: {state}")
            faces = [state[i*9:(i+1)*9] for i in range(6)]
            save_scan_result(state, faces, args.output)
        else:
            print("Scan failed!")
            sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
