#!/bin/sh
# Railway startup script - Simplified for reliability

echo "🚀 Starting TrafficBot Pro Backend..."

# 1. Initialize database (if init_database.py exists)
if [ -f "init_database.py" ]; then
    echo "🗄️ Initializing database..."
    python init_database.py 2>&1 || echo "⚠️ Warning: Database init failed, API may initialize it on first request"
fi

# 2. Start the FastAPI server with environment variables
echo "✅ Starting API server on PORT=${PORT:-8000}..."
exec python -m api.server
