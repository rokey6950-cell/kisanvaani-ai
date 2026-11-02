# KisanVaani AI (किसानवाणी AI)
> **"अपनी भाषा, अपनी खेती, Smart Faisle."**  
> *Voice-First AI Agricultural Assistance Platform for Indian Farmers*

---

## 🌾 1. Project Overview & Vision

**KisanVaani AI** is a voice-first, multi-platform agricultural intelligence system built specifically for Indian farmers. Designed for accessibility, the platform enables farmers—regardless of their digital literacy—to ask farming questions in their regional language (primarily Hindi) through voice or text, receiving accurate, grounded, and safe agricultural guidance in real time.

### Target Regions (North & Central India)
1. **Haryana**
2. **Punjab**
3. **Uttar Pradesh**
4. **Rajasthan**
5. **Himachal Pradesh**
6. **Uttarakhand**
7. **Delhi NCR**

---

## 🚀 2. System Architecture & Tech Stack

```
                                  +---------------------------------------+
                                  |     React 18 + Vite + Tailwind CSS    |
                                  |  (8 Production Pages + Dual STT/TTS)  |
                                  +-------------------+-------------------+
                                                      |
                                         HTTP / JSON  |  Vite Proxy (/api/v1)
                                                      v
                                  +---------------------------------------+
                                  |           FastAPI Application         |
                                  |       (Modular Service Architecture)  |
                                  +----+--------------+----------------+--+
                                       |              |                |
                    +------------------+              |                +------------------+
                    v                                 v                                   v
+-----------------------+         +-----------------------+         +-----------------------+
|  SQLite / PostgreSQL  |         | Agricultural KB Engine|         | Voice & Ext. Services |
|  - Conversations      |         | - 44 JSON Files       |         | - Gnani Prisma STT    |
|  - Chat Messages      |         | - 114 Domain Records  |         | - Gnani Timbre TTS    |
|  - Audit Timestamps   |         | - 37 Source Registry  |         | - IMD Agromet Format  |
+-----------------------+         +-----------------------+         +-----------------------+
```

### Technology Highlights
- **Backend**: Python 3.13, FastAPI, Pydantic v2, SQLAlchemy, Uvicorn, HTTPX.
- **Frontend**: React 18, Vite 6, Tailwind CSS, Lucide Icons, React Router v6.
- **Voice Stack**:
  - **Speech-to-Text**: Gnani Prisma v2.5 integration with browser Web Speech API fallback.
  - **Text-to-Speech**: Gnani Timbre v2.5 integration with HTML5 SpeechSynthesis fallback.
- **Database**: SQLite default (zero-config local persistence), PostgreSQL migration ready via SQLAlchemy.
- **Knowledge Base**: 44 structured, source-traced JSON files with strict schema validation.

---

## 🌟 3. The 8 Core Features & Pages

