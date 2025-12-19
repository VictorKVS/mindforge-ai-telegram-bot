<p align="center"> <img src="assets/logo/mindforge_logo_neon.png" width="200" alt="MindForge Neon Logo"/> </p> <h1 align="center">🤖 MindForge AI Telegram Bot v2.0</h1> <p align="center"> <img src="assets/banners/industrial_neon_banner.png" width="100%" alt="MindForge Industrial Banner"/> </p> <p align="center"> <b>Industrial-Grade Secure AI Assistant for Enterprise Workflows</b><br/> <sub>Powered by MindForge UAG • MSDLC • KR API • Multi-Agent Brain • Zero-Trust AI Architecture</sub> </p>
<p align="center"> <img src="https://img.shields.io/badge/AI-KM6%20MultiAgent-purple?style=for-the-badge&logo=openai"/> <img src="https://img.shields.io/badge/API-FastAPI%20%7C%20OpenAPI%203.1-blue?style=for-the-badge&logo=fastapi"/> <img src="https://img.shields.io/badge/Security-Zero%20Trust-red?style=for-the-badge&logo=shield"/> <img src="https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python"/> <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/> </p>
<p align="center"> <a href="#english-version">🇬🇧 English Version</a> • <a href="#русская-версия">🇷🇺 Русская версия</a> • <a href="docs/mindforge_ai_telegram_bot_shema.md">📘 Architecture Schema</a> </p>
📑 Table of Contents

Overview

Architecture

Security Model

AI Integration

Interview Agent

Installation

Configuration

Run

Roadmap

License

English Version

Русская версия

🚀 Overview

MindForge AI Telegram Bot v2.0 is an advanced enterprise-grade AI assistant designed for:

internal automations

support workflows

HR interviews

decision support

secure interaction with corporate knowledge

Unlike traditional bots, this assistant:

never talks directly to LLMs,

never touches raw data,

never bypasses policies.

All actions are processed through:

Security Pipeline

MindForge UAG (Zero-Trust Gateway)

KM-6 Multi-Agent Brain

KR API Retrieval Engine

Shared Enterprise Knowledge Base

This makes the bot compliant, auditable, predictable, and safe.
"""
🏗 Architecture
User
  ↓
Telegram Bot (UI)
  ↓
──────────── SECURITY PIPELINE ────────────
  Input Sanitization
  Entropy Analysis
  Prompt Injection Filter
  Rate Limit
  Pattern Blocker
────────────────────────────────────────────
  ↓
MindForge UAG (Zero-Trust Gateway)
  ↓
────────── INTELLIGENCE LAYER (KM-6) ───────
  Interview Agent
  Knowledge Agent
  Security Agent
  Workflow Agent
────────────────────────────────────────────
  ↓
MindForge KR API (Retrieval Engine)
  ↓
Unified Knowledge Base (Shared KB)
  ↓
Embeddings → Vector Store
  ↓
LLM (OpenAI / Qwen / LLaMA / Mistral)
  ↓
Response → UAG → Bot → User

"""
Именно такая цепочка обеспечивает контроль, безопасность, контекст, прозрачность, отказоустойчивость.

🔒 Security Model (Zero-Trust AI)

MindForge Bot has a 3-layer security system:

🛡 Layer 1 — Input Protection

Before any data reaches UAG:

normalization

max length control

high-entropy detection

unicode sanitization

SQL/OS code detection

base64/hex obfuscation block

anti-jailbreak ruleset

🛡 Layer 2 — Prompt Injection Defense

Blocks:

jailbreak payloads

prompt boundary violations

"ignore previous" attacks

recursive instruction rewriting

model hijacking sequences

encoded prompt injections

🛡 Layer 3 — UAG Enforcement

UAG ensures:

RBAC / ABAC permissions

masked parameters

action-level capability control

audit trail

kill-switch

rate limiting

compliance logging

This protects the enterprise from LLM-related risks.

🧠 AI Integration

Bot uses a hybrid intelligent pipeline:

✔ KR API — Knowledge Retrieval

Retrieves relevant context from the Unified Knowledge Base and vector store.

✔ LLM Reasoning Layer

Generates controlled responses based on:

sanitized input

enriched context

enforced policies

✔ KM-6 Multi-Agent Brain

Decides how to answer, not just what to answer.

Agents include:

Interview Agent

Knowledge Agent

Workflow Agent

Security Agent

🎤 Interview Agent

One of the core capabilities of v2.0.

It allows the bot to:

conduct structured interviews

generate multi-level questions (L1–L6)

evaluate answers using AI scoring

increase/decrease difficulty

fetch context through KR API

produce final interview reports

Example workflow:
User → “Interview me for Python Engineer”
Bot → starts InterviewAgent
Agent → asks L2 question
User → answers
Agent → evaluates + adjusts difficulty
Agent → continues until final report
Bot → sends structured PDF/JSON report

🛠 Installation
git clone https://github.com/<your_repo>/mindforge-ai-telegram-bot.git
cd mindforge-ai-telegram-bot
pip install -r requirements.txt

⚙️ Configuration

Rename:

cp .env.example .env


Fill:

TELEGRAM_TOKEN=
UAG_API_KEY=
LLM_API_KEY=
KR_API_URL=http://localhost:8000/rag/query

▶️ Run
python src/bot/bot.py


Bot will start with activated:

Security Pipeline

UAG Gateway

Interview Agent

KR API integration

🗺 Roadmap
🔜 v2.1

Workflow Agent automation

Ticket system integration

Role-aware messaging

🔜 v3.0

Autonomous Mode (KM-6 full intelligence)

Agent task planning

Continuous learning system

Multi-LLM routing

Dashboard & Admin Panel

📄 License

MIT License.

🇬🇧 English Version

This entire README is the English version.

🇷🇺 Русская версия

Полная локализация будет добавлена по запросу.
