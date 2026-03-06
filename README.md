<div align="center">

<img src="rtiassist_logo.png" alt="RTIAssist Logo" width="300"/>

**RTIAssist — AI-Powered RTI & Legal Tools for Indian Citizens**

🌐 [Website](#) &nbsp;|&nbsp; 📖 [API Docs](#-api-reference) &nbsp;|&nbsp; 🤖 [Telegram Bot](#-telegram-bot) &nbsp;|&nbsp; ⚡ [Quick Start](#-quick-start) &nbsp;|&nbsp; 🤝 [Contributing](#-contributing)

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![ASI-1](https://img.shields.io/badge/Powered%20by-ASI--1%20API-6B46C1)](https://asi1.ai)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram&logoColor=white)](#-telegram-bot)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](Dockerfile)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **India's most powerful AI-powered RTI application generator.**
> Describe your problem in plain language — get a legally correct, ready-to-file RTI application in seconds.

📖 **New to RTI?** Read the [Full RTI Overview, Use Cases & Competitor Comparison →](RTI_PRODUCT_OVERVIEW.md)

</div>

---

## 🧩 Problem Statement

Over **65 million RTI applications** are filed in India every year — yet most citizens struggle to:

- Identify the **correct government department** to address
- Draft a **legally correct application** under RTI Act 2005
- Understand what information is **legally accessible** vs. exempt
- Know **how and where to file** their application
- Track **deadlines** for First Appeal (30 days) and Second Appeal (90 days)

RTIAssist solves all these problems in one tool — **free**, in **your language**, in **seconds**.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **4-Layer AI Pipeline** | Intent → PIO Resolver → Draft → Quality Check |
| 🌐 **11 Indian Languages** | Hindi, English, Tamil, Telugu, Kannada, Bengali, Gujarati, Marathi, Punjabi, Malayalam, Odia |
| 📱 **Telegram Bot** | Full RTI + Legal tools via Telegram, webhook mode |
| ⚖️ **Legal Tools** | Consumer Court, Legal Notice, Labour Complaint, Second Appeal |
| 💡 **Legal Examples Library** | 44 real-world examples with prefilled forms |
| 🎯 **Quality Score** | 0–100 score + exemption risk analysis |
| 🔔 **Deadline Alerts** | Bell icon with in-app alerts + browser push notifications |
| 🤖 **Telegram Reminders** | Bot sends deadline reminders 7 days & 1 day before deadline |
| 📋 **RTI Tracker** | Save, track, and manage all your filed RTIs locally |
| 🔗 **WhatsApp Share** | Share RTI draft directly via WhatsApp |
| 📄 **PDF Download** | Download RTI draft as PDF |
| ⭐ **User Feedback** | 5-star rating + comment form (Formspree) in Settings |
| ❓ **Help & Support** | FAQ accordion + contact options in Settings |
| 🔒 **Privacy Policy** | Full privacy policy modal in Settings |
| 🐳 **Docker Ready** | One-command deployment on any platform |

---

## 🖼️ Screenshots

> Website running at `http://localhost:8080/index_Version4.html`

| RTI Generator | Legal Tools | Telegram Bot |
|:---:|:---:|:---:|
| *(coming soon)* | *(coming soon)* | *(coming soon)* |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Engine | ASI-1 API (`asi1-mini` model) |
| Backend | FastAPI + Python 3.10 |
| Bot | Python Telegram Bot v20 |
| Data Validation | Pydantic v2 |
| Frontend | Vanilla HTML / CSS / JS |
| Deployment | Docker + Hugging Face Spaces |
| API Docs | Swagger UI (auto at `/docs`) |

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/shlok926/rtiassist-api.git
cd rtiassist-api
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and fill in:
# ASI1_API_KEY — from https://asi1.ai
# TELEGRAM_TOKEN — from @BotFather on Telegram
```

### 3. Run

```bash
# API Server + Bot (port 7860) — bot runs in webhook mode inside the API
python app.py

# Website — just open the HTML file directly in any browser
# index_Version4.html — no server needed, fully self-contained
```

---

## 📖 Usage

### Generate an RTI via Website
1. Open `http://localhost:8080/index_Version4.html`
2. Click **RTI Generator**
3. Describe your problem in plain language (any Indian language)
4. Select language + state
5. Click **Generate** — download PDF or copy your RTI draft

### Use Legal Tools
1. Click **Legal Tools** in the navbar
2. Choose: Consumer Complaint / Legal Notice / Labour Complaint / Second Appeal
3. Fill in the form (or pick from **Legal Examples Library** — 44 real-world cases)
4. Generate your legal draft instantly

### RTI Tracker
1. After generating your RTI, click **Save to Tracker**
2. Track status: Filed → Response Due → Received / First Appeal / Second Appeal
3. Set a Telegram Reminder for automatic deadline reminders

### Telegram Bot
Send `/start` to [@RTIAssistBot](https://t.me/RTIAssistBot) → choose language → pick tool → describe your problem → get your draft.

---

## 📡 API Reference

Interactive docs available at **`/docs`** (Swagger UI) when server is running.

### `POST /rti/generate`

**Request:**
```json
{
  "description": "My ration card was rejected 3 months ago. I want to know the exact reason.",
  "language": "hindi",
  "state": "Maharashtra"
}
```

**Response:**
```json
{
  "draft": "दिनांक: [दिनांक]\n\nसेवा में,\nलोक सूचना अधिकारी...",
  "department": "Food and Civil Supplies Department",
  "quality_score": 88,
  "estimated_success_probability": "high",
  "pio_details": {
    "filing_fee": "Rs. 10",
    "online_portal": "https://rtionline.gov.in"
  },
  "filing_instructions": "Step-by-step guide..."
}
```

### Legal Tool Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /legal/consumer-complaint` | Consumer Court complaint draft |
| `POST /legal/legal-notice` | Legal notice draft |
| `POST /legal/labour-complaint` | Labour department complaint |
| `POST /legal/second-appeal` | Second appeal to CIC/SIC |

---

## 🤖 Telegram Bot

**Bot Flow:**
```
/start → Choose Language → Tool Menu
                              ├── 📋 RTI Application
                              ├── ⚖️  Consumer Complaint
                              ├── 📜 Legal Notice
                              ├── 👷 Labour Complaint
                              └── 📁 Second Appeal
```

**Bot Commands:**
```
/start        — Start the bot and choose language
/help         — How to use RTIAssist
/about        — About this tool
/fee          — RTI filing fees for all states
/state        — Select your state
/legal        — Legal tools (Consumer, Appeal, etc.)
/myreminders  — View your active RTI deadline reminders
```

**Telegram Reminders:** After saving an RTI to the tracker on the website, click **"Set Reminder →"** — bot will automatically remind you 7 days and 1 day before the response deadline.

---

## 🧠 Architecture — 4-Layer AI Pipeline

```
Citizen plain-language input
         │
         ▼
┌─────────────────────┐
│  Layer 1: Intent    │  ← ASI-1 #1 — Identifies department, ministry, RTI sections
│  Classifier         │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Layer 2: PIO       │  ← ASI-1 #2 — Finds correct PIO, address, fee, portal
│  Resolver           │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Layer 3: Draft     │  ← ASI-1 #3 — Generates legally correct RTI application
│  Generator          │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Layer 4: Quality   │  ← ASI-1 #4 — Quality score, exemption risk, suggestions
│  Checker            │
└──────────┬──────────┘
           ▼
  Structured JSON Response
  ├── Complete RTI draft
  ├── Filing instructions
  ├── PIO details + portal
  ├── Quality score (0–100)
  └── Success probability
```

---

## 📁 Project Structure

```
rtiassist-api/
├── app.py                  # Entry point — starts API + bot
├── main.py                 # FastAPI app definition
├── start.sh                # Docker startup script
├── Dockerfile
├── requirements.txt
├── .env.example
│
├── routes/
│   ├── rti.py              # POST /rti/generate
│   └── legal.py            # 4 legal tool endpoints
│
├── agents/
│   ├── intent_classifier.py
│   ├── pio_resolver.py
│   ├── draft_generator.py
│   └── quality_checker.py
│
├── prompts/
│   └── system_prompts.py   # All ASI-1 system prompts
│
├── models/
│   └── schemas.py          # Pydantic request/response models
│
├── utils/
│   └── asi1_client.py      # ASI-1 API wrapper
│
├── telegram_bot.py         # Telegram bot logic
├── bot_languages.py        # Bot UI translations
│
├── index_Version4.html     # Full web frontend
├── legal_examples.js       # 44 real-world legal examples
├── ui_translations.js      # Website UI translations
└── tracker_Version2.js     # RTI tracker JS
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

**Ideas for contributions:**
- Add more Indian languages (Assamese, Konkani, Manipuri, Sindhi)
- Improve AI draft quality with more RTI Act case law
- Add more real-world RTI examples to the Examples Library
- UI improvements and mobile responsiveness
- Persistent reminder backend with database

---

## 🔮 Future Scope

- RTI Status Tracker via registered post number (auto-fetch from India Post)
- Verified PIO directory for 700+ Central Government departments
- Android/iOS mobile app
- OCR — scan rejection letters and auto-draft appeals
- Persistent Telegram reminders with database backend
- WhatsApp Bot integration
- **Gram Panchayat Complaint** — MNREGA funds misused? Road/nali not built? File formal complaint to District Collector
- **Tender Objection (CVC)** — Government tender irregularity? File CVC complaint + RTI for tender documents combo

---

## 👨‍💻 Author

**Shlok** — [@shlok926](https://github.com/shlok926)

Built with ❤️ to empower Indian citizens with their Right to Information.
Powered by **ASI-1 API** by [Fetch.ai](https://fetch.ai)

---

## ⚠️ Disclaimer

RTIAssist is an informational and productivity tool designed to help Indian citizens draft RTI applications and legal documents. It does **not** constitute legal advice. Key points:

- Always **verify the PIO name and address** before filing — officers change frequently
- Generated drafts should be **reviewed before submission**
- RTIAssist is **not liable** for outcomes of filed applications
- For complex legal matters, consult a qualified RTI activist or advocate
- Information about Section 8 exemptions is indicative — final decisions rest with PIOs and Information Commissions
- **BPL cardholders are exempt from filing fees** — carry BPL card copy when filing in person

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**RTIAssist — Bringing India's Right to Information to every citizen's fingertips.**

*Jan Shakti. Jan Jagruti. Jan Suchna.*
*(People's Power. People's Awareness. People's Information.)*

Powered by **[ASI-1 API](https://asi1.ai)** &nbsp;|&nbsp; Built with ❤️ by **[Shlok](https://github.com/shlok926)**

</div>