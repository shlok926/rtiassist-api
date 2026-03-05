#!/bin/bash
# RTIAssist Startup Script — Hugging Face Spaces
# Starts both the FastAPI server and Telegram bot

echo "=== RTIAssist Starting ==="

# Start Telegram bot in background if token is set
if [ -n "$TELEGRAM_TOKEN" ] && [ "$TELEGRAM_TOKEN" != "your_token_here" ]; then
    echo "[INFO] Starting Telegram bot..."
    python telegram_bot.py &
    BOT_PID=$!
    echo "[INFO] Telegram bot started (PID $BOT_PID)"
else
    echo "[INFO] TELEGRAM_TOKEN not set — bot not started"
fi

# Start FastAPI server (keeps HF Space alive)
echo "[INFO] Starting API server on port 7860..."
python app.py
