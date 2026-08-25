# 📋 RTIAssist — PRD & TRD

> **Product Requirements Document (PRD) + Technical Requirements Document (TRD)**
> Project: RTIAssist | Version: 2.0 | Date: March 2026 | Status: Live

---

# PART 1 — PRODUCT REQUIREMENTS DOCUMENT (PRD)

---

## 📊 1. Project Overview

| Field | Details |
|-------|---------|
| **Product Name** | RTIAssist |
| **Tagline** | AI-powered RTI application generator for every Indian citizen |
| **Version** | 2.0 |
| **Status** | Live (Hugging Face Space + Render Bot) |
| **Live URL** | https://visgrow-03-rtiassist-api.hf.space |
| **Repo** | https://github.com/shlok926/rtiassist-api |
| **Languages** | 11 Indian languages |
| **Last Updated** | March 2026 |

RTIAssist is a free, open-source web + Telegram tool that turns a citizen's plain-language description of a problem into a **legally correct RTI application** — in seconds — along with 4 legal document generators (Second Appeal, Consumer Complaint, Legal Notice, Labour Complaint).

---

## 🎯 2. Product Vision

**Mission:** Make the Right to Information Act 2005 accessible to every Indian citizen regardless of their legal knowledge, language, or education level.

**Vision Statement:**
> "Koi bhi naagrik, kisi bhi bhasha mein, apna RTI khud likh sake — bina vakeel ke, bina paison ke."
> *(Any citizen, in any language, should be able to write their own RTI — no lawyer, no money.)*

**Core Belief:**
- RTI is a fundamental right (Article 19(1)(a)) but 99% of citizens don't know how to use it
- Bureaucratic language creates fear and barriers
- AI can bridge the gap between citizen's problem and the legal document required

**North Star Metric:** Number of RTI applications successfully generated and filed by real citizens.

---

## 👤 3. Target User

### Primary Users

| Persona | Profile | Pain Point | How RTIAssist Helps |
|---------|---------|------------|---------------------|
| 🌾 Rural Citizen | Farmer/village resident, Hindi-speaking | Ration card rejected, no guidance | Generates Hindi RTI in 30 seconds |
| 🏙️ Urban Middle Class | Salaried, 25–45 years | Passport/property delay, doesn't know RTI format | English RTI + filing guide |
| 🎓 Student | College student | Exam marks not disclosed, scholarship held | Draft + Section 8 risk check |
| 👷 Worker | Factory/daily wage | Salary not paid, PF not deposited | Labour complaint + RTI both |
| 🏘️ RWA Member | Society secretary | Road/water/garbage issues | RTI to municipality + docs |
| 📰 Journalist | Freelance/regional | Needs government info for story | Quick professional RTI draft |
| 🏥 Patient/Family | Healthcare seeker | Hospital records, death certificate denied | Urgent RTI (48-hour clause) |

### Secondary Users
- NGOs / legal aid clinics
- Law students learning RTI practice
- Developers building civic-tech tools (via API)

### NOT the Target User
- Legal professionals (they already know)
- Users seeking commercial document services

---

## ✨ 4. Core Features

### Feature Set A — RTI Generator (Core)

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| A1 | Plain-language Input | User types their problem in natural language | ✅ Live |
| A2 | AI Intent Classification | 4-layer pipeline classifies department, ministry, urgency | ✅ Live |
| A3 | PIO Resolver | Auto-fetches correct PIO address and fee details for state/central | ✅ Live |
| A4 | Draft Generator | Full RTI application with all mandatory sections | ✅ Live |
| A5 | Quality Checker | Scores RTI 0–100, warns about Section 8 exemption risks | ✅ Live |
| A6 | 11 Language Support | Hindi, English, Marathi, Tamil, Telugu, Kannada, Bengali, Gujarati, Punjabi, Malayalam, Odia | ✅ Live |
| A7 | State Selector | All 28 states + central government supported | ✅ Live |
| A8 | Filing Instructions | Auto-generated step-by-step filing guide per state | ✅ Live |
| A9 | Demo Mode | Instant response without AI API for HF Space | ✅ Live |

### Feature Set B — Legal Tools

