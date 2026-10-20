# Changelog

All notable changes to **RTIAssist** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Created formal root-level `LICENSE.md` (MIT License) and `CONTRIBUTING.md`.
- Consolidated release milestones and phase documentation into `CHANGELOG.md`.

---

## [1.2.0] - 2026-10-20

### Added
- **Phase 16 - Final Production Audit**: Comprehensive case isolation and security verification.
- Telegram-to-Web parity validation tests.
- Step 1C & Step 1D scheduled monitoring with atomic locking and timezone handling.

### Fixed
- Migrated password hashing from `passlib` to native `bcrypt` for Python 3.12+ compatibility and security hardening.
- Vitest 5 test runner compatibility for native jsdom localStorage in frontend unit tests.
- Fixed Render deployment start command configuration.

---

## [1.1.0] - 2026-10-15

### Added
- **Phase 15 - Product Hardening**:
  - Authority population and data verification tests (`test_authority_population.db`).
  - Response mapping and real-world case validation suites.
- **Phase 14 - Citizen Experience**:
  - Central citizen UI workspace with Vite and responsive layout.
  - Multi-language interface support (11 Indian regional languages).
  - PDF export and WhatsApp share integration.

---

## [1.0.0] - 2026-10-01

### Added
- **Core 4-Layer AI Pipeline**:
  - Layer 1: Citizen Intent Extractor.
  - Layer 2: PIO Authority Resolver (State & Central Government departments).
  - Layer 3: Legally structured RTI Application Drafter.
  - Layer 4: Exemption Risk & Quality Scorer (0–100 score).
- **Telegram Bot**:
  - Webhook-integrated Telegram bot for conversational RTI drafting (`/start`, `/newcase`, `/cases`, `/help`).
  - Automated deadline tracking and reminders (First Appeal at 30 days, Second Appeal at 90 days).
- **Legal Tools Suite**:
  - Consumer Court Complaint generator.
  - Legal Notice drafter.
  - Labour Court Complaint generator.
  - Second Appeal petition generator.
- **Examples Library**: 44 real-world RTI scenarios across health, roads, municipal services, exams, and subsidies.
- **Deployment**: Hugging Face Spaces & Render deployment templates (`render.yaml`, `Procfile`, `start.sh`).
