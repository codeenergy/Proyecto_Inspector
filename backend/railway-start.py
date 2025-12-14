#!/usr/bin/env python3
"""Railway startup script - respects PORT environment variable"""
import os
import subprocess
import sys

# Get port from environment or default to 8080
port = os.environ.get("PORT", "8080")

print(f"🚀 Starting TrafficBot Pro Backend on port {port}...")

# Start uvicorn
subprocess.run([
    "python", "-m", "uvicorn",
    "api.server:app",
    "--host", "0.0.0.0",
    "--port", port
], check=True)