| # | Feature | Document Generated | Law |
|---|---------|-------------------|-----|
| B1 | Second Appeal (CIC) | Appeal to Central Information Commission | RTI Act 2005 Sec 19(3) |
| B2 | Consumer Complaint | District Consumer Commission complaint | Consumer Protection Act 2019 |
| B3 | Legal Notice | Formal pre-litigation notice | NI Act / Contract Act / RERA |
| B4 | Labour Complaint | Labour Commissioner complaint | Payment of Wages Act / ID Act |

### Feature Set C — Settings & Utility

| # | Feature | Description | Status |
|---|---------|-------------|--------|
| C1 | RTI Tracker | localStorage tracker for all filed RTIs with deadlines | ✅ Live |
| C2 | Bell Alerts | In-app notification for approaching deadlines | ✅ Live |
| C3 | Browser Notifications | Push notification for RTI deadlines | ✅ Live |
| C4 | Telegram Reminders | Bot sends deadline reminders via Telegram | ✅ Live |
| C5 | Star Rating Feedback | 1–5 star rating with hover preview | ✅ Live |
| C6 | Formspree Feedback | Feedback form submission to email | ✅ Live |
| C7 | FAQ Accordion | Help section with expandable answers | ✅ Live |
| C8 | Privacy Policy Modal | Full privacy policy in modal overlay | ✅ Live |

### Feature Set D — Telegram Bot (@RTIAssistBot)

| Command | Function |
|---------|----------|
| `/start` | Welcome message + language prompt |
| `/help` | All commands list |
| `/about` | Bot description |
| `/fee` | RTI filing fee by state |
| `/state` | Set your state |
| `/legal` | Legal tools quick access |
| `/myreminders` | View active RTI deadline reminders |

---

## 🖥️ 5. Screen Inventory

| Screen / Page | Navigation | Key Elements |
|---------------|-----------|-------------|
| RTI Generator | Default (`#home`) | Language select, State select, Text area, Submit button, Result panel |
| Legal Tools Hub | `#legaltools` | 4 tool cards with icons |
| Second Appeal | `#second-appeal` | 7-field form → Generate → Output panel |
| Consumer Complaint | `#consumer-court` | 8-field form → Generate → Output panel |
| Legal Notice | `#legal-notice` | 6-field form → Generate → Output panel |
| Labour Complaint | `#labour` | 6-field form → Generate → Output panel |
| RTI Tracker | `#tracker` | Add RTI form, RTI list, deadline countdown badges |
| Settings | `#settings` | Telegram setup, Notifications, Feedback, FAQ, Privacy |
| Privacy Modal | Overlay (z-index 2000) | Full privacy policy text, close button |

---

## 🔄 6. Key User Flows

### Flow 1 — Generate RTI Application
```
User opens app
  → Selects Language (default: English)
  → Selects State (optional; blank = Central Govt)
  → Types: "My ration card application was rejected 3 months ago..."
  → Clicks "Generate RTI"
  → Loading indicator (AI: 2–8s / Demo: <1s)
  → Result panel shows:
      ├── Complete RTI draft (copy button)
      ├── Quality Score (0–100)
      ├── Filing instructions
      ├── Department & Ministry identified
      ├── Exemption risk level
      └── Estimated success probability
```

### Flow 2 — File Second Appeal
```
User → Legal Tools → Second Appeal
  → Fills: Name, RTI Date, First Appeal Date, Department, Query, Reason
  → Clicks "Generate Second Appeal"
  → Formal CIC letter generated with all legal sections cited
  → User prints and files at CIC or edaakhil.nic.in
```

### Flow 3 — Set Telegram Reminder
```
User → Settings → Telegram Setup
  → Enters Telegram username
  → Clicks "Set Reminder"
  → Bot sends 7-day, 3-day, 1-day deadline alerts automatically
  → /myreminders command shows all active reminders
```

### Flow 4 — Track RTI Deadline
```
User files RTI → Adds to Tracker
  → Enters: Department, Date Filed, Notes
  → Tracker auto-calculates 30-day response deadline
  → Bell icon lights when < 7 days remain
  → Browser push notification fires when < 3 days remain
```

---

