# 🏛️ RTIAssist — Design Document & Tech Stack

> Complete system design, architecture, component breakdown, and full technology stack
> Version: 2.0 | March 2026

---

## 📋 Table of Contents

1. [System Overview](#1-system-overview)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Component Design](#3-component-design)
4. [AI Pipeline Design](#4-ai-pipeline-design)
5. [Frontend Design](#5-frontend-design)
6. [Backend Design](#6-backend-design)
7. [Telegram Bot Design](#7-telegram-bot-design)
8. [Data Flow Diagrams](#8-data-flow-diagrams)
9. [Full Tech Stack](#9-full-tech-stack)
10. [File & Folder Structure](#10-file--folder-structure)
11. [Design Decisions & Trade-offs](#11-design-decisions--trade-offs)

---

## 1. System Overview

RTIAssist is a **3-component system**:

| Component | Description | Hosting |
|-----------|-------------|---------|
| **Web Frontend** | Single HTML file — RTI generator, legal tools, tracker, settings | GitHub Pages / HF Space (static) |
| **FastAPI Backend** | REST API — AI pipeline + legal tool generators + Telegram webhook | Hugging Face Spaces (Docker) |
| **Telegram Bot** | @RTIAssistBot — 7 commands, deadline reminders, inline keyboards | Render (free tier) |

All three communicate over HTTPS. No shared database — the backend is **stateless** (privacy by design).

```
User (Browser) ←────────────────────→ index_Version4.html
                                              │
                                     HTTPS REST calls
                                              │
                                              ▼
                                  FastAPI  (HF Space :7860)
                                       │          │
                              ASI-1 API      Telegram Webhook
                                              │
                                              ▼
                                   @RTIAssistBot (Render)
```

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                            PRESENTATION LAYER                            │
│                                                                          │
│   ┌──────────────────────────────┐   ┌──────────────────────────────┐   │
│   │     index_Version4.html      │   │     @RTIAssistBot             │   │
│   │  ─────────────────────────  │   │  ─────────────────────────   │   │
│   │  • RTI Generator             │   │  • /start  /help  /about     │   │
│   │  • 4 Legal Tools             │   │  • /fee  /state  /legal      │   │
│   │  • RTI Tracker               │   │  • /myreminders              │   │
│   │  • Settings (Notif, Remind)  │   │  • Deadline reminder alerts  │   │
│   │  • 11 Languages              │   │  • Inline keyboard menus     │   │
│   └──────────────┬───────────────┘   └──────────────┬───────────────┘   │
└──────────────────┼──────────────────────────────────┼────────────────────┘
                   │ HTTP/REST                         │ Webhook (POST)
                   ▼                                   ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                             SERVICE LAYER  (FastAPI)                     │
│                                                                          │
│   ┌──────────────────┐   ┌──────────────────┐   ┌────────────────────┐  │
│   │  routes/rti.py   │   │ routes/legal.py  │   │  /telegram webhook │  │
│   │  ─────────────  │   │  ─────────────   │   │  ───────────────   │  │
│   │  POST /rti/      │   │  POST /legal/    │   │  Receives Telegram │  │
│   │  generate        │   │  generate        │   │  updates from API  │  │
│   └────────┬─────────┘   └──────────────────┘   └────────────────────┘  │
└────────────┼─────────────────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                           AI PIPELINE LAYER                              │
│                                                                          │
│   [1] IntentClassifier → [2] PIOResolver → [3] DraftGenerator → [4] QualityChecker │
│                                                                          │
│   Each layer calls ASI-1 API  (or returns demo response if DEMO_MODE)   │
└──────────────────────────────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SERVICES                                │
│                                                                          │
│   ASI-1 AI (api.asi1.ai)    Telegram Bot API    Formspree (feedback)    │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Design

### 3.1 Frontend — `index_Version4.html`

A **fully self-contained single-file web app** — no build step, no npm, no framework.

```
index_Version4.html
├── <head>
│   ├── Meta tags (SEO, OG, description)
│   ├── Google Fonts (DM Sans, Nunito) — CDN
│   └── <style> — All CSS inline (~600 lines)
│       ├── CSS variables (colors, spacing)
│       ├── Dark theme design system
│       ├── Component styles (cards, buttons, modals, forms)
│       ├── Responsive breakpoints (≤480px mobile)
│       └── Page transition animations
│
├── <body>
│   ├── Nav bar (logo + page buttons + legal dropdown)
│   ├── Page: #home       — RTI Generator
│   ├── Page: #legaltools  — Legal Tools Hub (4 cards)
│   ├── Page: #second-appeal
│   ├── Page: #consumer-court
│   ├── Page: #legal-notice
│   ├── Page: #labour
│   ├── Page: #tracker    — RTI Deadline Tracker
│   ├── Page: #settings   — Settings + Feedback + FAQ + Privacy
│   ├── Modal: Language Selector (z-index 500)
│   └── Modal: Privacy Policy (z-index 2000)
│
└── <script> — All JS inline (~1800 lines)
    ├── State variables (_feedbackRating, currentLanguage, currentState...)
    ├── showPage() — SPA-style page navigation
    ├── generateRTI() — API call + display result
    ├── Legal tool generators (4 functions)
    ├── RTI Tracker (CRUD — localStorage)
    ├── Bell/Notification system
    ├── Telegram reminder setup
    ├── Star rating IIFE (hover + click)
    ├── FAQ accordion
    ├── Privacy modal
    └── Formspree feedback submit
```

**Page Navigation Model:**
SPA (Single Page Application) pattern — all pages are `<div class="page">` elements. `showPage(id)` hides all, shows the target:

```javascript
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}
```

---

### 3.2 Backend — `main.py` + `routes/`

**Entry point:** `main.py`
- FastAPI app with `lifespan` context manager
- Telegram setup runs during startup (if `TELEGRAM_TOKEN` is set)
- CORS middleware allows all origins (public API)
- Registers two routers: `rti_router` (`/rti`) and `legal_router` (`/legal`)

```
main.py
├── lifespan() — startup/shutdown manager
│   ├── _setup_telegram() — registers commands, sets webhook
│   └── Shutdown — stops bot gracefully
├── CORSMiddleware — allow all origins
├── /rti router mounted at prefix /rti
├── /legal router mounted at prefix /legal
└── /telegram — Telegram webhook receiver
```

**Routing:**

```
routes/
├── rti.py     → POST /rti/generate
│                   If DEMO_MODE: returns pre-built response immediately
│                   Else:         runs 4-layer AI pipeline
└── legal.py   → POST /legal/generate
                    Dispatches to one of 4 template generators
                    based on req.tool field
```

---

### 3.3 Agents — `agents/`

Each agent is an independent Python module. They are called sequentially in the pipeline.

```
agents/
├── intent_classifier.py   # Layer 1 — classify department, ministry, urgency
├── pio_resolver.py        # Layer 2 — PIO address, fee, portal URL
├── draft_generator.py     # Layer 3 — full RTI draft in requested language
└── quality_checker.py     # Layer 4 — quality score, warnings, exemption risk
```

Each agent:
1. Constructs a prompt using system prompt from `prompts/system_prompts.py`
2. Calls `utils/asi1_client.py:call_asi1()`
3. Parses JSON response
4. Returns a dict to the next layer

---

### 3.4 Data Models — `models/schemas.py`

All API contracts are defined with Pydantic:

```python
RTIRequest       → Input to /rti/generate
  ├── description: str (20–2000 chars)
  ├── language: str (11 options)
  ├── state: Optional[str]
  └── demo_mode: Optional[bool]

RTIResponse      → Output of /rti/generate
  ├── draft: str                         # complete RTI text
  ├── filing_instructions: str
  ├── department, ministry, government_level
  ├── urgency, pio_details
  ├── quality_score: int (0–100)
  ├── is_valid: bool
  ├── warnings: List[str]
  ├── suggestions: List[str]
  ├── exempt_risk: str (none/low/medium/high)
  ├── estimated_success_probability: str
  └── confidence: float (0.0–1.0)

LegalRequest     → Input to /legal/generate
  └── tool + all optional fields for 4 tools

HealthResponse   → Output of GET /health
```

---

## 4. AI Pipeline Design

### Pipeline Flow

```
User Input (plain language description)
             │
             ▼
    ┌─────────────────────────────────────────────┐
    │  LAYER 1 — IntentClassifier                 │
    │                                             │
    │  System Prompt: INTENT_CLASSIFIER           │
    │  Temperature:   0.2  (deterministic)        │
    │  Max Tokens:    500                         │
    │                                             │
    │  Output JSON:                               │
    │  {                                          │
    │    information_needed: str,                 │
    │    department: str,                         │
    │    ministry: str,                           │
    │    government_level: "central|state",       │
    │    state_name: str|null,                    │
    │    rti_section: str,                        │
    │    urgency: "routine|urgent|life_threatening"│
    │    confidence: float (0.0–1.0)              │
    │  }                                          │
    └────────────────────┬────────────────────────┘
                         │ intent dict
                         ▼
    ┌─────────────────────────────────────────────┐
    │  LAYER 2 — PIOResolver                      │
    │                                             │
    │  System Prompt: PIO_RESOLVER                │
    │  Temperature:   0.2                         │
    │  Max Tokens:    500                         │
    │                                             │
    │  Input:  department + ministry + state      │
    │  Output JSON:                               │
    │  {                                          │
    │    pio_designation: str,                    │
    │    appellate_authority_designation: str,    │
    │    address_format: str,                     │
    │    filing_fee: str,                         │
    │    fee_payment_modes: [str],                │
    │    response_timeline_days: 30,              │
    │    life_threatening_timeline_days: 48,      │
    │    online_portal: str|null,                 │
    │    additional_notes: str                    │
    │  }                                          │
    └────────────────────┬────────────────────────┘
                         │ pio_info dict
                         ▼
    ┌─────────────────────────────────────────────┐
    │  LAYER 3 — DraftGenerator                   │
    │                                             │
    │  System Prompt: DRAFT_GENERATOR             │
    │  Temperature:   0.3                         │
    │  Max Tokens:    1500                        │
    │                                             │
    │  Input:  intent + pio_info + language       │
    │  Language enforcement injected into prompt  │
    │  (e.g., "Write ENTIRE application in Hindi  │
    │   Devanagari — हिन्दी")                     │
    │                                             │
    │  Output: Complete RTI application text      │
    │          Ready to print and file            │
    └────────────────────┬────────────────────────┘
                         │ draft string
                         ▼
    ┌─────────────────────────────────────────────┐
    │  LAYER 4 — QualityChecker                   │
    │                                             │
    │  System Prompt: QUALITY_CHECKER             │
    │  Temperature:   0.1  (very deterministic)   │
    │  Max Tokens:    400                         │
    │                                             │
    │  Input:  draft text                         │
    │  Output JSON:                               │
    │  {                                          │
    │    is_valid: bool,                          │
    │    score: int (0–100),                      │
    │    issues: [str],                           │
    │    suggestions: [str],                      │
    │    exempt_risk: "none|low|medium|high",     │
    │    exempt_risk_reason: str,                 │
    │    estimated_success_probability: str       │
    │  }                                          │
    └────────────────────────────────────────────┘
                         │
                         ▼
             Final RTIResponse JSON  →  Client
```

### Temperature Strategy

| Layer | Temp | Reason |
|-------|------|--------|
| IntentClassifier | 0.2 | Department classification must be consistent |
| PIOResolver | 0.2 | Legal addresses must match exactly each time |
| DraftGenerator | 0.3 | Slightly creative to vary phrasing, but formal |
| QualityChecker | 0.1 | Scoring must be deterministic and unbiased |

### Demo Mode Bypass

```python
if DEMO_MODE or request.demo_mode == True:
    # Skip all 4 AI layers
    # Return pre-written high-quality sample response
    return get_demo_response(request)
```

Demo responses are scenario-matched (ration, passport, road, exam, etc.) with realistic quality scores, PIO details, and filing instructions.

---

### Error Handling in AI Calls (`utils/asi1_client.py`)

```
call_asi1() called
    │
    ├── HTTP 429 (rate limit) → wait 2^attempt seconds → retry (max 3x)
    ├── HTTP 5xx              → wait and retry (max 3x)
    ├── Timeout (30s)         → raise exception → caller returns fallback
    └── JSONDecodeError       → each agent returns safe fallback dict
                                 with confidence: 0.3 or score: 70
```

---

## 5. Frontend Design

### 5.1 Design System

| Token | Value | Usage |
|-------|-------|-------|
| `--green` | `#00A86B` | Primary brand — RTI buttons, borders, highlights |
| `--green-l` | `#34d399` | Light green — success states, text accents |
| `--purple` | `#6B21A8` | Legal Tools secondary brand |
| `--purple-l` | `#9333EA` | Legal button hovers |
| `--bg` | `#0A0A0A` | Page background |
| `--surface` | `#111827` | Card/modal background |
| `--surface-2` | `#1F2937` | Input fields, inner surfaces |
| `--text` | `#FFFFFF` | Primary text |
| `--text-muted` | `rgba(255,255,255,0.65)` | Secondary text |
| `--radius-card` | `12px` | Cards, panels |
| `--radius-btn` | `8px` | Buttons, inputs |
| `--radius-pill` | `50px` | Language/state pills |

### 5.2 Typography

| Role | Font | Weight | Size |
|------|------|--------|------|
| Headings | Nunito | 700–800 | 1.4–2rem |
| Body | DM Sans | 400 | 0.9rem |
| Labels | DM Sans | 600 | 0.85rem |
| Results/Draft | DM Sans | 400 | 0.82rem |

### 5.3 Z-Index Layers

| Layer | Z-Index | Element |
|-------|---------|---------|
| Base content | 1 | Pages, cards |
| Navigation | 100 | Top nav bar |
| Dropdown menus | 200 | Legal tools nav dropdown |
| Language modal | 500 | Language selector overlay |
| Privacy modal | 2000 | Privacy Policy overlay |

### 5.4 State Management (JavaScript)

All global state is held in plain JS variables:

```javascript
// UI state
let currentPage = 'home';
let currentLanguage = 'english';    // from localStorage
let currentState = null;             // from localStorage

// Feedback state
let _feedbackRating = 0;             // 0–5 stars

// Notification state
let _notifGranted = false;           // browser push permission
let _bellRTIs = [];                  // RTIs from localStorage for bell

// Tracker
function getAllRTIs()   // reads localStorage["rti_tracker"]
function saveAllRTIs()  // writes to localStorage["rti_tracker"]
```

### 5.5 localStorage Schema

```javascript
"rti_tracker"     → JSON array of RTI objects (id, dept, date, deadline, status)
"rti_language"    → string: selected language
"rti_state"       → string: selected state
"telegram_user"   → string: @username
"notif_enabled"   → "true" | "false"
"feedback_rating" → "1"–"5"
```

### 5.6 API Call Pattern (Frontend)

```javascript
async function generateRTI() {
  const payload = {
    description: textarea.value,
    language: currentLanguage,
    state: currentState,
  };

  const res = await fetch('https://visgrow-03-rtiassist-api.hf.space/rti/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  // Render: data.draft, data.quality_score, data.filing_instructions, etc.
}
```

---

## 6. Backend Design

### 6.1 Application Startup (`main.py` lifespan)

```
App starts
    │
    ├── load_dotenv()  — load .env file
    ├── _setup_telegram()  — runs if TELEGRAM_TOKEN exists
    │       ├── Build Application with token
    │       ├── Register 7 CommandHandlers
    │       ├── Register CallbackQueryHandler
    │       ├── Register MessageHandler
    │       ├── await initialize() + start()
    │       └── set_webhook(url) if WEBHOOK_URL is set
    │
    └── yield  (app is running)
    
App shuts down
    └── bot.stop() + bot.shutdown()
```

### 6.2 Request Lifecycle — `/rti/generate`

```
POST /rti/generate  (JSON body)
    │
    ├── Pydantic validates RTIRequest
    │   ├── description: 20–2000 chars ← 422 if fails
    │   └── language: valid option     ← 422 if fails
    │
    ├── Determine demo_mode:
    │   request.demo_mode → or → DEMO_MODE env → default false
    │
    ├── if demo_mode:
    │   └── get_demo_response(request) → return immediately
    │
    └── AI Pipeline:
        ├── intent = classify_intent(description)
        ├── pio   = resolve_pio(dept, ministry, level, state)
        ├── draft = generate_draft(intent, pio, language)
        └── quality = check_quality(draft)
        
        → Build RTIResponse → return JSON
```

### 6.3 Legal Tool Dispatch (`routes/legal.py`)

```
POST /legal/generate  (JSON body with "tool" field)
    │
    ├── tool == "second_appeal"
    │   ├── Validate: name, department, query required
    │   └── generate_second_appeal_demo(req)
    │
    ├── tool == "consumer_complaint"
    │   ├── Validate: name, company, description required
    │   └── generate_consumer_complaint_demo(req)
    │
    ├── tool == "legal_notice"
    │   ├── Validate: sender, recipient, description required
    │   └── generate_legal_notice_demo(req)
    │
    ├── tool == "labour_complaint"
    │   ├── Validate: name, employer, description required
    │   └── generate_labour_complaint_demo(req)
    │
    └── unknown tool → HTTP 400
```

Each generator is a pure Python function — no AI call — that interpolates user data into a legally formatted f-string template, with law-section lookups via internal `dict` maps.

---

## 7. Telegram Bot Design

### 7.1 Bot Architecture

```
bot_server.py  (Render)              OR   main.py  (HF Space)
     │                                         │
     └── python-telegram-bot v20               └── same Application
          Application (webhook mode)                 (webhook mode)
               │
               ▼  HTTPS Webhook
          api.telegram.org
               │
               ▼
          User message arrives
               │
     ┌─────────┴──────────┐
     │   Handler routing  │
     │  ─────────────── │
     │  /start    → start()          │
     │  /help     → help_cmd()       │
     │  /about    → about()          │
     │  /fee      → fee()            │
     │  /state    → state_cmd()      │
     │  /legal    → legal_cmd()      │
     │  /myreminders → myreminders() │
     │  button click → button_callback() │
     │  text msg  → handle_message() │
     └───────────────────────────────┘
```

### 7.2 Reminder System (In-Memory)

```python
# Structure held in memory (lost on restart)
reminders = {
    12345678: [           # chat_id
        {
            "department": "PWD Maharashtra",
            "filed_date":  "2026-01-15",
            "deadline":    "2026-02-14",
            "notified_7":  False,
            "notified_3":  False,
            "notified_1":  False,
        }
    ]
}
```

**Reminder check loop** (runs every hour):
```
For each chat_id in reminders:
  For each reminder:
    days_left = (deadline - today).days
    if days_left == 7 and not notified_7 → send alert → set notified_7 = True
    if days_left == 3 and not notified_3 → send alert → set notified_3 = True
    if days_left == 1 and not notified_1 → send alert → set notified_1 = True
```

### 7.3 State Auto-Detection

When user sends a message, the bot scans it for city/state keywords:

```python
STATE_KEYWORDS = {
  "Maharashtra": ["maharashtra", "mumbai", "pune", "nagpur"],
  "Delhi":       ["delhi", "new delhi"],
  "Gujarat":     ["gujarat", "ahmedabad", "surat"],
  ...  # 20 states covered
}

def auto_detect_state(text: str) -> str | None:
    for state, keywords in STATE_KEYWORDS.items():
        for kw in keywords:
            if kw in text.lower():
                return state
    return None
```

### 7.4 Dual Language System

```
bot_languages.py
├── UI_LANGUAGES   — language codes for bot UI (what bot says)
├── DRAFT_LANGUAGES — language codes passed to /rti/generate API
└── get_message(key, lang) — returns localized string for bot messages
```

Users can select language for:
1. Bot UI messages (Hindi/English)
2. RTI draft language (all 11 languages)

---

## 8. Data Flow Diagrams

### 8.1 RTI Generation — End to End

```
Browser                    FastAPI                  ASI-1 API
   │                          │                         │
   │──POST /rti/generate──────►│                         │
   │   {description, lang,    │                         │
   │    state, demo_mode}     │                         │
   │                          │                         │
   │                          │──classify_intent────────►│
   │                          │◄──{dept, ministry,      │
   │                          │    urgency, confidence}──│
   │                          │                         │
   │                          │──resolve_pio────────────►│
   │                          │◄──{pio_designation,      │
   │                          │    address, fee}─────────│
   │                          │                         │
   │                          │──generate_draft─────────►│
   │                          │◄──"Full RTI text..."─────│
   │                          │                         │
   │                          │──check_quality──────────►│
   │                          │◄──{score, warnings...}───│
   │                          │                         │
   │◄──RTIResponse────────────│                         │
   │   {draft, score,         │                         │
   │    instructions, ...}    │                         │
```

### 8.2 Legal Tool Generation — End to End

```
Browser                    FastAPI
   │                          │
   │──POST /legal/generate────►│
   │   {tool: "second_appeal", │
   │    name, dept, query...} │
   │                          │
   │                          │── dispatch based on req.tool
   │                          │── generate_second_appeal_demo(req)
   │                          │   (pure template, no AI needed)
   │                          │── returns formatted legal document
   │                          │
   │◄──{draft, tool, status}──│
```

### 8.3 Telegram Reminder — End to End

```
User (Telegram)        @RTIAssistBot         FastAPI (HF Space)
      │                      │                      │
      │──/start─────────────►│                      │
      │◄──Welcome message────│                      │
      │                      │                      │
      │──"My ration card..."─►│                      │
      │                      │──POST /rti/generate──►│
      │                      │◄──{draft, score...}───│
      │◄──RTI draft + score──│                      │
      │                      │                      │
      │──Set reminder────────►│                      │
      │                      │──store in reminders{}│
      │◄──Reminder set ✓─────│                      │
      │                      │                      │
  [3 days later]             │                      │
      │◄──⚠️ RTI deadline    │                      │
      │   in 3 days! ---─────│                      │
```

---

## 9. Full Tech Stack

### 9.1 Backend Stack

| Category | Technology | Version | Role |
|----------|-----------|---------|------|
| **Language** | Python | 3.10 | Core runtime |
| **Web Framework** | FastAPI | latest | REST API server, webhook receiver |
| **ASGI Server** | Uvicorn | latest | Production HTTP server |
| **Data Validation** | Pydantic | v2 | Request/response schemas, type safety |
| **HTTP Client** | requests | latest | ASI-1 API calls, retry logic |
| **Bot Framework** | python-telegram-bot | v20 | Telegram webhook bot (async) |
| **PDF Generation** | reportlab | latest | PDF export for RTI drafts |
| **Config** | python-dotenv | latest | `.env` file loading |
| **Testing** | pytest | latest | Unit tests |
| **Test Client** | httpx | latest | Async API testing |
| **Async Runtime** | asyncio (stdlib) | built-in | Async startup, bot coroutines |

### 9.2 AI & ML Stack

| Category | Technology | Detail |
|----------|-----------|--------|
| **AI Model** | ASI-1 (`asi1-mini`) | Fetch.ai's language model |
| **API Protocol** | OpenAI-compatible | `POST /v1/chat/completions` |
| **Auth** | Bearer token | `ASI1_API_KEY` env variable |
| **Streaming** | Disabled | `stream: false` — full response |
| **Prompt Style** | System + User message | Structured JSON output enforced in prompts |
| **Temperature** | 0.1 – 0.3 | Low for legal accuracy; slight variance for drafts |
| **Max Tokens** | 400 – 1500 | Per layer, tuned to output length |
| **Retry Strategy** | Exponential backoff | 3 retries, wait: 2^n seconds on 429/5xx |
| **Fallback** | Demo mode | Pre-built responses when API unavailable |

### 9.3 Frontend Stack

| Category | Technology | Version | Role |
|----------|-----------|---------|------|
| **Markup** | HTML5 | — | Structure |
| **Styling** | CSS3 | — | Custom design system, no framework |
| **Logic** | Vanilla JavaScript | ES6+ | All interactivity, API calls, DOM manipulation |
| **Persistence** | localStorage API | Browser built-in | RTI tracker, user preferences |
| **Notifications** | Web Notifications API | Browser built-in | Deadline push alerts |
| **Fonts** | Google Fonts | CDN | DM Sans + Nunito |
| **Icons** | Emoji | — | No external icon library dependency |
| **Form Backend** | Formspree | v2 API | Feedback form email handler |
| **Build Tool** | None | — | Plain file, no webpack/vite/rollup |
| **Framework** | None | — | Vanilla JS only — no React/Vue/Angular |

### 9.4 Infrastructure Stack

| Category | Platform | Plan | Role |
|----------|---------|------|------|
| **API Hosting** | Hugging Face Spaces | Free (CPU Basic) | FastAPI + Docker deployment |
| **Bot Hosting** | Render | Free tier | Telegram bot server (bot_server.py) |
| **Container** | Docker | python:3.10-slim | HF Spaces deployment image |
| **Source Control** | GitHub | Free (public) | Code hosting, version control |
| **CI/CD** | HF Auto-Deploy | — | Push to GitHub → HF rebuilds automatically |
| **Process Manager** | start.sh (bash) | — | Startup script on HF container |
| **Static Hosting** | GitHub Pages (planned) | Free | Frontend public URL |

### 9.5 DevOps & Config

| File | Purpose |
|------|---------|
| `Dockerfile` | Docker image for HF Spaces — python:3.10-slim, port 7860, DEMO_MODE=true |
| `render.yaml` | Render deployment config — bot_server.py, env vars, free plan |
| `requirements.txt` | Python dependencies — fastapi, uvicorn, pydantic, requests, python-telegram-bot, reportlab, dotenv, pytest, httpx |
| `start.sh` | Startup script — sets env, starts uvicorn |
| `.env` | Local secrets — never committed (in .gitignore) |
| `Procfile` | Alternative process definition (Render/Heroku compatible) |

### 9.6 Testing Stack

| Category | Tool | Usage |
|----------|------|-------|
| **Unit Tests** | pytest | `tests/test_rti.py`, `test_features.py`, `test_bot_features.py` |
| **API Testing** | httpx (async) | Test `/rti/generate` and `/legal/generate` endpoints |
| **Manual Testing** | Browser DevTools | Frontend JS validation, localStorage inspection |
| **Bot Testing** | Telegram app | Manual command + callback testing |

---

## 10. File & Folder Structure

```
rtiassist-api/
│
├── main.py                    # FastAPI app entry point, lifespan, CORS, router registration
├── app.py                     # Alternative app entry (bot_server mode)
├── bot_server.py              # Telegram-only server for Render deployment
├── telegram_bot.py            # Bot handlers — all 7 commands, callbacks, reminders
├── bot_languages.py           # Localized strings for bot UI (Hindi/English)
│
├── routes/
│   ├── __init__.py
│   ├── rti.py                 # POST /rti/generate — pipeline orchestrator
│   └── legal.py               # POST /legal/generate — 4 legal tool generators
│
├── agents/
│   ├── __init__.py
│   ├── intent_classifier.py   # AI Layer 1 — classify department/ministry/urgency
│   ├── pio_resolver.py        # AI Layer 2 — PIO address, fee, portal
│   ├── draft_generator.py     # AI Layer 3 — full RTI draft generation
│   └── quality_checker.py     # AI Layer 4 — score, warnings, exemption risk
│
├── models/
│   ├── __init__.py
│   └── schemas.py             # Pydantic schemas — RTIRequest, RTIResponse, LegalRequest
│
├── prompts/
│   ├── __init__.py
│   └── system_prompts.py      # 4 system prompts for AI layers
│
├── utils/
│   ├── __init__.py
│   └── asi1_client.py         # ASI-1 API wrapper — auth, retry, error handling
│
├── tests/
│   ├── __init__.py
│   ├── test_rti.py            # RTI endpoint tests
│   └── (test_features.py, test_bot_features.py — root level)
│
├── index_Version4.html        # Complete frontend — RTI generator + legal tools + tracker
├── tracker_Version2.js        # RTI tracker module (standalone JS)
├── legal_examples.js          # Legal tool example data
├── ui_translations.js         # Frontend i18n translations
│
├── requirements.txt           # Python dependencies
├── Dockerfile                 # HF Spaces Docker config
├── start.sh                   # Container startup script
├── Procfile                   # Process definition (Render/Heroku)
├── render.yaml                # Render deployment config
│
└── docs/
    ├── README.md              # Technical quick-start (DO NOT MODIFY)
    ├── RTI_PRODUCT_OVERVIEW.md # RTI education, use cases, competitors
    ├── LEGAL_TOOLS_GUIDE.md   # 4 legal tools step-by-step
    ├── RTIAssist_PRD_TRD.md   # PRD + TRD
    └── DESIGN_AND_TECH_STACK.md # This file
```

---

## 11. Design Decisions & Trade-offs

### Decision 1 — Single HTML File (No Framework)

| | Choice | Alternative |
|-|--------|------------|
| **Chosen** | Single `index_Version4.html` — vanilla HTML/CSS/JS | React / Vue / Next.js |
| **Why** | Zero build setup, zero dependencies, instant deploy via GitHub Pages, works offline | Faster dev with framework but heavy setup |
| **Trade-off** | Harder to maintain as file grows (4000+ lines) | Easier state management with React but adds complexity for this project size |

### Decision 2 — No Database (localStorage Only)

| | Choice | Alternative |
|-|--------|------------|
| **Chosen** | All user data in localStorage | PostgreSQL / Supabase |
| **Why** | Privacy-first — no user data leaves the browser, no GDPR concerns, zero infra cost | Server DB allows cross-device sync but requires auth system |
| **Trade-off** | Data lost if user clears browser; no cross-device support | But eliminates biggest privacy surface |

### Decision 3 — Demo Mode by Default

| | Choice | Alternative |
|-|--------|------------|
| **Chosen** | `DEMO_MODE=true` on HF Space; real AI optional | Always call ASI-1 API |
| **Why** | HF Free tier can't sustain API costs; demo quality is still excellent; zero latency | Real AI gives personalized output but needs paid plan |
| **Trade-off** | Demo responses are scenario-matched, not truly custom | Acceptable for MVP and demo purposes |

### Decision 4 — 4-Layer AI Pipeline

| | Choice | Alternative |
|-|--------|------------|
| **Chosen** | 4 separate small AI calls | One large single prompt |
| **Why** | Each layer is focused → better accuracy per task; easier to debug and improve individually | Single call is faster (1 round trip) but lower quality |
| **Trade-off** | 4x API latency in AI mode | Quality + maintainability justified the cost |

### Decision 5 — Legal Tools as Templates (No AI)

| | Choice | Alternative |
|-|--------|------------|
| **Chosen** | Pure Python f-string templates with legal lookup dicts | Call AI for each legal doc |
| **Why** | Legal documents require exact citations — templates guarantee accuracy; instant response | AI adds flexibility but risks citing wrong section |
| **Trade-off** | No personalization beyond filled fields | Legally safer and faster |

### Decision 6 — Telegram Bot on Render (Not HF Space)

| | Choice | Alternative |
|-|--------|------------|
| **Chosen** | Separate Render service for bot | Bundle bot into HF Space |
| **Why** | HF Spaces sleeps on inactivity — bad for webhook bots; Render stays awake | HF bundling would cause missed Telegram updates |
| **Trade-off** | Two deployments to manage | Reliability for bot justified the split |

---

*RTIAssist — Designed for simplicity, built for scale, made for every Indian citizen.*
*Design Document v2.0 | March 2026*
