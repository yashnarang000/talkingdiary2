# Talking Diary

**Talking Diary** is a voice-first, emotionally-aware journaling tool that talks back.
You speak or type — it listens, replies like a human, and writes your day.

---

## 🌱 What it is (for now)

A modular experiment in emotional journaling.
Backends are swappable — cloud AI or local models. Frontends are open-ended — from bots to classic apps.

---

## 🧠 Why I’m building this

* Tired of blank pages and silent logs
* Wanted a diary that feels like a **friend**, not a form
* Curious how human-like these systems can actually get

---

## 🧩 Current Plan

### 🎯 Backend Modules

#### Premade / Web Agent Modules

* `PiModule` - using Pi AI as primary conversational engine via browser automation
* `UnmuteModule` – Hooks into tools like Unmute.sh

> May use Playwright or similar tools for interaction.

#### Model / API-Based Modules

* `KyutaiSST` – Speech-to-text (local/cloud)
* `KyutaiTTS` – Text-to-speech (local/cloud)
* `LLaMaGen` – Text generation (local/cloud)
* `GeminiJournalizer` / `DeepSeekJournalizer` – Entry summarizer/writer

---

### 🖥️ Frontend Ideas

* Telegram Bot (prototype)
* Desktop App (traditional diary look)
* Web Interface
* Mobile App (maybe later, maybe not)

---

## 📊 Feature Wishlist

* Daily mood logging
* Monthly emotional graphs
* Offline journaling with synced backup

---

## 🧱 Tech Stack (WIP)

* Python backend
* Browser automation: Playwright/Selenium
* APIs + Local AI models
* Maybe SQLite for local data storage

---

## 🚧 Project Status

Still building the bones.
Starting with backend → hooking up frontends next.

---