#!/usr/bin/env python3
"""
🎯 BIRD SHOOTER GAME 🦅

A fun physics-based bird shooting game with multiple bird rendering modes!

FEATURES:
- 3 Bird Modes: Emoji 🦅, Sprites 🖼️, or Geometric shapes
- Slingshot mechanics for shooting
- Mario-style pixelated background
- Score tracking and high scores
- Colorful bouncing balls

CONTROLS:
- Drag any ball to aim and shoot
- B - Switch between bird modes
- R - Reset game
- Space - Pause
- Shift+Click - Add more balls
- ESC/Q - Quit

OBJECTIVE:
Shoot as many flying birds as you can using the slingshot!
Each bird hit = 1 point. Try to beat your high score!
"""

import subprocess
import sys

def main():
    print(__doc__)
    print("\n" + "="*50)
    print("Starting Bird Shooter Game...")
    print("="*50 + "\n")
    
    try:
        # Run the game
        subprocess.run([sys.executable, "bouncing_ball.py"])
    except KeyboardInterrupt:
        print("\nGame terminated by user")
    except Exception as e:
        print(f"Error running game: {e}")
        print("\nMake sure pygame is installed:")
        print("  pip install pygame")

if __name__ == "__main__":
    main()