## 📈 7. Success Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Applications Generated | Total RTI drafts created | 10,000 / month |
| Quality Score Avg | Average score across all generated RTIs | ≥ 80 / 100 |
| Language Diversity | % of drafts in non-English languages | ≥ 40% |
| Telegram Bot Users | Active users on @RTIAssistBot | 500 / month |
| Legal Tool Usage | Total legal documents generated | 2,000 / month |
| Feedback Rating | Average star rating from users | ≥ 4.0 / 5.0 |
| API Response Time | Time to return RTI draft (AI mode) | < 8 seconds |
| Demo Mode Uptime | HF Space availability | ≥ 99% |

---

## 🚫 8. Out of Scope

| Out of Scope | Reason |
|-------------|--------|
| User login / authentication | Privacy-first design — no accounts |
| Storing user data on server | All data is localStorage-only |
| Auto-filing RTI on govt portals | Legal liability; user must file manually |
| Providing legal advice | Tool generates documents, not legal counsel |
| Tracking RTI response from govt | No access to govt portal APIs |
| Paid premium features | Product is 100% free |
| Document OCR / upload | Not in roadmap for v2 |
| Court-ready filing for complex cases | Documents need advocate review for those |

---

## 🚀 9. Development Phases

| Phase | Name | Features | Status |
|-------|------|----------|--------|
| **v0.1** | MVP | Basic RTI generator (English only), FastAPI backend | ✅ Done |
| **v0.5** | Multi-language | 11 Indian languages, State selector | ✅ Done |
| **v1.0** | Bot Launch | Telegram bot @RTIAssistBot, all 7 commands | ✅ Done |
| **v1.5** | Legal Tools | 4 legal document generators | ✅ Done |
| **v2.0** | Settings + UX | Tracker, Notifications, Feedback, Privacy, Star rating | ✅ Done |
| **v2.5** | Deploy | HF Space, GitHub Pages, BotFather commands | 🔄 In Progress |
| **v3.0** | AI Upgrade | Switch demo mode to full ASI-1 AI on all tools | 📋 Planned |
| **v3.5** | CIC Direct | One-click filing to RTI portals | 📋 Future |

---

## 🔒 10. Privacy & Safety

| Concern | Policy |
|---------|--------|
| **User Data** | No user data stored on any server. All RTI history in browser localStorage only |
| **API Calls** | Input text sent to ASI-1 API for processing — no PII stored |
| **Telegram Bot** | Stores only chat_id + reminder data in memory (not database) — cleared on restart |
| **Feedback Form** | Formspree handles form data — RTIAssist does not store it |
| **Cookies** | No tracking cookies. No analytics scripts |
| **Privacy Policy** | Full Privacy Policy available in-app (Settings → Privacy Policy) |
| **Generated Documents** | Templates only — user responsible for accuracy of their details |
| **Minors** | No age restriction; tool is informational and free |

---

## ✅ 11. Definition of Done

A feature is considered **Done** when:

- [ ] Works correctly in `index_Version4.html` (no JS/CSS errors in console)
- [ ] Works on mobile (responsive layout tested)
- [ ] Works in all 11 language modes
- [ ] API endpoint returns correct response (if backend involved)
- [ ] Edge cases handled (empty input, network failure, API error)
- [ ] README / relevant docs updated
- [ ] Committed and pushed to `main` branch
- [ ] Tested on live HF Space URL

---

## 🎨 12. Design System

| Element | Value |
|---------|-------|
| **Primary Color** | `#00A86B` (Emerald Green — RTI brand) |
| **Secondary Color** | `#6B21A8` (Deep Purple — Legal Tools) |
| **Background** | `#0A0A0A` (Near Black) |
| **Surface / Card** | `#111827` (Dark Card) |
| **Text Primary** | `#FFFFFF` |
| **Text Secondary** | `rgba(255,255,255,0.65)` |
| **Font Family** | `DM Sans` (body), `Nunito` (headers) |
| **Border Radius** | `12px` (cards), `8px` (inputs), `50px` (pills) |
| **RTI Gradient** | `linear-gradient(135deg, #00A86B, #059669)` |
| **Legal Gradient** | `linear-gradient(135deg, #6B21A8, #9333EA)` |
| **Mobile Break** | `≤ 480px` |
| **Z-Index Layers** | Base: 1, Nav: 100, Lang Modal: 500, Privacy Modal: 2000 |

