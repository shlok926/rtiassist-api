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

</div>

---

## 🧩 Problem Statement

Over **65 million RTI applications** are filed in India every year — yet most citizens struggle to:

- Identify the **correct government department** to address
- Draft a **legally correct application** under RTI Act 2005
- Understand what information is **legally accessible** vs. exempt
- Know **how and where to file** their application

RTIAssist solves all 4 problems in one tool — for free, in seconds.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **4-Layer AI Pipeline** | Intent → PIO Resolver → Draft → Quality Check |
| 🌐 **11 Indian Languages** | Hindi, English, Tamil, Telugu, Kannada, Bengali + more |
| 📱 **Telegram Bot** | Full RTI + Legal tools via Telegram |
| ⚖️ **Legal Tools** | Consumer Court, Legal Notice, Labour Complaint, Second Appeal |
| 💡 **Legal Examples Library** | 44 real-world examples with prefilled forms |
| 🎯 **Quality Score** | 0–100 score + exemption risk analysis |
| 🆓 **Demo Mode** | Works without API key for testing |
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
# API Server (port 7860)
python app.py

# Telegram Bot (separate terminal)
python telegram_bot.py

# Website (port 8080)
python -m http.server 8080
# Open: http://localhost:8080/index_Version4.html
```

---

## 📖 Usage

### Generate an RTI via Website
1. Open `http://localhost:8080/index_Version4.html`
2. Click **RTI Generator**
3. Describe your problem in plain language
4. Select language + state
5. Click **Generate** — download or copy your RTI draft

### Use Legal Tools
1. Click **Legal Tools** in the navbar
2. Choose: Consumer Complaint / Legal Notice / Labour Complaint / Second Appeal
3. Fill in the form (or pick from **Legal Examples Library**)
4. Generate your legal draft instantly

### Telegram Bot
Send `/start` to the bot → choose language → pick tool → describe your problem → get your draft.

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
/start   — Start the bot and choose language
/help    — How to use RTIAssist
/about   — About this tool
```

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
- Add more Indian languages
- Improve legal draft quality
- Add more RTI examples
- UI improvements

---

## 🔮 Future Scope

- RTI Status Tracker via registered post number
- WhatsApp Bot integration
- Verified PIO directory for 700+ Central Government departments
- Android/iOS mobile app
- OCR — scan rejection letters and auto-draft appeals

---

## 👨‍💻 Author

**Shlok** — [@shlok926](https://github.com/shlok926)

Built with ❤️ to empower Indian citizens with their Right to Information.
Powered by **ASI-1 API** by [Fetch.ai](https://fetch.ai)

---

## ⚠️ Disclaimer

RTIAssist is an informational tool to help citizens draft RTI applications. It does not constitute legal advice. Always verify PIO details before filing. The generated drafts should be reviewed before submission.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.