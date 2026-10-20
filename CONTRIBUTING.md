# Contributing to RTIAssist

Thank you for your interest in contributing to **RTIAssist**! We welcome contributions to help empower Indian citizens with AI-driven Right to Information (RTI) drafts and civic legal assistance tools.

---

## Code of Conduct

This project adheres to the Contributor Covenant. By participating, you are expected to uphold this code. Please review our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details on expected behavior and reporting guidelines.

---

## 🛠️ Getting Started

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** & **npm**
- **Git**

### 1. Fork & Clone
```bash
git clone https://github.com/<your-username>/rtiassist-api.git
cd rtiassist-api
```

### 2. Backend Setup
```bash
# Create and activate Python virtual environment
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
npm install
```

### 4. Environment Variables
Copy `.env.example` to `.env` and fill in necessary keys (e.g., `ASI1_API_KEY`, `TELEGRAM_TOKEN` if testing bot features):
```bash
cp .env.example .env
```

---

## 🧪 Running Tests

Always ensure existing tests pass before submitting a pull request:

### Backend Tests (Python)
```bash
pytest
```

### Frontend Tests (Vitest)
```bash
npm run test
```

### Frontend Build Check
```bash
npm run build
```

---

## 🌿 Branching & Git Workflow

1. Create a dedicated branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
2. Make atomic, well-documented commits:
   ```bash
   git commit -m "feat(authority): add support for state-level portal integration"
   ```
3. Push your branch to your fork:
   ```bash
   git push origin feat/your-feature-name
   ```
4. Open a Pull Request targeting `main`.

---

## 💡 Contribution Opportunities

- **Language Expansion**: Help add or refine translations for Indian regional languages (Tamil, Telugu, Kannada, Bengali, Odia, Marathi, Punjabi, Gujarati, etc.).
- **Authority Mappings**: Expand PIO directories and jurisdiction resolution data for Central and State government departments.
- **RTI Legal Precedents**: Add real-world RTI applications and appeal templates to the examples library.
- **UX & Accessibility**: Enhance responsiveness and assistive toolings for citizens with varying digital literacy.

---

## 🔒 Security

For responsible disclosure of security vulnerabilities, please refer to our [SECURITY.md](SECURITY.md).
