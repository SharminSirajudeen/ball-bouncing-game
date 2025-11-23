# Ball Bouncing & Bird Shooting Games

A multi-platform game project featuring a combined Ball Bouncing and Bird Shooting game in Python, plus an Android bird shooting game called Aishooty.

## Project Structure

```
ball-bouncing-game/
├── python/           # Python implementation using Pygame
│   ├── bouncing_ball.py              # Main game (combined ball bouncing + bird shooting)
│   ├── run_bird_shooter.py           # Game launcher script
│   ├── bird_hunter_highscore.txt     # High score storage
│   ├── bouncing_ball_debug.py        # Debug version
│   ├── bouncing_ball_original_backup.py  # Original backup
│   ├── test_ball_position.py         # Position tests
│   └── test_game_fixes.py            # Game fixes tests
├── android/          # Android implementations
│   ├── Aishooty/     # Bird shooting game
│   └── app/          # Ball bouncing game module
└── scripts/          # Setup and utility scripts
    ├── setup-playwright-mcp.sh       # Playwright MCP setup
    └── setup-playwright-mcp-correct.sh  # Corrected setup script
```

## Python Version

The Python version is a combined game built using Pygame that includes:
- **Ball Bouncing mechanics** with physics simulation
- **Bird Shooting game** with slingshot mechanics
- Multiple bird rendering modes (Emoji, Sprites, Geometric shapes)
- High score tracking
- Debug mode for testing
- Test suites for validation

### Running the Python Game

```bash
cd python
# Run directly
python bouncing_ball.py

# Or use the launcher
python run_bird_shooter.py
```

### Game Controls
- **Drag any ball** - Aim and shoot
- **B** - Switch between bird modes
- **R** - Reset game
- **Space** - Pause
- **Shift+Click** - Add more balls
- **ESC/Q** - Quit

## Android Version - Aishooty (Bird Shooting Game)

Aishooty is a bird shooting game built using native Android development tools. It's a companion game to the ball bouncing game, offering a different gameplay experience on Android devices.

### Building the Android App

```bash
cd android
./gradlew build
```

## Requirements

### Python
- Python 3.x
- Pygame

### Android
- Android Studio
- Gradle
- Android SDK

## Author

Sharmin Sirajudeen

## License

This project is proprietary and confidential.