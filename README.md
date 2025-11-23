# Ball Bouncing Game

A multi-platform ball bouncing game with both Python and Android implementations.

## Project Structure

```
ball-bouncing-game/
├── python/           # Python implementation using Pygame
│   ├── bouncing_ball.py              # Main game file
│   ├── bouncing_ball_debug.py        # Debug version
│   ├── bouncing_ball_original_backup.py  # Original backup
│   ├── test_ball_position.py         # Position tests
│   └── test_game_fixes.py            # Game fixes tests
└── android/          # Android implementation (Aishooty)
    ├── Aishooty/     # Main Android app
    ├── app/          # App module
    └── build files   # Gradle configuration
```

## Python Version

The Python version is built using Pygame and includes:
- Main game implementation
- Debug mode for testing
- Test suites for validation

### Running the Python Game

```bash
cd python
python bouncing_ball.py
```

## Android Version (Aishooty)

The Android version is built using native Android development tools.

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