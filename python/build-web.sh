#!/bin/bash
# Build script for web deployment with Pygbag

set -e

echo "🎮 Building Ricochet Hunter for Web Deployment..."
echo "================================================"

# Check if pygbag is installed
if ! command -v pygbag &> /dev/null; then
    echo "❌ Pygbag not found. Installing..."
    pip install pygbag>=0.8.7
fi

# Clean previous build
if [ -d "build" ]; then
    echo "🧹 Cleaning previous build..."
    rm -rf build
fi

# Build with pygbag
echo "🔨 Building with Pygbag..."
python -m pygbag \
    --build \
    --app_name "Ricochet Hunter" \
    .

echo ""
echo "✅ Build complete!"
echo "================================================"
echo "📂 Output directory: build/web"
echo ""
echo "To test locally:"
echo "  cd build/web && python -m http.server 8000"
echo "  Then open: http://localhost:8000"
echo ""
echo "To deploy to GitHub Pages:"
echo "  1. Commit and push the build/web directory"
echo "  2. Enable GitHub Pages in repository settings"
echo "  3. Point it to the /python/build/web directory"
echo "================================================"