| # | Feature / Page | Capabilities & Guardrails |
|---|---|---|
| **1** | **AI Voice Assistant** (`/assistant`) | Large microphone UI, real-time waveform recording animation, audio upload, Gnani Prisma STT transcription, grounded AI answer retrieval, and Gnani Timbre TTS playback. |
| **2** | **Smart Crop Advisory** (`/crop-advisory`) | Sowing calendar, seed varieties (DBW-187, HD-3086, etc.), irrigation stages (CRI), and pest/disease IPM guidance. **Safety Rule**: Never invents chemical doses; directs farmers to KVK Helpline (**1800-180-1551**). |
| **3** | **Government Scheme Navigator** (`/schemes`) | Catalog for **PM-KISAN** (₹6,000/yr, helpline 155261), **PMFBY** (14447, 72h damage window), **PMKSY**, **Soil Health Card**, **SMAM**, and **mKisan**. Official links only; no personal data collected. |
| **4** | **Mandi Price Information** (`/mandi`) | 15 benchmark markets across 7 pilot states. Min/Max/Modal prices and arrivals in tonnes. Clearly labeled `data_type="sample"` pending official AGMARKNET API access. |
| **5** | **Weather & Agromet Guidance** (`/weather`) | 17 agro-meteorological stations across 7 states. Current metrics + **5-day forecast** + 3 specialized advisories: **Spray Feasibility** (wind/rain thresholds), **Irrigation Need**, and **Harvest Safety**. Discloses IMD non-commercial policy with links to [`mausam.imd.gov.in`](https://mausam.imd.gov.in) and Meghdoot App. |
| **6** | **Multilingual Engine** (All Pages) | Hindi-first UI, toggle for English, Haryanvi-accent test models. |
| **7** | **Conversation History** (`/history`) | Multi-turn session persistence, timestamped Q&A records, message details drawer, individual conversation deletion, and clear-all actions. |
| **8** | **About KisanVaani AI** (`/about`) | Complete data provenance, source registry (ICAR, Ministry of Ag), farmer safety principles, and explicit limitations disclosure. |

---

## 🔒 4. Agricultural Safety & Ethics Guardrails

KisanVaani AI follows non-negotiable safety guardrails:
1. **Zero Chemical Fabrication**: The system **never** guesses or invents pesticide mixtures, insecticide concentrations, or fertilizer formulas. When an unverified question is asked, it provides cultural/IPM practices and refers the farmer to the local **Krishi Vigyan Kendra (KVK)** or Toll-Free Kisan Helpline (**1800-180-1551**).
2. **Honest Data Attribution**: Every data point is tagged with one of:
   - `official_static` (verified government publication / university package)
   - `sample` (benchmark demonstration data)
   - `unverified` (flagged for review)
3. **No Fake Live Data**: When live feeds (AGMARKNET, live IMD) lack commercial keys, the platform explicitly displays sample disclosures rather than masquerading mock data as live.

---

## ⚙️ 5. Installation & Setup

### Prerequisites
- **Python**: 3.10+ (tested on Python 3.13)
- **Node.js**: v18+ (tested on Node v22)
- **Git**

### Backend Setup
```powershell
# 1. Navigate to backend directory
cd d:\kisanvaani-ai\backend

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate # Linux/macOS

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure environment variables (.env)
cp .env.example .env
# Edit .env with your optional Gnani credentials:
# GNANI_API_KEY="your-key-here"
# GNANI_STT_MODEL="v2.5"
# GNANI_TTS_MODEL="v2.5"

# 5. Start the FastAPI development server
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
Backend API will be accessible at `http://127.0.0.1:8000` with Swagger docs at `http://127.0.0.1:8000/docs`.

### Frontend Setup
```powershell
# 1. Navigate to frontend directory
cd d:\kisanvaani-ai\frontend

# 2. Install Node dependencies
npm install

# 3. Start Vite dev server (proxies /api/v1 to port 8000)
npm run dev

# 4. Production build check
npm run build
```
Frontend will be accessible at `http://localhost:5173`.

---

## 🧪 6. Testing & Quality Assurance

The project includes an extensive test suite verifying all 8 phases:

```powershell
# Run the complete test suite (58 passing tests)
backend\.venv\Scripts\pytest.exe tests\ -v --tb=short

# Run knowledge base schema & integrity validator
backend\.venv\Scripts\python.exe validate_knowledge_base.py
```

### Test Suite Structure (58 Tests)
- `tests/test_backend_health.py`: Health endpoints, DB connection, subsystem status.
- `tests/test_database.py`: SQLAlchemy session lifecycle, Conversation/Message models.
- `tests/test_knowledge_loader.py`: JSON parsing, tolerance of empty catalogs, schema loading.
- `tests/test_assistant.py`: Grounded chat, stop-word filtering, unknown query safety fallbacks.
- `tests/test_voice.py` & `test_voice_e2e.py`: Gnani Prisma STT, Timbre TTS, audio validation, browser fallbacks.
- `tests/test_phase3_knowledge.py`: Seed varieties, glossary, agro-climatic zones, multi-turn contexts.
- `tests/test_phase4_crop_advisory.py`: Districts, topics, sowing calendars, IPM pest safety, KVK helpline.
- `tests/test_phase5_schemes.py`: PM-KISAN, PMFBY, search endpoints, category filters.
- `tests/test_phase6_mandi.py`: 15 pilot markets, commodity filters, sample flags, AGMARKNET disclaimer.
- `tests/test_phase7_weather.py`: 17 IMD agromet stations, spray/irrigation/harvest logic, 5-day forecast.
- `tests/test_phase8_integration.py`: End-to-end multi-route farmer journeys, full history lifecycle.

---

## 📡 7. API Reference Overview

| Prefix | Key Routes | Description |
|---|---|---|
| `/api/v1/health` | `GET /health` | Subsystem connectivity (DB, KB, total records) |
| `/api/v1/assistant` | `POST /assistant/chat` | Grounded multi-turn conversational Q&A |
| `/api/v1/voice` | `GET /status`, `POST /transcribe`, `POST /speak` | Gnani Prisma STT & Timbre TTS pipeline |
| `/api/v1/crop-advisory` | `GET /districts`, `GET /topics`, `POST /recommendation` | Verified crop guidance & KVK referral |
| `/api/v1/schemes` | `GET /`, `GET /search`, `GET /{id}` | Verified government agricultural schemes |
| `/api/v1/mandi-prices` | `GET /`, `GET /markets`, `GET /commodities`, `GET /status` | Benchmark mandi prices & market status |
| `/api/v1/weather` | `GET /`, `GET /locations`, `GET /status`, `GET /advisory` | IMD agromet parameters & farm advisories |
| `/api/v1/knowledge` | `GET /seeds`, `GET /glossary`, `GET /zones`, `GET /status` | Direct knowledge base access |
| `/api/v1/history` | `GET /`, `GET /{id}`, `DELETE /{id}`, `DELETE /` | Conversation history management |

---

## 📑 8. Licenses & Attribution
- Agricultural package recommendations derived from ICAR and State Agricultural University research packages (CCS HAU Hisar, PAU Ludhiana, GBPUAT Pantnagar).
- Scheme information sourced directly from official government portals (`pmkisan.gov.in`, `pmfby.gov.in`).
- Weather formatting adheres to IMD Agromet Advisory format standards.
- Designed & engineered for the Indian agricultural ecosystem.
