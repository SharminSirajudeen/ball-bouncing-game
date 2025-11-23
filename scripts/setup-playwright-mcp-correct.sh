#!/bin/bash

# Claude Code Playwright MCP Setup Script (Corrected Version)
# This script properly installs and configures Playwright MCP for visual development workflows

echo "🚀 Setting up Playwright MCP for Claude Code (Corrected)..."
echo "================================================"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ npm found"

# Method 1: Using npx (Recommended for Claude Code)
echo ""
echo "📦 Setting up Playwright MCP Server..."
echo "We'll use the executeautomation version which is actively maintained."
echo ""

# Install Playwright if not already installed
echo "Installing Playwright test package..."
npm install --save-dev @playwright/test

# Install the browsers
echo ""
echo "🌐 Installing Playwright browsers (if needed)..."
npx playwright install chromium

# Create the MCP configuration
echo ""
echo "📝 Creating MCP configuration..."

CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Creating new Claude Code config..."
    mkdir -p "$HOME/Library/Application Support/Claude"
    cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "-y",
        "@executeautomation/playwright-mcp-server"
      ]
    }
  }
}
EOF
    echo "✅ Created Claude Code config with Playwright MCP"
else
    echo "⚠️  Claude Code config exists. Please manually add this to your mcpServers section:"
    echo ""
    echo "Location: $CONFIG_FILE"
    echo ""
    cat << 'EOF'
"playwright": {
  "command": "npx",
  "args": [
    "-y",
    "@executeautomation/playwright-mcp-server"
  ]
}
EOF
    echo ""
    echo "Alternative (Microsoft version):"
    cat << 'EOF'
"playwright": {
  "command": "npx",
  "args": [
    "@playwright/mcp@latest"
  ]
}
EOF
fi

# Create a package.json if it doesn't exist
if [ ! -f "package.json" ]; then
    echo ""
    echo "📄 Creating package.json..."
    cat > package.json << 'EOF'
{
  "name": "playwright-mcp-project",
  "version": "1.0.0",
  "description": "Playwright MCP integration for Claude Code",
  "scripts": {
    "test": "playwright test"
  },
  "devDependencies": {
    "@playwright/test": "^1.56.0"
  }
}
EOF
fi