---
---

# PART 2 — TECHNICAL REQUIREMENTS DOCUMENT (TRD)

---

## 📄 1. Document Overview

| Field | Details |
|-------|---------|
| **Document Type** | Technical Requirements Document (TRD) |
| **System** | RTIAssist — Backend API + Frontend + Telegram Bot |
| **Backend Language** | Python 3.10 |
| **Frontend** | Vanilla HTML5 / CSS3 / JavaScript (ES6+) — no framework |
| **API Framework** | FastAPI |
| **AI Model** | ASI-1 (`asi1-mini`) by Fetch.ai |
| **Deployment** | Hugging Face Spaces (Docker) + Render (Telegram Bot) |
| **Port** | 7860 (HF Spaces default) |
| **Repo** | https://github.com/shlok926/rtiassist-api |

---

## 🏗️ 2. System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                            │
│                                                                  │
│   index_Version4.html              @RTIAssistBot (Telegram)      │
│   (Vanilla JS, no framework)       (python-telegram-bot v20)     │
└──────────────────┬──────────────────────────┬────────────────────┘
                   │ HTTP REST                │ Webhook POST
                   ▼                          ▼
┌──────────────────────────────────────────────────────────────────┐
│                      API LAYER  (FastAPI)                        │
│                                                                  │
│   POST /rti/generate          POST /legal/generate               │
│   GET  /health                POST /telegram  (webhook)          │
│                                                                  │
│   main.py — lifespan, CORS, router registration                  │
└──────────────────┬───────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                 AI PIPELINE  (4 Agents)                          │
│                                                                  │
│  Layer 1: IntentClassifier  → department, ministry, urgency      │
│  Layer 2: PIOResolver       → PIO address, fee, portal URL       │
│  Layer 3: DraftGenerator    → Full RTI application text          │
│  Layer 4: QualityChecker    → Score 0–100, warnings, risk        │
└──────────────────┬───────────────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
│                                                                  │
│  ASI-1 API  (api.asi1.ai)      Formspree  (feedback form)        │
│  Telegram Bot API              Render  (bot server hosting)      │
│  Hugging Face Spaces           Browser Notifications API         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ 3. Technology Stack

### Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.10 | Core backend runtime |
| Web Framework | FastAPI | latest | REST API + webhook server |
| ASGI Server | Uvicorn | latest | Production HTTP server |
| Data Validation | Pydantic v2 | latest | Request/Response schemas |
| HTTP Client | requests | latest | ASI-1 API calls |
| Bot Framework | python-telegram-bot | v20 | Telegram webhook bot |
| PDF Generation | reportlab | latest | Document export (future) |
| Config | python-dotenv | latest | Environment variables |
| Testing | pytest + httpx | latest | API unit tests |

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Markup | HTML5 | Structure |
| Styling | CSS3 (custom — no framework) | Design system |
| Logic | Vanilla JavaScript ES6+ | All interactivity |
| Persistence | localStorage API | RTI Tracker, preferences, ratings |
| Notifications | Web Notifications API | Browser push alerts for deadlines |
| Fonts | Google Fonts (DM Sans, Nunito) | Typography |
| Icons | Emoji (no external icon lib) | Lightweight, no dependency |
| Form Submission | Formspree API (AJAX) | User feedback emails |

### Infrastructure

| Service | Platform | Purpose |
|---------|---------|---------|
| API + Frontend | Hugging Face Spaces | Main hosting — FastAPI on Docker |
| Telegram Bot | Render (free) | bot_server.py running separately |
| Container | Docker (python:3.10-slim) | HF Spaces Docker deployment |
| Code Hosting | GitHub | Source control, CI via push |
| Process Manager | start.sh (bash) | Starts uvicorn + sets env on HF |

---

## 🗄️ 4. Database Schema

> RTIAssist uses **no server-side database**. All user data lives in browser localStorage.

### localStorage Schema (Client-Side)

