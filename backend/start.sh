#!/bin/bash
# Railway startup script

echo "🚀 Starting TrafficBot Pro Backend..."

# Initialize database
echo "🗄️ Initializing database..."
python init_database.py

# Start server with uvicorn
echo "✅ Starting API server on PORT=${PORT:-8080}..."
exec uvicorn api.server:app --host 0.0.0.0 --port ${PORT:-8080}
