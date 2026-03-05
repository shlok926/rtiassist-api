"""
RTIAssist API — Hugging Face Spaces Entry Point
This file is the main entry point for Hugging Face deployment.
"""

import os
import subprocess
import sys
from main import app

# Set demo mode as default for Hugging Face deployment
os.environ.setdefault("DEMO_MODE", "true")

def start_telegram_bot():
    """Start telegram bot as background subprocess if token is set."""
    token = os.getenv("TELEGRAM_TOKEN", "")
    if not token or token == "your_token_here":
        print("[INFO] TELEGRAM_TOKEN not set — bot not started.")
        return None
    print("[INFO] Starting Telegram bot...")
    proc = subprocess.Popen(
        [sys.executable, "telegram_bot.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    print(f"[INFO] Telegram bot started (PID {proc.pid})")
    return proc

# The app is already created in main.py, just import and use it
if __name__ == "__main__":
    import uvicorn
    # Start bot in background if TELEGRAM_TOKEN is set
    start_telegram_bot()
    port = int(os.getenv("PORT", 7860))  # Hugging Face uses port 7860
    uvicorn.run(app, host="0.0.0.0", port=port)