```javascript
// RTI Tracker entries
localStorage["rti_tracker"] = JSON.stringify([
  {
    id: "rti_1706000000000",           // timestamp-based unique ID
    department: "PWD Maharashtra",     // department name
    filed_date: "2026-01-15",          // ISO date string
    subject: "Road repair status",     // brief subject
    notes: "Filed via post",           // optional user notes
    status: "pending",                 // pending | replied | appealed | closed
    deadline: "2026-02-14",            // auto-calculated: filed_date + 30 days
    reminder_sent: false               // browser notification flag
  }
]);

// User preferences
localStorage["rti_language"]    = "hindi";       // selected UI language
localStorage["rti_state"]       = "Maharashtra"; // selected state for RTI
localStorage["telegram_user"]   = "@username";   // Telegram username for reminders
localStorage["notif_enabled"]   = "true";        // browser notifications toggle
localStorage["feedback_rating"] = "4";           // last star rating submitted
```

### Server-Side Data (In-Memory Only — NOT persisted)

```python
# telegram_bot.py
reminders: dict[int, list[dict]] = {
    chat_id: [
        {
            "department": str,
            "filed_date": str,
            "deadline": str,
            "notified_7": bool,   # 7-day alert sent?
            "notified_3": bool,   # 3-day alert sent?
            "notified_1": bool    # 1-day alert sent?
        }
    ]
}
# ⚠️ Cleared on every server restart — intentional (privacy-first)
```

---

## 🔌 5. API Design

### Base URL
```
Production:  https://visgrow-03-rtiassist-api.hf.space
Local Dev:   http://localhost:7860
Swagger UI:  http://localhost:7860/docs
```

### `GET /health`
```json
Response 200:
{
  "status": "healthy",
  "version": "2.0.0",
  "model": "asi1-mini",
  "endpoints": ["/rti/generate", "/legal/generate", "/health"]
}
```

### `POST /rti/generate`
```json
Request Body:
{
  "description": "string (20–2000 chars) — required",
  "language": "english | hindi | marathi | tamil | telugu | kannada | bengali | gujarati | punjabi | malayalam | odia",
  "state": "Maharashtra | null (= Central Govt)",
  "demo_mode": true | false | null
}

Response 200:
{
  "draft": "Complete RTI application text (ready to file)...",
  "filing_instructions": "Step-by-step guide...",
  "department": "Food and Civil Supplies Department",
  "ministry": "Ministry of Consumer Affairs...",
  "government_level": "state | central",
  "information_needed": "Detailed description of info sought...",
  "urgency": "routine | urgent | life_threatening",
  "pio_details": { "pio_designation": "...", "address_format": "...", "filing_fee": "₹10", ... },
  "quality_score": 85,
  "is_valid": true,
  "warnings": [],
  "suggestions": ["Add application number if available"],
  "exempt_risk": "none | low | medium | high",
  "estimated_success_probability": "High | Medium | Low",
  "confidence": 0.92
}

Errors:
  422 — description < 20 chars or > 2000 chars
  500 — AI API failure (with error detail)
```

### `POST /legal/generate`
```json
Request Body:
{
  "tool": "second_appeal | consumer_complaint | legal_notice | labour_complaint",
  "name": "string",
  "department": "string",        // second_appeal
  "query": "string",             // second_appeal
  "rti_date": "DD/MM/YYYY",      // second_appeal
  "appeal_date": "DD/MM/YYYY",   // second_appeal
  "reason": "no_response | incomplete | denied | wrong_info | partial | delay",
  "company": "string",           // consumer_complaint
  "address": "string",
  "type": "string",              // varies by tool
  "description": "string",
  "amount": "string",
  "purchase_date": "DD/MM/YYYY",
  "relief": "refund | replacement | compensation | all",
  "sender": "string",            // legal_notice
  "recipient": "string",         // legal_notice
  "employer": "string",          // labour_complaint
  "state": "string"              // labour_complaint
}

Response 200:
{
  "draft": "Full legal document text...",
  "tool": "second_appeal",
  "status": "success"
}

Errors:
  400 — Required fields missing (field name specified)
  422 — Validation error
```

**Required Fields per Tool:**

| Tool | Required Fields |
|------|----------------|
| `second_appeal` | `name`, `department`, `query` |
| `consumer_complaint` | `name`, `company`, `description` |
| `legal_notice` | `sender`, `recipient`, `description` |
| `labour_complaint` | `name`, `employer`, `description` |

---

## 🔐 6. Security & Rate Limiting

