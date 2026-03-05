#!/bin/bash
# RTIAssist Startup Script — Hugging Face Spaces
# Bot runs in webhook mode — no separate process needed

echo "=== RTIAssist Starting ==="
echo "[INFO] Starting API + Telegram webhook on port 7860..."
python app.py
