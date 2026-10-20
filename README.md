<div align="center">

<img src="https://raw.githubusercontent.com/shlok926/rtiassist-api/main/rtiassist_logo.png" alt="RTIAssist Logo" width="280"/>

### RTIAssist: AI-Powered RTI, Legal Tools and Case Lifecycle Platform

[Live Demo](https://shlok926.github.io/rtiassist-api) | [API Docs](#api-reference) | [Telegram Bot](#telegram-bot-integration) | [Quick Start](#quick-start) | [Contributing](CONTRIBUTING.md) | [Changelog](CHANGELOG.md)

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![ASI-1](https://img.shields.io/badge/Powered%20by-ASI--1%20API-6B46C1)](https://asi1.ai)
[![React](https://img.shields.io/badge/Frontend-React%2019%20%2B%20Vite-61DAFB?logo=react&logoColor=black)](src/)
[![Tests](https://img.shields.io/badge/Tests-117%20Passing-brightgreen?logo=pytest&logoColor=white)](tests/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE.md)

> India's legal-tech platform for automated Right to Information (RTI) drafting, Public Information Officer (PIO) authority resolution, statutory deadline tracking, and appeal generation.

Detailed product specifications and RTI guide: [Product Overview and Legal Guide](docs/RTI_PRODUCT_OVERVIEW.md)

</div>

---

## Overview

Over 65 million RTI applications are filed annually across India. Citizens and advocacy groups face systemic bottlenecks when exercising their rights under the RTI Act, 2005:

- **Public Authority Identification**: Identifying whether an issue falls under Central, State, or Municipal jurisdiction, and locating the competent PIO.
- **Statutory Drafting Requirements**: Applications must formulate clear questions and request specific records without requesting opinions or attracting Section 8 exemptions.
- **Language Barriers**: Legal portals and forms frequently restrict communication to formal Hindi or English.
- **Strict Appeal Timelines**: Citizens regularly forfeit rights due to unmonitored statutory deadlines (30-day First Appeal under Section 19(1) and 90-day Second Appeal under Section 19(3)).
- **Arbitrary Rejections**: Citizens lack accessible legal tools to analyze denial orders and challenge non-disclosure.

RTIAssist automates this entire lifecycle in 11 Indian languages, from problem definition to final statutory appeal.

---

## System Architecture

The following diagram illustrates the multi-tier system architecture:

```mermaid
graph TB
    subgraph ClientTier["Client Tier"]
        WebUI["React 19 Web Workspace<br/>(Vite, Tailwind CSS)"]
        TgClient["Telegram Messenger<br/>(Mobile / Desktop Client)"]
    end

    subgraph IngressTier["Ingress & Gateway Tier"]
        FastAPIApp["FastAPI Application Core"]
        AuthModule["JWT Auth & Security Guard<br/>(Native Bcrypt)"]
        TgWebhook["Telegram Webhook Receiver"]
    end

    subgraph ServiceTier["Core Application Services"]
        AIEngine["4-Layer AI Pipeline Engine"]
        CaseEngine["Case Lifecycle Engine"]
        AuthService["Authority Resolution Service"]
        DeadlineEngine["Statutory Deadline Calculator"]
        OCREngine["OCR & Document Parser"]
        SourceMonitor["Source Intelligence & Monitor"]
    end

    subgraph IntegrationTier["Inference & External Services"]
        ASI1["Fetch.ai ASI-1 API<br/>(asi1-mini Reasoning Model)"]
        TgBotAPI["Telegram Bot API"]
        GovPortals["Official Government Portals"]
    end

    subgraph PersistenceTier["Persistence Tier"]
        SQLAlchemyORM["SQLAlchemy ORM & Repositories"]
        Database[(SQLite Database<br/>rtiassist.db)]
    end

    WebUI -->|HTTP / JSON| FastAPIApp
    TgClient -->|Webhook Updates| TgWebhook
    TgWebhook --> FastAPIApp
    FastAPIApp --> AuthModule
    AuthModule --> ServiceTier
    
    AIEngine -->|Prompts & Inference| ASI1
    DeadlineEngine -->|Push Notifications| TgBotAPI
    SourceMonitor -->|Health & Schema Check| GovPortals
    
    ServiceTier --> SQLAlchemyORM
    SQLAlchemyORM --> Database
```

---

## Live End-to-End Workflow

The sequence below illustrates the live lifecycle of a citizen query from submission through draft generation, filing, and statutory appeal escalation:

```mermaid
sequenceDiagram
    autonumber
    actor Citizen as Citizen / User
    participant Client as Web App / Telegram Bot
    participant API as FastAPI Backend
    participant Pipeline as 4-Layer AI Pipeline
    participant DB as SQLite Repositories
    participant Scheduler as Deadline & Reminder Engine

    Citizen->>Client: Submits grievance in plain language (1 of 11 languages)
    Client->>API: POST /rti/generate (description, state, language)
    
    rect rgb(240, 248, 255)
        Note over API,Pipeline: 4-Layer AI Pipeline Execution
        API->>Pipeline: Layer 1: Classify Intent & Extract Case Facts
        Pipeline-->>API: Facts JSON & Recommended Action
        API->>DB: Layer 2: Resolve Public Authority & Competent PIO
        DB-->>API: Authority Metadata, Filing Fee, Portal URL
        API->>Pipeline: Layer 3: Generate Structured RTI Draft
        Pipeline-->>API: Section-Compliant RTI Draft
        API->>Pipeline: Layer 4: Audit Draft Quality & Sec 8 Risk
        Pipeline-->>API: Quality Score (0-100) & Risk Summary
    end

    API->>DB: Store Case (Status: DRAFTED)
    API-->>Client: Return Structured JSON (Draft, PIO, Fee, Score)
    Client-->>Citizen: Displays Preview, PDF Download, WhatsApp Share

    Note over Citizen,Client: Citizen files application with Public Authority
    Citizen->>Client: Confirms filing & inputs post receipt / acknowledgement
    Client->>API: POST /cases/{id}/status (FILED, tracking_no)
    API->>Scheduler: Compute Statutory 30-Day Response Window
    Scheduler->>DB: Register First Appeal Deadline Record

    opt Authority Rejects or Fails to Respond (After 30 Days)
        Scheduler-->>Client: Trigger Proactive Deadline Alert
        Citizen->>Client: Uploads Rejection Letter / Notice (PDF/Image)
        Client->>API: POST /pdf/analyze & /cases/{id}/appeal
        API->>Pipeline: Parse Rejection Order & Frame Grounds of Appeal
        Pipeline-->>API: Formatted First Appeal Petition (Section 19(1))
        API->>Scheduler: Compute 90-Day Second Appeal Window
        API-->>Client: Returns Formatted Appeal Document
    end
```

---

## Database Architecture

The entity-relationship model enforces strict user case isolation, lifecycle tracking, public authority registries, and statutory deadlines:

```mermaid
erDiagram
    USERS ||--o{ CASES : owns
    CASES ||--o{ DOCUMENTS : contains
    CASES ||--o{ FILINGS : tracks
    CASES ||--o{ DEADLINES : schedules
    CASES ||--o{ APPEALS : escalates
    CASES ||--o{ CASE_EVENTS : audits
    CASES ||--o{ RESPONSE_ANALYSIS : analyzes
    AUTHORITIES ||--o{ CASES : assigned_to
    AUTHORITIES ||--o{ OFFICIAL_SOURCES : verified_by

    USERS {
        string id PK
        string email UK
        string password_hash
        string telegram_id UK
        string first_name
        string last_name
        string role
        boolean is_active
        datetime created_at
    }

    CASES {
        string id PK
        string user_id FK
        string authority_id FK
        string title
        string problem_description
        string status
        string priority
        string recommended_action
        string case_objective
        string extracted_facts
        datetime created_at
        datetime updated_at
    }

    AUTHORITIES {
        string id PK
        string name
        string jurisdiction
        string state
        string pio_name
        string pio_address
        string filing_fee
        string portal_url
        string active_status
    }

    DOCUMENTS {
        string id PK
        string case_id FK
        string doc_type
        string content
        string language
        integer quality_score
        datetime created_at
    }

    FILINGS {
        string id PK
        string case_id FK
        string filing_mode
        string tracking_number
        datetime filed_at
    }

    DEADLINES {
        string id PK
        string case_id FK
        string deadline_type
        datetime due_date
        string status
        boolean reminder_sent
    }

    APPEALS {
        string id PK
        string case_id FK
        string appeal_type
        string appellate_authority
        string appeal_grounds
        string status
        datetime created_at
    }

    RESPONSE_ANALYSIS {
        string id PK
        string case_id FK
        string parsed_text
        string rejection_grounds
        string appeal_viable
    }

    CASE_EVENTS {
        string id PK
        string case_id FK
        string event_type
        string description
        datetime created_at
    }

    OFFICIAL_SOURCES {
        string id PK
        string authority_id FK
        string source_url
        string verification_status
        datetime last_scraped_at
    }
```

---

## Core Capabilities

- **4-Layer AI Pipeline**:
  - *Layer 1 (Intent)*: Determines whether RTI, Consumer Forum, Labour Court, or Grievance Portal is the appropriate legal mechanism.
  - *Layer 2 (PIO Resolver)*: Matches query context against 700+ Central and State authority departments.
  - *Layer 3 (Drafter)*: Assembles questions adhering to Section 6(1) drafting principles without requesting opinions.
  - *Layer 4 (Quality Scorer)*: Evaluates risk against Section 8 exemption clauses (defense, trade secrets, personal privacy) and assigns a score from 0 to 100.
- **Language Support**: Native drafting across 11 languages: English, Hindi, Tamil, Telugu, Kannada, Bengali, Gujarati, Marathi, Punjabi, Malayalam, and Odia.
- **End-to-End Case Progression**: Full tracking across states: `UNDERSTANDING` -> `DRAFTED` -> `FILED` -> `PENDING_RESPONSE` -> `FIRST_APPEAL` -> `SECOND_APPEAL`.
- **OCR and Rejection Parsing**: Upload rejection notices to isolate specific rejection clauses cited by authorities and auto-populate appeal templates.
- **Proactive Deadline Alerts**: Real-time statutory deadline monitoring with push alerts at 7 days and 1 day prior to expiry.
- **Enterprise Security**: Native `bcrypt` password hashing, token-based JWT authentication, rate limiting, and case data isolation.

---

## Tech Stack

| Layer | Component | Description |
|---|---|---|
| **Frontend** | React 19, Vite 8, Tailwind CSS | Client workspace with responsive forms and document export |
| **Backend** | FastAPI, Python 3.10+, Uvicorn | High-concurrency async REST API and webhook endpoints |
| **AI Inference** | Fetch.ai ASI-1 API (`asi1-mini`) | High-speed LLM reasoning pipeline |
| **Data & ORM** | SQLAlchemy, SQLite, Alembic | Relational storage with repository abstraction |
| **Security** | Native Bcrypt, PyJWT | Cryptographic password verification and bearer authentication |
| **OCR & Parsing**| `pdfplumber`, PyPDFium2 | PDF ingestion, text extraction, and clause parsing |
| **Bot Gateway** | `python-telegram-bot` v20 | Webhook-driven interactive Telegram assistant |
| **Testing** | Pytest, Vitest | 117 backend integration tests and frontend component checks |

---

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Node.js 18 or higher with npm
- Git

### 1. Clone and Set Up Backend
```bash
git clone https://github.com/shlok926/rtiassist-api.git
cd rtiassist-api

# Create and activate Python virtual environment
python -m venv venv
venv\Scripts\activate       # On Linux/macOS: source venv/bin/activate

# Install backend dependencies
pip install -r requirements.txt
```

### 2. Set Up Frontend
```bash
npm install
```

### 3. Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Configure the environment variables in `.env`:
```env
ASI1_API_KEY=your_asi1_api_key_here         # Fetch.ai API key from https://asi1.ai
TELEGRAM_TOKEN=your_telegram_bot_token       # Telegram token from @BotFather (optional)
JWT_SECRET=your_secure_random_key_here
DATABASE_URL=sqlite:///./rtiassist.db
```

### 4. Run Development Servers

**Run FastAPI Backend:**
```bash
uvicorn main:app --reload --port 8000
```
API documentation is available at `http://localhost:8000/docs`.

**Run React Frontend:**
```bash
npm run dev
```
Client workspace is available at `http://localhost:5173`.

---

## Testing

Run test suites across backend and frontend:

```bash
# Execute backend test suite (117 test cases)
pytest

# Execute frontend component test suite
npm run test

# Run frontend production build check
npm run build
```

---

## Project Structure

```
rtiassist-api/
├── main.py                     # FastAPI application factory and router configuration
├── app.py                      # Alternative entry point for Hugging Face Spaces
├── start.sh                    # Container boot script
├── Dockerfile                  # Container definition
├── render.yaml                 # Render cloud deployment blueprint
├── requirements.txt            # Python dependencies
├── package.json                # Frontend dependencies and scripts
│
├── agents/                     # 4-Layer AI Pipeline
│   ├── intent_classifier.py    # Problem classification and legal mechanism routing
│   ├── pio_resolver.py         # Authority identification and directory resolution
│   ├── draft_generator.py      # Statutory RTI application draft generation
│   └── quality_checker.py      # Section 8 exemption risk analysis and quality score
│
├── routes/                     # REST API route handlers
│   ├── auth.py                 # User authentication (register, login, JWT)
│   ├── cases.py                # Case tracking, status changes, appeal triggers
│   ├── authorities.py          # Authority search and directory lookup
│   ├── admin_authorities.py    # Public authority management endpoints
│   ├── rti.py                  # Direct RTI generation endpoint
│   ├── legal.py                # Legal tools (Consumer, Labour, Legal Notice, Second Appeal)
│   └── pdf_analysis.py         # OCR upload and rejection letter parser
│
├── services/                   # Core business logic layer
│   ├── case_service.py         # Case state management and validation
│   ├── appeal_service.py       # First and Second Appeal petition generation
│   ├── authority_service.py    # Jurisdiction and fee calculation
│   ├── source_monitoring.py    # Scheduled authority status scraping
│   ├── ocr_service.py          # PDF extraction and rejection parsing
│   └── deadline_service.py     # 30-day and 90-day statutory timeline calculation
│
├── repositories/               # Data access layer
│   ├── user_repository.py      # User authentication queries
│   ├── case_repository.py      # Case storage and event logging
│   └── authority_repository.py # Authority data access
│
├── integrations/
│   └── telegram/               # Telegram bot implementation (Webhook mode)
│       ├── bot.py              # Application builder and handler wiring
│       ├── handlers.py         # Interactive commands (/start, /newcase, /cases)
│       └── identity.py         # Telegram ID to RTIAssist user mapping
│
├── src/                        # React 19 Frontend
│   ├── App.jsx                 # Citizen workspace shell
│   ├── components/             # Reusable UI modules (RTI, Legal, Tracker, Auth)
│   └── context/                # Client state management
│
├── docs/                       # Project documentation
│   ├── RTI_PRODUCT_OVERVIEW.md # Comprehensive RTI legal guide
│   ├── DESIGN_AND_TECH_STACK.md# System architecture deep-dive
│   └── DEPLOYMENT.md           # Cloud deployment instructions
│
└── tests/                      # Automated test suite (117 test cases)
    ├── test_auth.py            # Password hashing and token validation
    ├── test_cases.py           # Case state and appeal transitions
    ├── test_authorities.py     # Authority lookup tests
    ├── test_web_telegram_parity.py # Web-to-Telegram feature parity
    └── frontend/               # Vitest component test cases
```

---

## API Reference

Interactive Swagger documentation is available at `/docs` when the backend is running.

### Core Endpoints

| Category | Method | Endpoint | Description |
|---|---|---|---|
| **Authentication** | `POST` | `/auth/register` | Register user with bcrypt password hash |
| **Authentication** | `POST` | `/auth/token` | Authenticate and obtain JWT bearer token |
| **RTI Generator** | `POST` | `/rti/generate` | Generate RTI draft and PIO metadata via AI pipeline |
| **Case Lifecycle** | `POST` | `/cases/` | Create and store a new case record |
| **Case Lifecycle** | `GET` | `/cases/` | Fetch all cases belonging to authenticated user |
| **Case Lifecycle** | `POST` | `/cases/{id}/appeal` | Generate First or Second Appeal from existing case |
| **Authorities** | `GET` | `/authorities/search` | Search 700+ Public Authorities across India |
| **OCR Analysis** | `POST` | `/pdf/analyze` | Ingest rejection notice and extract grounds of appeal |
| **Legal Tools** | `POST` | `/legal/consumer-complaint` | Generate Consumer Protection Court petition |
| **Legal Tools** | `POST` | `/legal/legal-notice` | Generate formal demand notice |
| **Legal Tools** | `POST` | `/legal/labour-complaint` | Generate Labour Commission complaint |

---

## Telegram Bot Integration

The Telegram Bot operates in webhook mode alongside the FastAPI server:

- **Command Menu**:
  - `/start`: Select language and initiate case creation.
  - `/newcase`: Begin plain-language complaint ingestion.
  - `/cases`: View active cases and statutory countdowns.
  - `/help`: Detailed instructions for filing and statutory requirements.
- **Automated Deadline Notifications**: Direct messages sent 7 days and 1 day prior to First Appeal deadline expiry.

---

## Development Milestones

- **Phases 1 to 11**: 4-Layer AI Pipeline, prompt engineering, 11 Indian languages, and bot integration.
- **Phase 12**: Security architecture audit and production readiness hardening.
- **Phase 13**: Real-world case intelligence, fact extraction, and response mapping.
- **Phase 14**: React 19 citizen workspace and central UI integration.
- **Phase 15**: Scheduled source monitoring, authority seeding, and product hardening.
- **Phase 16**: Final production audit, native `bcrypt` migration, and web-telegram parity validation.

Historical release notes and phase milestones are documented in [`CHANGELOG.md`](CHANGELOG.md).

---

## Contributing

Contributions are welcome. Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for local setup instructions, code standards, and pull request guidelines.

---

## License

This project is licensed under the MIT License. See [LICENSE.md](LICENSE.md) for full terms.