### Endpoint Authentication

| Endpoint | Auth | Type |
|----------|------|------|
| `GET /health` | None | Public |
| `POST /rti/generate` | None | Public (platform rate-limited) |
| `POST /legal/generate` | None | Public (platform rate-limited) |
| `POST /telegram` | Telegram token validation | Webhook |

### Environment Secrets (Never Commit)
```bash
ASI1_API_KEY=         # ASI-1 model API key
TELEGRAM_TOKEN=       # Telegram BotFather token
WEBHOOK_URL=          # Full webhook URL for Telegram
SPACE_HOST=           # Auto-set by HF Spaces platform
DEMO_MODE=true        # true = bypass AI calls (HF default)
```

### Security Implementation

| Layer | Measure | How |
|-------|---------|-----|
| Input | Length validation | Pydantic `min_length=20`, `max_length=2000` |
| Input | Type validation | Pydantic BaseModel — all fields typed |
| Secrets | API key protection | `python-dotenv` — never logged or exposed |
| Retries | Rate limit handling | Exponential backoff on HTTP 429 (3 attempts, 2^n wait) |
| SQL injection | Not applicable | No SQL database used |
| XSS | Output safety | Frontend uses `textContent` not `innerHTML` for user input display |
| CORS | Open (public API) | `CORSMiddleware` allow all origins |
| Telegram | Webhook integrity | `python-telegram-bot` validates token on every update |
| File upload | Not applicable | No file upload endpoints exist |

---

## 🤖 7. AI Integration

### Model Details

| Field | Value |
|-------|-------|
| Provider | Fetch.ai — ASI-1 |
| Model ID | `asi1-mini` |
| API Endpoint | `https://api.asi1.ai/v1/chat/completions` |
| Auth Header | `Authorization: Bearer {ASI1_API_KEY}` |
| Protocol | OpenAI-compatible chat completions |
| Streaming | `false` |
| Timeout | 30 seconds per request |

### 4-Layer AI Pipeline

```
Input: "My ration card was rejected 3 months ago..."
         │
         ▼
┌──────────────────────────────────────────────────────┐
│ Layer 1 — IntentClassifier                           │
│ Temperature: 0.2 (low — deterministic output)        │
│ Max tokens: 500                                      │
│ Output: department, ministry, urgency,               │
│         government_level, confidence (0.0–1.0)       │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ Layer 2 — PIOResolver                                │
│ (Lookup dict — no AI call needed)                    │
│ Output: pio_designation, address, fee,               │
│         online_portal, response_timeline             │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ Layer 3 — DraftGenerator                             │
│ Temperature: 0.3                                     │
│ Max tokens: 1500                                     │
│ Output: Full RTI draft in requested language         │
│         + step-by-step filing instructions           │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│ Layer 4 — QualityChecker                             │
│ Temperature: 0.1 (very deterministic)                │
│ Max tokens: 400                                      │
│ Output: quality_score (0–100), is_valid,             │
│         warnings[], suggestions[],                   │
│         exempt_risk, success_probability             │
└──────────────────────────────────────────────────────┘
         │
         ▼
Final: RTIResponse JSON returned to client
```

### Demo Mode Behaviour
When `DEMO_MODE=true`:
- All 4 AI layers are **bypassed entirely**
- Pre-written high-quality sample responses returned per scenario
- Response time: ~200ms (vs 2–8s for AI mode)
- All legal tools always run as demo (deterministic template filling, no AI needed)
- Enabled by default on HF Space to avoid API cost on free tier

### Error Handling

| Error | Handling |
|-------|---------|
| HTTP 429 (rate limit) | Exponential backoff: wait 2, 4, 8 seconds, max 3 retries |
| HTTP 5xx (server error) | Same retry logic |
| `JSONDecodeError` | Fallback response returned with `confidence: 0.3` |
| `EnvironmentError` (no API key) | HTTP 500 with clear error message |
| Timeout (30s exceeded) | `requests.exceptions.Timeout` — caught and returned as 500 |

---

## 🚀 8. Deployment Strategy

### Architecture

