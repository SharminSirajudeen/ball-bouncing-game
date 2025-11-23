# Ball Bouncing & Bird Shooting Game

A fun physics-based game combining ball bouncing mechanics with bird shooting gameplay!

## Requirements

- Python 3.6 or higher
- Pygame library

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Files Structure

- `bouncing_ball.py` - Main game file with all game logic
- `run_bird_shooter.py` - Launcher script with game description
- `bird_sprite.png` - Bird sprite (right-facing)
- `bird_sprite_left.png` - Bird sprite (left-facing)
- `bird_hunter_highscore.txt` - Stores the high score
- `bouncing_ball_debug.py` - Debug version for testing
- `test_*.py` - Test files for game validation

## How to Run

### Method 1: Direct execution
```bash
python3 bouncing_ball.py
```

### Method 2: Using the launcher (shows game description)
```bash
python3 run_bird_shooter.py
```

## Game Controls

- **Drag any ball** - Aim and shoot with slingshot mechanics
- **B** - Switch between bird rendering modes:
  - Emoji mode (🦅)
  - Sprite mode (custom bird images)
  - Geometric shapes mode
- **R** - Reset the game
- **Space** - Pause/Resume
- **Shift+Click** - Add more balls
- **ESC or Q** - Quit the game

## Game Features

### Ball Bouncing
- Realistic physics simulation
- Multiple colored balls
- Gravity and collision effects
- Wall bouncing mechanics

### Bird Shooting
- Flying birds as targets
- Slingshot aiming system
- Score tracking
- High score persistence
- Multiple bird rendering modes

## Scoring

- Each bird hit = 1 point
- Try to beat your high score!
- High score is automatically saved

## Troubleshooting

If you get an error about missing pygame:
```bash
pip install pygame
```

If sprites don't load, make sure these files are in the same directory as `bouncing_ball.py`:
- `bird_sprite.png`
- `bird_sprite_left.png`

## Development

- The main game logic is in `bouncing_ball.py`
- Debug mode available in `bouncing_ball_debug.py`
- Test files available for validation
- Sprite creation script in `assets/create_bird_sprite.py`