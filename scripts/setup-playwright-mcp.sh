#!/bin/bash

# Claude Code Playwright MCP Setup Script
# This script installs and configures Playwright MCP for visual development workflows

echo "🚀 Setting up Playwright MCP for Claude Code..."
echo "================================================"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install Node.js first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ npm found"

# Install Playwright MCP
echo ""
echo "📦 Installing Playwright MCP..."
npm install -g @modelcontextprotocol/server-playwright

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
npx playwright install chromium firefox webkit

# Check if Claude Code config exists
CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  Claude Code config not found. Creating new config..."
    mkdir -p "$HOME/Library/Application Support/Claude"
    cat > "$CONFIG_FILE" << 'EOF'
{
  "mcpServers": {
    "playwright": {
      "command": "node",
      "args": [
        "/usr/local/lib/node_modules/@modelcontextprotocol/server-playwright/dist/index.js"
      ],
      "env": {
        "PLAYWRIGHT_BROWSER": "chromium",
        "PLAYWRIGHT_HEADLESS": "false"
      }
    }
  }
}
EOF
    echo "✅ Created new Claude Code config with Playwright MCP"
else
    echo "📝 Claude Code config found. Please manually add Playwright MCP:"
    echo ""
    echo "Add this to your mcpServers section in:"
    echo "$CONFIG_FILE"
    echo ""
    cat << 'EOF'
"playwright": {
  "command": "node",
  "args": [
    "/usr/local/lib/node_modules/@modelcontextprotocol/server-playwright/dist/index.js"
  ],
  "env": {
    "PLAYWRIGHT_BROWSER": "chromium",
    "PLAYWRIGHT_HEADLESS": "false"
  }
}
EOF
fi

# Create a test HTML file for verification
echo ""
echo "🧪 Creating test file for verification..."
cat > test-playwright.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Playwright MCP Test</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .card {
            background: white;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
        }
        h1 {
            color: #333;
            margin-bottom: 1rem;
        }
        .success {
            color: #10b981;
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        button {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-size: 1rem;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: #2563eb;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="success">✅</div>
        <h1>Playwright MCP Ready!</h1>
        <p>Your visual development workflow is set up.</p>
        <button onclick="alert('Playwright can interact with this!')">Test Interaction</button>
    </div>
</body>
</html>
EOF

echo "✅ Test file created: test-playwright.html"

# Summary
echo ""
echo "================================================"
echo "✨ Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Restart Claude Code to load the Playwright MCP"
echo "2. Test with: /visual-check"
echo "3. Open test-playwright.html in your browser to verify"
echo ""
echo "Available commands:"
echo "  /visual-check       - Take screenshot and analyze"
echo "  /responsive-test    - Test across devices"
echo "  /design-review      - Full UI/UX review"
echo "  /iterate-design     - Iterative improvements"
echo "  /a11y-audit        - Accessibility check"
echo ""
echo "Agents:"
echo "  @agent-visual-debugger"
echo "  @agent-ui-reviewer"
echo "  @agent-cross-platform-ui-builder"
echo ""
echo "📚 Documentation: .claude/CLAUDE.md"
echo "🎨 Design Principles: .claude/context/design-principles.md"
echo "🎭 Style Guide: .claude/context/style-guide.md"
echo ""
echo "Happy designing! 🚀"