```
GitHub (main branch)
    │
    ├── Hugging Face Spaces  (Docker auto-deploy on push)
    │       └── FastAPI  (port 7860)
    │           ├── /rti/generate
    │           ├── /legal/generate
    │           ├── /health
    │           └── /telegram  (Telegram webhook receiver)
    │
    └── Render  (deploy via render.yaml)
            └── bot_server.py  (Telegram-only server)
                └── Calls HF Space API at /rti/generate
```

### Dockerfile (HF Spaces)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 7860
ENV PORT=7860
ENV HOST=0.0.0.0
ENV DEMO_MODE=true
CMD ["/app/start.sh"]
```

### render.yaml (Telegram Bot)
```yaml
services:
  - type: web
    name: rtiassist-bot
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot_server.py
    plan: free
    envVars:
      - key: TELEGRAM_TOKEN
      - key: ASI1_API_KEY
      - key: API_BASE
        value: https://visgrow-03-rtiassist-api.hf.space
      - key: WEBHOOK_URL
```

### Required Environment Variables

| Variable | Needed On | Description |
|---------|----------|-------------|
| `ASI1_API_KEY` | HF + Render | ASI-1 model access key |
| `TELEGRAM_TOKEN` | HF + Render | BotFather token for @RTIAssistBot |
| `WEBHOOK_URL` | HF Spaces | Full HTTPS URL for Telegram webhook |
| `SPACE_HOST` | HF Spaces | Auto-set by HF platform |
| `DEMO_MODE` | HF Spaces | `true` = bypass live AI calls |

### Planned: GitHub Pages
- Rename `index_Version4.html` → `index.html`
- Enable GitHub Pages: Settings → Pages → Branch: `main` → Root
- Public URL: `https://shlok926.github.io/rtiassist-api`

---

## ⚡ 9. Performance Requirements

| Metric | Target | Current State |
|--------|--------|--------------|
| RTI Generation — AI mode | < 8 seconds | Not enabled on HF yet |
| RTI Generation — Demo mode | < 1 second | ✅ ~200ms |
| Legal Doc Generation | < 1 second | ✅ ~100ms |
| `/health` response | < 100ms | ✅ ~50ms |
| Frontend initial load | < 2 seconds | ✅ ~800ms (single HTML file) |
| Telegram bot response | < 3 seconds | ✅ ~1s |
| HF Space cold start | < 30 seconds | ~15–20s |
| localStorage read/write | < 10ms | ✅ |
| Browser notification trigger | Immediate | ✅ |

### Why Performance is Good
- Frontend is a **single HTML file** — no bundle, no framework overhead
- No external JS framework (React/Vue/Angular) — pure vanilla JS
- No tracking/analytics scripts loaded
- Google Fonts loaded async (non-blocking)
- localStorage instead of IndexedDB for simplicity (< 5MB total data)
- Demo mode makes API free-tier viable with no AI latency

---

## 💰 10. Cost Estimate

| Service | Plan | Monthly Cost (INR) |
|---------|------|-------------------|
| Hugging Face Spaces | Free (CPU Basic) | ₹0 |
| Render (Bot Server) | Free tier | ₹0 |
| GitHub | Free (public repo) | ₹0 |
| ASI-1 API — Demo mode | No calls made | ₹0 |
| ASI-1 API — AI mode (10k req) | ~₹0.002/req | ~₹2,000 |
| Formspree | Free (50 forms/mo) | ₹0 |
| Telegram Bot API | Free | ₹0 |
| Domain (optional) | Custom `.in` domain | ~₹700/year |
| **Current Total** | | **₹0 / month** |
| **Scaled (AI mode, 10k/mo)** | | **~₹2,000 / month** |

---

## 📋 11. Development Checklist

### Backend
- [x] FastAPI app with lifespan context manager
- [x] CORS middleware configured
- [x] `POST /rti/generate` with Pydantic validation
- [x] `POST /legal/generate` (4 tools: second_appeal, consumer, notice, labour)
- [x] `GET /health` endpoint
- [x] 4-layer AI pipeline (Classify → Resolve → Draft → Check)
- [x] Demo mode for all endpoints
- [x] ASI-1 HTTP client with exponential backoff retry
- [x] Telegram bot webhook (7 commands + callback + message handler)
- [x] `/myreminders` with active deadline tracking
- [x] `.env` + `python-dotenv` config
- [x] Dockerfile for HF Spaces (python:3.10-slim, port 7860)
- [x] render.yaml for Render bot deployment
- [ ] Enable AI mode on HF Space (need ASI1_API_KEY in HF secrets)
- [ ] App-level rate limiting middleware
- [ ] Persistent storage for Telegram reminders (database)

