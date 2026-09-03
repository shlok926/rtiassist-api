import os
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uuid
import time
from routes.rti import router as rti_router
from routes.legal import router as legal_router
from routes.cases import router as cases_router
from routes.authorities import router as authorities_router
from routes.admin_authorities import router as admin_authorities_router
from routes.pdf_analysis import router as pdf_analysis_router
from routes.auth import router as auth_router
from models.schemas import HealthResponse
from models.database import engine, Base
import models.orm  # Load all models for Base.metadata.create_all

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DB for Phase 2 development (Temporary before Alembic)
from utils.config import ENVIRONMENT
if ENVIRONMENT != "production":
    Base.metadata.create_all(bind=engine)

ENVIRONMENT = os.getenv("ENVIRONMENT", "production").lower()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
WEBHOOK_PATH = "/telegram"
_telegram_app = None
_telegram_init_lock = asyncio.Lock()
_telegram_initialized = False


async def _build_telegram_app():
    from integrations.telegram import get_telegram_app
    app = get_telegram_app()
    if not app:
        return None
    # We must set updater to None manually if running in webhook mode, but it's done inside get_telegram_app
    return app


async def _get_telegram_app():
    """Lazy-initialize telegram app on first webhook call."""
    global _telegram_app, _telegram_initialized
    if _telegram_initialized:
        return _telegram_app
    async with _telegram_init_lock:
        if _telegram_initialized:
            return _telegram_app
        try:
            app = await _build_telegram_app()
            if not app:
                _telegram_initialized = True
                return None
            await app.initialize()
            await app.start()
            _telegram_app = app
            _telegram_initialized = True
            logger.info("✅ Telegram bot initialized successfully (lazy)")
            # Register webhook
            space_host = os.getenv("SPACE_HOST", "")
            webhook_url = f"https://{space_host}{WEBHOOK_PATH}" if space_host else os.getenv("WEBHOOK_URL", "")
            if webhook_url:
                await app.bot.set_webhook(url=webhook_url, drop_pending_updates=False)
                logger.info(f"Webhook set: {webhook_url}")
        except Exception as e:
            logger.error(f"Telegram lazy init failed: {e}")
            _telegram_initialized = False  # Allow retry next request
    return _telegram_app


_monitoring_task = None

async def _monitoring_loop():
    from models.database import SessionLocal
    from services.source_monitoring import SourceMonitoringService
    interval_sec = int(os.getenv("MONITORING_LOOP_INTERVAL_SECONDS", "3600"))
    
    logger.info(f"Source monitoring scheduler started. Checking every {interval_sec}s.")
    while True:
        try:
            db = SessionLocal()
            try:
                logger.info("Running scheduled source checks...")
                results = await SourceMonitoringService.run_due_checks(db)
                if results["processed"] > 0:
                    logger.info(f"Monitoring cycle complete: {results}")
            finally:
                db.close()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in monitoring loop: {e}")
        
        await asyncio.sleep(interval_sec)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _monitoring_task
    if os.getenv("ENABLE_SOURCE_MONITORING", "false").lower() == "true":
        _monitoring_task = asyncio.create_task(_monitoring_loop())
        
    yield  # Nothing to do at startup — bot initializes lazily
    
    if _monitoring_task:
        _monitoring_task.cancel()
        try:
            await _monitoring_task
        except asyncio.CancelledError:
            pass
            
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
        "url": "https://github.com/shlok926/rtiassist-api",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS
cors_origins_str = os.getenv("CORS_ORIGINS", "*" if ENVIRONMENT != "production" else "")
origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

if ENVIRONMENT == "production":
    if not origins or "*" in origins:
        raise ValueError("CORS_ORIGINS must be explicitly provided in production and cannot be '*'.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True if ENVIRONMENT == "production" else False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # We can inject request_id into context vars if needed, but for now just logging it
    logger.info(f"Req_ID: {request_id} | {request.method} {request.url.path} started")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Req_ID: {request_id} | {request.method} {request.url.path} completed | Status: {response.status_code} | Duration: {process_time:.4f}s")
    
    response.headers["X-Request-ID"] = request_id
    return response


# Register routes
app.include_router(rti_router)
app.include_router(legal_router)
app.include_router(auth_router)
app.include_router(cases_router)
app.include_router(authorities_router)
app.include_router(admin_authorities_router)
from routes.pdf_analysis import router as pdf_analysis_router
from routes.document_drafting import router as document_drafting_router
from routes.company_registration import router as company_registration_router
app.include_router(pdf_analysis_router)
app.include_router(document_drafting_router)
app.include_router(company_registration_router)


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
    if not TELEGRAM_TOKEN:
        return Response(status_code=200)
    try:
        from telegram import Update
        data = await request.json()
        bot_app = await _get_telegram_app()
        if bot_app:
            update = Update.de_json(data, bot_app.bot)
            await bot_app.process_update(update)
        else:
            logger.warning("Telegram update received but bot not ready yet")
    except Exception as e:
        logger.error(f"Error processing Telegram update: {e}")
    return Response(status_code=200)


@app.get("/debug/webhook", include_in_schema=False)
async def debug_webhook():
    """Debug endpoint — check webhook status."""
    if ENVIRONMENT != "development":
        return Response(status_code=403, content="Forbidden")
    if not _telegram_app:
        return {"error": "Telegram bot not initialized", "token_set": bool(os.getenv("TELEGRAM_TOKEN"))}
    try:
        info = await _telegram_app.bot.get_webhook_info()
        return {
            "webhook_url": info.url,
            "pending_update_count": info.pending_update_count,
            "last_error_message": info.last_error_message,
            "last_error_date": str(info.last_error_date) if info.last_error_date else None,
        }
    except Exception:
        return {"error": "Failed to retrieve webhook info"}


@app.get("/admin/set-webhook", include_in_schema=False)
async def admin_set_webhook():
    """Manually trigger webhook registration."""
    if ENVIRONMENT != "development":
        return Response(status_code=403, content="Forbidden")
    if not _telegram_app:
        return {"error": "Telegram bot not initialized"}
    try:
        await _register_webhook()
        info = await _telegram_app.bot.get_webhook_info()
        return {"success": True, "webhook_url": info.url}
    except Exception:
        return {"error": "Failed to configure webhook"}


@app.get("/debug/ping-telegram", include_in_schema=False)
async def ping_telegram():
    """Test if HF Space can reach api.telegram.org using requests (sync)."""
    if ENVIRONMENT != "development":
        return Response(status_code=403, content="Forbidden")
    import requests as req
    results = {}
    try:
        r = req.get("https://api.telegram.org", timeout=8)
        results["requests_sync"] = f"OK {r.status_code}"
    except Exception:
        results["requests_sync"] = "FAIL: Connection error"
    return results
