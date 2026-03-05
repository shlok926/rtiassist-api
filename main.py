import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.rti import router as rti_router
from routes.legal import router as legal_router
from models.schemas import HealthResponse

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
WEBHOOK_PATH = "/telegram"
_telegram_app = None


async def _setup_telegram():
    global _telegram_app
    if not TELEGRAM_TOKEN:
        return
    try:
        from telegram.ext import (
            Application, CommandHandler, MessageHandler,
            filters, CallbackQueryHandler
        )
        from telegram_bot import (
            start, help_cmd, about, fee, state_cmd, legal_cmd,
            button_callback, handle_message
        )
        _telegram_app = Application.builder().token(TELEGRAM_TOKEN).updater(None).build()
        _telegram_app.add_handler(CommandHandler("start", start))
        _telegram_app.add_handler(CommandHandler("help", help_cmd))
        _telegram_app.add_handler(CommandHandler("about", about))
        _telegram_app.add_handler(CommandHandler("fee", fee))
        _telegram_app.add_handler(CommandHandler("state", state_cmd))
        _telegram_app.add_handler(CommandHandler("legal", legal_cmd))
        _telegram_app.add_handler(CallbackQueryHandler(button_callback))
        _telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        await _telegram_app.initialize()
        await _telegram_app.start()

        space_host = os.getenv("SPACE_HOST", "")
        if space_host:
            webhook_url = f"https://{space_host}{WEBHOOK_PATH}"
        else:
            webhook_url = os.getenv("WEBHOOK_URL", "")

        if webhook_url:
            await _telegram_app.bot.set_webhook(url=webhook_url, drop_pending_updates=True)
            logger.info(f"Telegram webhook set: {webhook_url}")
        else:
            logger.warning("WEBHOOK_URL not configured — bot inactive")
    except Exception as e:
        logger.error(f"Telegram setup failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await _setup_telegram()
    yield
    if _telegram_app:
        await _telegram_app.stop()
        await _telegram_app.shutdown()


app = FastAPI(
    lifespan=lifespan,
    title="RTIAssist API",
    description="""
## 🏛️ RTIAssist API — AI-Powered RTI Application Generator for Indian Citizens

Free and open-source tool built to help Indian citizens exercise their RTI rights.

### What it does
Accepts a citizen's plain-language description of what government information they need,
and returns a **complete, legally correct RTI application** ready to file — in seconds.

### 4-Layer AI Reasoning Pipeline
1. **Intent Classifier** — Identifies the correct department, ministry, urgency level
2. **PIO Resolver** — Finds the correct Public Information Officer and filing details
3. **Draft Generator** — Generates a formal RTI application under Section 6(1) of RTI Act 2005
4. **Quality Checker** — Reviews for completeness, exemption risks, and legal compliance

### Key Features
- Supports Central Government and all State Governments
- Hindi and English language output
- Urgency detection (routine / urgent / life-threatening with 48-hour response)
- Section 8 exemption risk detection
- Quality score out of 100 with improvement suggestions
- Auto-generated filing instructions

### Built For
Indian citizens to access government information easily and exercise their democratic rights
    """,
    version="1.0.0",
    contact={
        "name": "RTIAssist API",
        "url": "https://github.com/yourusername/rtiassist-api",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS — allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(rti_router)
app.include_router(legal_router)


@app.get("/", response_model=HealthResponse, tags=["Health"])
def root():
    return HealthResponse(
        status="✅ RTIAssist API is running",
        version="1.0.0",
        model="asi1-mini",
        endpoints=[
            "POST /rti/generate — Generate a complete RTI application",
            "GET /docs — Interactive API documentation (Swagger UI)",
            "GET /redoc — Alternative API documentation",
        ],
    )


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}


@app.post("/telegram", include_in_schema=False)
async def telegram_webhook(request: Request):
    """Receive updates from Telegram (webhook mode)."""
    if not _telegram_app:
        return Response(status_code=200)
    from telegram import Update
    data = await request.json()
    update = Update.de_json(data, _telegram_app.bot)
    await _telegram_app.process_update(update)
    return Response(status_code=200)