### Frontend (`index_Version4.html`)
- [x] RTI Generator — language selector, state selector, text area
- [x] 11 language support (Hindi, English, Marathi, Tamil, Telugu, Kannada, Bengali, Gujarati, Punjabi, Malayalam, Odia)
- [x] All 28 states + Central Government support
- [x] Legal Tools hub + 4 individual tool pages
- [x] RTI Tracker (localStorage, add/delete/status update)
- [x] Bell alert for approaching RTI deadlines
- [x] Browser push notifications (Web Notifications API)
- [x] Settings page with all sections
- [x] Telegram reminder setup UI
- [x] Star rating 1–5 with hover preview (CSS `~` bug fixed, JS IIFE added)
- [x] Formspree feedback form (AJAX submit)
- [x] FAQ accordion (expand/collapse)
- [x] Privacy Policy modal (z-index 2000)
- [x] Responsive mobile layout (≤480px)
- [ ] GitHub Pages deploy (rename to `index.html`, enable Pages)

### Documentation
- [x] `README.md` — Technical quick-start
- [x] `RTI_PRODUCT_OVERVIEW.md` — Full RTI education + use cases
- [x] `LEGAL_TOOLS_GUIDE.md` — 4 legal tools step-by-step
- [x] `RTIAssist_PRD_TRD.md` — This file (PRD + TRD)
- [x] `DEPLOYMENT.md` — Deploy guide
- [ ] BotFather `/setcommands` (manual Telegram step)

---

## 🤝 12. Acceptance Criteria

### RTI Generator

| Scenario | Expected Result |
|---------|----------------|
| Valid description (≥20 chars) entered | RTI draft returned, `quality_score ≥ 60` |
| Description < 20 chars submitted | HTTP 422 validation error |
| Hindi language selected | RTI draft in Devanagari script |
| State selected as Maharashtra | PIO address reflects Maharashtra office |
| AI API is down | Demo mode fallback kicks in, response still returned |
| Network error on frontend | Error message shown with retry guidance |
| `exempt_risk = high` | Warning banner shown in result panel |

### Legal Tools

| Scenario | Expected Result |
|---------|----------------|
| All required fields filled | Document generated in < 1 second |
| Required field missing | HTTP 400 — specific missing field named in error |
| Second Appeal — `reason = no_response` | Document cites RTI Act Section 7(1) |
| Consumer Complaint — `amount = 45000` | Compensation = ₹22,500 (50% of claim) |
| Labour — `type = pf_not_deposited` | Document cites EPF Act Section 14A/14B |

### Telegram Bot

| Scenario | Expected Result |
|---------|----------------|
| User sends `/start` | Welcome message in ≤ 2 seconds |
| User sends `/myreminders` (none set) | "No active reminders found" message |
| RTI deadline exactly 3 days away | Bot sends proactive reminder automatically |
| Unknown command sent | Help text with all valid commands returned |
| `/fee` command sent | State-wise RTI fee table displayed |

### Deployment

| Check | Pass Criteria |
|-------|--------------|
| HF Space `/health` returns 200 | `status: "healthy"` in response |
| Telegram webhook registered | Bot responds to messages within 3s |
| Demo mode enabled | RTI generated without AI API key |
| Mobile layout rendered | No horizontal scroll on 375px viewport |

---

### Commit Message Convention
```
feat:     New feature added
fix:      Bug fix
docs:     Documentation only (no code change)
style:    CSS/formatting (no logic change)
refactor: Code restructure (no feature change)
test:     Adding or updating tests
chore:    Build, deploy, config changes
```

### Branch Strategy
```
main          ← always deployable (production)
  └── feature/[name]    ← new features
  └── fix/[name]        ← bug fixes
  └── docs/[name]       ← documentation only
```

---

*RTIAssist — Built for 1.4 billion Indians who deserve to know.*
*PRD + TRD Document — Version 2.0 | March 2026*
