# Ball Bouncing & Bird Shooting Games

A multi-platform game project featuring a combined Ball Bouncing and Bird Shooting game in Python, plus an Android bird shooting game called Aishooty.

## Project Structure

```
ball-bouncing-game/
├── python/           # Python implementation using Pygame
│   ├── assets/       # Game assets
│   │   ├── bird_sprite.png           # Bird sprite (right-facing)
│   │   └── bird_sprite_left.png      # Bird sprite (left-facing)
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
- Multiple bird rendering modes:
  - Emoji mode (🦅)
  - Sprite mode (using custom brown bird sprites)
  - Geometric shapes mode
- Custom bird sprites with directional variants (left/right facing)
- High score tracking
- Debug mode for testing
- Test suites for validation
- **Web deployment support** via Pygbag (play in browser!)

### Running the Python Game

**Desktop Version:**
```bash
cd python
# Run directly
python bouncing_ball.py

# Or use the launcher
python run_bird_shooter.py
```

**Web Version (Play in Browser):**

The game can be played directly in your web browser! Visit the deployed version at:
🎮 **[Play Ricochet Hunter Online](https://SharminSirajudeen.github.io/ball-bouncing-game/)**

### Game Controls
- **Drag any ball** - Aim and shoot
- **B** - Switch between bird modes
- **R** - Reset game
- **Space** - Pause
- **Shift+Click** - Add more balls
- **ESC/Q** - Quit

## 🌐 Web Deployment

This game can be deployed to the web using **Pygbag**, which converts Pygame games to run in browsers via WebAssembly.

### Automatic Deployment (GitHub Pages)

The repository is configured for automatic deployment:

1. **Push to main/master branch** - The game will automatically build and deploy
2. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Set Source to "GitHub Actions"
   - The game will be available at: `https://[username].github.io/ball-bouncing-game/`

### Manual Build

To build the web version locally:

```bash
cd python

# Install pygbag
pip install pygbag>=0.8.7

# Build the game
./build-web.sh

# Or manually:
python -m pygbag --build --app_name "Ricochet Hunter" .
```

Test locally:
```bash
cd build/web
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

### Deployment Options

1. **GitHub Pages** (Recommended) - Free, automatic deployment
2. **Itch.io** - Upload the `build/web` folder
3. **Netlify/Vercel** - Deploy as a static site
4. **Your own web server** - Host the `build/web` directory

### Web Version Features

✅ Runs directly in modern browsers (Chrome, Firefox, Safari, Edge)
✅ No installation required
✅ Full game functionality
✅ Touch controls support (mobile-friendly)
✅ Automatic updates when you push changes
✅ Beautiful loading screen with progress indicators

**Note:** Initial loading may take 30-90 seconds on mobile devices due to WebAssembly compilation. The loading screen shows progress and helpful tips while you wait!

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