# Create a test HTML file for verification
echo ""
echo "🧪 Creating test file for verification..."
cat > test-playwright-visual.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Playwright MCP Visual Test</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            width: 100%;
        }

        .hero-card {
            background: white;
            padding: 3rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-bottom: 2rem;
        }

        .logo {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: pulse 2s ease-in-out infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        h1 {
            color: #1a202c;
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: 800;
        }

        .subtitle {
            color: #718096;
            font-size: 1.25rem;
            margin-bottom: 2rem;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 20px rgba(0, 0, 0, 0.15);
        }

        .feature-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .feature-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.5rem;
        }

        .feature-description {
            color: #718096;
            font-size: 0.875rem;
        }

        .button-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }

        .btn {
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }

        .btn-secondary:hover {
            background: #f7fafc;
        }

        .console {
            background: #1a202c;
            color: #68d391;
            padding: 1rem;
            border-radius: 8px;
            font-family: 'Monaco', 'Courier New', monospace;
            text-align: left;
            margin-top: 2rem;
            max-height: 200px;
            overflow-y: auto;
        }

        .console-line {
            margin: 4px 0;
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }

        @keyframes fadeIn {
            to { opacity: 1; }
        }

        /* Responsive Design Test Elements */
        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            .hero-card { padding: 2rem; }
            .feature-grid { grid-template-columns: 1fr; }
        }

        /* Accessibility Test Elements */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0,0,0,0);
            border: 0;
        }

        /* Focus indicators for keyboard navigation */
        *:focus {
            outline: 3px solid #667eea;
            outline-offset: 2px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="hero-card">
            <div class="logo">🎨</div>
            <h1>Playwright MCP Visual Testing</h1>
            <p class="subtitle">Your visual development workflow is ready for testing!</p>

            <div class="button-group">
                <button class="btn btn-primary" onclick="testInteraction()">
                    <span>✨</span> Test Interaction
                </button>
                <button class="btn btn-secondary" onclick="toggleTheme()">
                    <span>🌙</span> Toggle Theme
                </button>
                <button class="btn btn-primary" onclick="showConsole()">
                    <span>📊</span> Show Metrics
                </button>
            </div>
        </div>

        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">📸</div>
                <div class="feature-title">Visual Screenshots</div>
                <div class="feature-description">Capture and analyze UI states automatically</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔄</div>
                <div class="feature-title">Iterative Design</div>
                <div class="feature-description">AI-powered improvements through visual feedback</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <div class="feature-title">Responsive Testing</div>
                <div class="feature-description">Test across all device sizes automatically</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">♿</div>
                <div class="feature-title">Accessibility</div>
                <div class="feature-description">WCAG compliance and screen reader support</div>
            </div>
        </div>

        <div id="console" class="console" style="display: none;">
            <div class="console-line">$ Playwright MCP connected ✓</div>
            <div class="console-line" style="animation-delay: 0.2s">$ Visual debugging enabled ✓</div>
            <div class="console-line" style="animation-delay: 0.4s">$ Screenshot capability: Active</div>
            <div class="console-line" style="animation-delay: 0.6s">$ Browser automation: Ready</div>
            <div class="console-line" style="animation-delay: 0.8s">$ Performance metrics: 60fps</div>
        </div>
    </div>

    <script>
        function testInteraction() {
            alert('✅ Playwright can interact with this button!\n\nThe visual debugging agent can now:\n• Take screenshots\n• Analyze layouts\n• Test interactions\n• Verify designs');
        }

        function toggleTheme() {
            document.body.style.background = document.body.style.background.includes('667eea')
                ? 'linear-gradient(135deg, #1a202c 0%, #2d3748 100%)'
                : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }

        function showConsole() {
            const console = document.getElementById('console');
            console.style.display = console.style.display === 'none' ? 'block' : 'none';
        }

        // Log for Playwright to detect
        console.log('Playwright MCP Test Page Loaded');
        console.log('Ready for visual debugging');
    </script>
</body>
</html>
EOF

echo "✅ Test file created: test-playwright-visual.html"

# Create a simple test script
echo ""
echo "📝 Creating test script..."
cat > test-playwright.js << 'EOF'
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  // Navigate to test page
  await page.goto('file://' + process.cwd() + '/test-playwright-visual.html');

  // Take screenshot
  await page.screenshot({ path: 'playwright-test-screenshot.png' });

  console.log('✅ Screenshot saved as playwright-test-screenshot.png');

  // Test interaction
  await page.click('button:has-text("Test Interaction")');

  // Wait a bit to see the result
  await page.waitForTimeout(3000);

  await browser.close();
})();
EOF

# Summary
echo ""
echo "================================================"
echo "✨ Setup Complete!"
echo "================================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣  Restart Claude Code to load the Playwright MCP"
echo ""
echo "2️⃣  Test the integration by saying:"
echo '   "Use playwright mcp to open test-playwright-visual.html and take a screenshot"'
echo ""
echo "3️⃣  Or use the slash commands:"
echo "   /visual-check       - Take screenshot and analyze"
echo "   /responsive-test    - Test across devices"
echo "   /design-review      - Full UI/UX review"
echo "   /iterate-design     - Iterative improvements"
echo "   /a11y-audit        - Accessibility check"
echo ""
echo "🤖 Available Agents:"
echo "   @agent-visual-debugger"
echo "   @agent-ui-reviewer"
echo "   @agent-cross-platform-ui-builder"
echo ""
echo "📚 Resources:"
echo "   Documentation: CLAUDE.md"
echo "   Design Guide: .claude/context/design-principles.md"
echo "   Style Guide: .claude/context/style-guide.md"
echo "   All Commands: .claude/commands/"
echo ""
echo "💡 Pro Tip: Always explicitly mention 'playwright mcp' in your first"
echo "   request to ensure Claude uses the MCP instead of bash commands."
echo ""
echo "🎨 Happy visual development! Your AI now has eyes! 👀"