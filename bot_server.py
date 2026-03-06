"""
RTIAssist — Telegram Bot Webhook Server
Deploy on Render (free tier) — webhook mode, no polling needed.
"""

import os
import logging
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler
)

# Import all handlers from main bot file
from telegram_bot import (
    start, help_cmd, about, fee, state_cmd, legal_cmd,
    button_callback, handle_message, myreminders_cmd, TELEGRAM_TOKEN, API_BASE
)

load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set after Render deployment, e.g. https://your-app.onrender.com/telegram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Build telegram application (shared instance)
telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()

# Register all handlers
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("help", help_cmd))
telegram_app.add_handler(CommandHandler("about", about))
telegram_app.add_handler(CommandHandler("fee", fee))
telegram_app.add_handler(CommandHandler("state", state_cmd))
telegram_app.add_handler(CommandHandler("legal", legal_cmd))
telegram_app.add_handler(CommandHandler("myreminders", myreminders_cmd))
telegram_app.add_handler(CallbackQueryHandler(button_callback))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize bot and set webhook on startup."""
    await telegram_app.initialize()
    await telegram_app.start()
    if WEBHOOK_URL:
        await telegram_app.bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True
        )
        logger.info(f"✅ Webhook set: {WEBHOOK_URL}")
    else:
        logger.warning("⚠️  WEBHOOK_URL not set — bot won't receive updates until set!")
    yield
    # Cleanup on shutdown
    await telegram_app.stop()
    await telegram_app.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health():
    """Health check — keeps Render service awake (ping from UptimeRobot)."""
    return {"status": "ok", "service": "RTIAssist Bot", "mode": "webhook"}


@app.post("/telegram")
async def telegram_webhook(request: Request):
    """Receive updates from Telegram."""
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return Response(status_code=200)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    logger.info(f"🤖 RTIAssist Bot webhook server starting on port {port}")
    logger.info(f"🔗 API: {API_BASE}")
    uvicorn.run(app, host="0.0.0.0", port=port)
