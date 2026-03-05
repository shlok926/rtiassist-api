from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.rti import router as rti_router
from routes.legal import router as legal_router
from models.schemas import HealthResponse

load_dotenv()

app = FastAPI(
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
