#!/bin/bash
# Railway startup script - Handles initialization before starting server

echo "🚀 Starting TrafficBot Pro Backend..."

# 1. Install Playwright browsers
echo "📦 Installing Playwright browsers..."
python -m playwright install chromium --with-deps || echo "⚠️ Warning: Playwright install failed, continuing..."

# 2. Initialize database
echo "🗄️ Initializing database..."
python init_database.py || echo "⚠️ Warning: Database init failed, continuing..."

# 3. Start the FastAPI server
echo "✅ Starting API server..."
PORT=${PORT:-8000}
python -m api.server
