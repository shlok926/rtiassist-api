---
title: RTIAssist API
emoji: 🏛️
colorFrom: blue
colorTo: green
sdk: docker
pinned: true
license: mit
app_port: 7860
---

# 🏛️ RTIAssist API — AI-Powered RTI Generator for India

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)

## What is RTIAssist?

RTIAssist is India's most powerful **AI-powered RTI (Right to Information) application generator**. It helps Indian citizens create **legally correct, complete RTI applications in seconds** — in 11 Indian languages and for all 28+ states.

Built with the **ASI-1 AI API** by [Fetch.ai](https://fetch.ai).

## ✨ Features

- **🤖 4-Layer AI Reasoning Pipeline**
  - Layer 1: Intent Classifier — Identifies correct department, ministry, urgency
  - Layer 2: PIO Resolver — Finds correct Public Information Officer details
  - Layer 3: Draft Generator — Creates legally correct RTI applications
  - Layer 4: Quality Checker — Reviews completeness and Section 8 exemption risks

- **🌐 Multi-Language Support**
  - Hindi, English, Marathi, Tamil, Telugu, Gujarati, Bengali, Kannada, Malayalam, Punjabi, Odia

- **📍 Pan-India Coverage**
  - Central Government + All 28 States + 8 Union Territories

- **📊 Quality Assurance**
  - Quality score out of 100
  - Section 8 exemption risk detection
  - Success probability estimation
  - Improvement suggestions

- **🎯 Smart Features**
  - Auto state detection from description
  - Urgency level classification (routine/urgent/life-threatening)
  - Filing fee and payment mode information
  - Step-by-step filing instructions
  - Appeal letter generator

- **🎭 Demo Mode**
  - Instant sample responses without API calls
  - Perfect for testing and demonstrations

## 🚀 Quick Start

### Using the API

Send a POST request to `/rti/generate`:

```bash
curl -X POST "https://huggingface.co/spaces/YOUR_USERNAME/rtiassist-api/rti/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My ration card application was rejected 3 months ago in Maharashtra, I want to know the exact reason and who rejected it",
    "language": "english",
    "state": "Maharashtra",
    "demo_mode": true
  }'
```

### Demo Mode

Set `demo_mode: true` to get instant sample responses without making actual AI API calls. Perfect for:
- Testing the system
- Demonstrations
- When API quota is limited

### Response

You'll receive a complete RTI application with:
- Complete draft ready to file
- Filing instructions
- Quality score and success probability
- PIO details and contact information
- Warnings and suggestions

## 📖 API Documentation

Once deployed, visit:
- **Swagger UI:** `/docs`
- **ReDoc:** `/redoc`

## 🏗️ Architecture

```
User Input
    ↓
Intent Classifier (ASI-1 AI)
    ↓
PIO Resolver (Rule-based + AI)
    ↓
Draft Generator (ASI-1 AI)
    ↓
Quality Checker (ASI-1 AI)
    ↓
Complete RTI Application
```

## 🔧 Tech Stack

- **Framework:** FastAPI
- **AI Model:** ASI-1 Mini by Fetch.ai
- **Language:** Python 3.8+
- **Deployment:** Hugging Face Spaces / Docker
- **Telegram Bot:** python-telegram-bot (optional)

## 🌟 Use Cases

1. **Citizens** — Generate RTI applications instantly
2. **NGOs** — Help communities file RTIs at scale
3. **Journalists** — Quick RTI filing for investigations
4. **Researchers** — Obtain government data efficiently
5. **Students** — Learn about RTI Act implementation

## 📱 Telegram Bot

The project includes a Telegram bot with:
- **Dual language system:**
  - UI Language: Language for bot messages (8 languages)
  - Draft Language: Language for RTI document (10 languages)
- State auto-detection
- Appeal letter generator
- Interactive buttons for easy navigation

## 🎯 Priority Feature Roadmap

- ✅ **Day 1:** Demo Mode (COMPLETED)
- ✅ **Day 2:** Dual Language Telegram Bot (COMPLETED)
- 🔄 **Day 3:** Hugging Face Deployment (IN PROGRESS)
- 📋 **Day 4:** Hindi UI Toggle for Web
- 📋 **Day 5:** Visual Filing Guide + Success Stories
- 📋 **Day 6:** Comprehensive Testing

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/shlok926/rtiassist-api.git
cd rtiassist-api

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run API server
uvicorn main:app --reload --port 8000

# Run Telegram bot (optional)
python telegram_bot.py
```

## 🔐 Environment Variables

- `ASI1_API_KEY` — Your ASI-1 API key
- `ASI1_API_URL` — ASI-1 API endpoint
- `TELEGRAM_TOKEN` — Telegram bot token (optional)
- `DEMO_MODE` — Set to `true` for demo mode

## 📄 License

MIT License — Feel free to use and modify for your needs.

## 👨‍💻 Developer

Built by **[Shlok](https://github.com/shlok926)** · Powered by ASI-1 API

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## ⭐ Support

If you find this project helpful:
- Star the repository
- Share with others who might benefit
- Report bugs or suggest features

## 📞 Contact

- **GitHub:** [@shlok926](https://github.com/shlok926)
- **Project:** [RTIASSIST-API](https://github.com/shlok926/RTIASSIST-API)

---

**Built with ❤️ for Indian Citizens**

*Making Government Information Accessible to All*
